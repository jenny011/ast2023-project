#!/usr/bin/env python3

from enum import Enum
import argparse, json
from extractor import *
from numbers import Number

if __name__ == "__main__":
    log_base = "/home/mysql/sqlancer/target"
    log_name = "logs_33_4hour"
    test_db = "database0"
    parser = argparse.ArgumentParser()
    parser.add_argument("--testdb", default=test_db, required=False)
    parser.add_argument("--logbase", default=log_base, required=False)
    parser.add_argument("--logname", default=log_name, required=False)
    parser.add_argument("--cur", type=int, default=0, required=False)
    args = parser.parse_args()

    test_db = args.testdb
    log_base = args.logbase
    log_name = args.logname
    log_dir = f"{log_base}/{log_name}/mysql"
    cur = bool(args.cur)
    if cur:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        qfile = f"{log_dir}/{test_db}-cur.log"
    else:
        qfile = f"{log_dir}/{test_db}.log"

    print(f">>>>>>>>{test_db}")
    _, queries = extract_queries(qfile)
    print(len(queries))

    with open(f"result_{log_name}/{test_db}.json", "r") as f:
        index = json.load(f)
    print(index)

    print("[LEN]")
    for i in index["3"]:
        print(i)
        print(">", queries[i])
    print("[CONTENT]")
    for i in index["4"]:
        print(i)
        print(">", queries[i])
    count = len(index["3"]) + len(index["4"])
    print("TOTAL:", count)
    
