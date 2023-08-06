# -*- coding:utf-8 -*-
import sys
import pymysql.cursors
import queue
import time
import threading
import logging
import logging.handlers


def init_log(log_name='mysqlutil'):
    logger = logging.getLogger(name=log_name)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


log = init_log()


def escape_name(s):
    return f"`{s.replace('`', '``')}`"


class DB:

    def __init__(self, conn_info=None, max_cached=5, idle_time=300):
        self._conn_info = conn_info
        if not self._conn_info:
            log.error('need connection information')
            sys.exit(1)
        for k in ['host', 'user', 'password', 'db']:
            if k not in self._conn_info:
                log.error('need %s configuration' % k)
                sys.exit(1)

        #
        self._max_cached = min(max_cached, 20)
        self._max_cached = max(self._max_cached, 1)
        self._idle_time = max(idle_time, 300)
        self._idle_time = min(self._idle_time, 1800)
        self.pool = queue.Queue(maxsize=self._max_cached)

        # check pool
        t = threading.Thread(target=self._check_pool)
        t.setDaemon(True)
        t.start()

    def _create_conn(self):
        conn = pymysql.connect(host=self._conn_info['host'],
                               port=self._conn_info['port'],
                               user=self._conn_info['user'],
                               password=self._conn_info['password'],
                               db=self._conn_info['db'],
                               charset=self._conn_info['charset'],
                               cursorclass=pymysql.cursors.DictCursor)

        return conn

    def get_conn(self):
        try:
            return self.pool.get_nowait()[0]
        except queue.Empty:
            return self._create_conn()

    def recycle(self, conn):
        if not conn:
            return
        try:
            self.pool.put_nowait((conn, time.time()))
        except queue.Full:
            conn.close()

    def _check_pool(self):
        while True:
            time.sleep(10)
            self._check_alive()

    def _check_alive(self):
        try:
            conn, last_time = self.pool.get_nowait()
        except queue.Empty:
            return
        try:
            conn.ping(reconnect=False)
            if time.time() - last_time > self._idle_time:
                conn.close()
                log.debug('remove a connection idle more than %ss' % self._idle_time)
            else:
                try:
                    self.pool.put_nowait((conn, last_time))
                except queue.Full:
                    conn.close()
        except pymysql.err.Error:
            log.debug('remove a closed connection')

    def fetchall(self, sql, data=()):
        ret = []
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cur:
                if not data:
                    cur.execute(sql)
                else:
                    cur.execute(sql, data)
                ret = cur.fetchall()
            conn.commit()
        finally:
            self.recycle(conn)
        return ret

    def fetchone(self, sql, data=()):
        ret = None
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cur:
                if not data:
                    cur.execute(sql)
                else:
                    cur.execute(sql, data)
                ret = cur.fetchone()
            conn.commit()
        finally:
            self.recycle(conn)
        return ret

    def fetchmany(self, sql, num, data=()):
        ret = None
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cur:
                if not data:
                    cur.execute(sql)
                else:
                    cur.execute(sql, data)
                ret = cur.fetchmany(num)
            conn.commit()
        finally:
            self.recycle(conn)
        return ret

    def execute(self, sql, data=()):
        ret = False
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cur:
                if not data:
                    cur.execute(sql)
                else:
                    cur.execute(sql, data)
            conn.commit()
            ret = True
        finally:
            self.recycle(conn)
        return ret

    def executemany(self, sql, data_list):
        ret = False
        conn = None
        try:
            conn = self.get_conn()
            with conn.cursor() as cur:
                cur.executemany(sql, data_list)
            conn.commit()
            ret = True
        finally:
            self.recycle(conn)
        return ret

    def insert(self, tbl, data):
        ret = False
        conn = None
        try:
            if isinstance(data, dict):
                names = list(data)
                cols = ', '.join(map(escape_name, names))
                placeholders = ', '.join([f'%({name})s' for name in names])
                query = f'INSERT INTO `{tbl}` ({cols}) VALUES ({placeholders})'
            elif isinstance(data, list):
                # TODO:
                pass

            conn = self.get_conn()
            with conn.cursor() as cur:
                cur.execute(query, data)
            conn.commit()
            ret = True
        finally:
            self.recycle(conn)
        return ret
