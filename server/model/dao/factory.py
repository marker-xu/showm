# -*- coding: utf-8 -*-
import torndb

DB_DICT = {
    "host": '127.0.0.1',
    "port": "9306",
    "database": "aip_show",
    "user": "root",
    "password": ""
}

g_db_map = {}


def get_db_inc(source='mmshow'):
    global g_db_map
    if source in g_db_map:
        return g_db_map[source]

    g_db_map[source] = torndb.Connection(host=DB_DICT["host"] + ":" + DB_DICT["port"],
                                         user=DB_DICT["user"],
                                         password=DB_DICT["password"],
                                         database=DB_DICT["database"])
    return g_db_map[source]
