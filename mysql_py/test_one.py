#!/usr/bin/env python3

import mysql.connector
from enum import Enum
import argparse, json
from extractor import *
from numbers import Number


DIFF = Enum('DIFF', ['SAME', 'CRASH', 'LEN', 'CONTENT'])

dbs = [33, 11]
db_configs = {}
conns = {}
curs = {}

def build_msg(msg0, msg1):
    return f"{dbs[0]}: {msg0}, {dbs[1]}: {msg1}"

def config_db(dbname, user, password, port):
    config = {}
    config["user"] = user
    config["password"] = password
    config["port"] = port
    db_configs[dbname] = config

def check_setup(cur, database):
    cur.execute("SELECT * FROM information_schema.tables")
    tables = cur.fetchall()
    for line in tables:
        if len(line) > 0 and line[0] == database:
            return True

    print(f"[ERR] missing {database} table")
    return False

def setup_db(dbname):
    # host = /tmp
    config = db_configs[dbname]
    conn = mysql.connector.connect(**config)

    conns[dbname] = conn
    curs[dbname] = conn.cursor()

    return True
    
def execute_dml(conn, cur, dmls):
    for dml in dmls:
        print("+", dml)
        try:
            cur.execute(dml)
            cur.fetchall()
        except:
            if "DATABASE" in dml:
                raise(Exception)
            else:
                print("Failed")
        conn.commit()
        print("DONE")

def execute_and_compare(cur1, cur2, query):
    print(">", query)
    err1 = None
    err2 = None
    try:
        cur1.execute(query)
    except Exception as e:
        err1 = e
    try:
        cur2.execute(query)
    except Exception as e:
        err2 = e

    if err1 and err2:
        return DIFF.SAME, build_msg(err1, err2)

    if not err1 and not err2:
        try:
            ret1 = cur1.fetchall()
        except Exception as e:
            err1 = e
        try:
            ret2 = cur2.fetchall()
        except Exception as e:
            err2 = e

        if err1 and err2:
            return DIFF.SAME, build_msg(err1, err2)
        
        if not err1 and not err2:
            if len(ret1) != len(ret2):
                return DIFF.LEN, build_msg(ret1, ret2)
            
            for i in range(len(ret1)):
                ret1[i] = tuple(str(x) if x else "0" for x in ret1[i])
                ret2[i] = tuple(str(x) if x else "0" for x in ret2[i])

            ret1.sort()
            ret2.sort()
            for i in range(len(ret1)):
                if ret1[i] != ret2[i]:
                    return DIFF.CONTENT, build_msg(ret1, ret2)

            return DIFF.SAME, "Same ret value"

    return DIFF.CRASH, build_msg(err1, err2)


def main():
    log_dir = "/home/mysql/sqlancer/target/logs_33_4hour/mysql"
    test_db = "database0"
    parser = argparse.ArgumentParser()
    parser.add_argument("--testdb", default=test_db, required=False)
    parser.add_argument("--logdir", default=log_dir, required=False)
    parser.add_argument("-i", type=int, required=True)
    args = parser.parse_args()

    test_db = args.testdb
    log_dir = args.logdir
    qfile = f"{log_dir}/{test_db}-cur.log" 

    for db in dbs:
        config_db(db, "root", "", f"548{db}")
        ok = setup_db(db)
        if not ok:
            return


    # extract queries
    print("[MSG] extract dml and query")
    dmls, queries = extract_queries(qfile)

    # setup test db
    print("[MSG] setup test db")
    for db in dbs:
        execute_dml(conns[db], curs[db], dmls)

    # execute queries and compare results
    query = queries[args.i]
    print(f"[MSG] Test starts")
    diff_query_ids = {DIFF.CRASH.value: [], 
                    DIFF.LEN.value: [], 
                    DIFF.CONTENT.value: []}
    comp, ret_str = execute_and_compare(curs[dbs[0]], curs[dbs[1]], query)
    print(f"[{comp}]", ret_str)
    for db in dbs:
        conns[db].commit()

    for db in dbs:
        conns[db].close()
 

if __name__ == "__main__":
    main()
