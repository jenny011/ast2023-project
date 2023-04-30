#!/usr/bin/env python3

import psycopg2
from enum import Enum
import argparse, json
from extractor import *


DIFF = Enum('DIFF', ['SAME', 'CRASH', 'LEN', 'CONTENT'])

def check_setup(cur):
    cur.execute("SELECT * FROM information_schema.tables")
    tables = cur.fetchall()
    for line in tables:
        if len(line) > 0 and line[0] == "regression":
            return True

    print("[ERR] missing 'regression' table")
    return False

def execute_and_print(cur152, cur140, query):
    err152 = None
    err140 = None
    ret152 = None
    ret140 = None

    try:
        cur152.execute(query)
    except Exception as e:
        err152 = e
    try:
        cur140.execute(query)
    except Exception as e:
        err140 = e


    if not err152 and not err140:
        try:
            ret152 = cur152.fetchall()
        except Exception as e:
            err152 = e
        try:
            ret140 = cur140.fetchall()
        except Exception as e:
            err140 = e

    print("-----"*20)
    print(f"<<<152>>>\nret: {ret152}\nerr: {err152}")        
    print("-----"*20)
    print(f"<<<140>>>\nret: {ret140}\nerr: {err140}")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qfile", default="queries_many", required=False)
    parser.add_argument("--id", type=int, required=True)
    args = parser.parse_args()
    

    # connect to db 152 and 140
    conn152 = psycopg2.connect(database="regression",
                        host="/tmp",
                        user="postgres152",
                        password="postgres152",
                        port="5432")


    conn140 = psycopg2.connect(database="regression",
                        host="/tmp",
                        user="postgres140",
                        password="postgres140",
                        port="5433")

    cur152 = conn152.cursor()
    cur140 = conn140.cursor()

    if not (check_setup(cur152) and check_setup(cur140)):
        return

    # extract queries
    print("[MSG] extract query")
    queries = extract_queries(args.qfile)
    print(len(queries))
    q = queries[args.id]

    # execute queries and compare results
    print(q)
    #execute_and_print(cur152, cur140, q)
    conn152.commit()
    conn140.commit()

    conn152.close()
    conn140.close()
        

if __name__ == "__main__":
    main()
