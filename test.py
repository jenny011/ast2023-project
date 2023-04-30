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

def execute_and_compare(cur152, cur140, query):
    err152 = None
    err140 = None
    try:
        cur152.execute(query)
    except Exception as e:
        err152 = e
    try:
        cur140.execute(query)
    except Exception as e:
        err140 = e

    if err152 and err140:
        return DIFF.SAME, f"152: {err152}, 140: {err140}"

    if not err152 and not err140:
        try:
            ret152 = cur152.fetchall()
        except Exception as e:
            err152 = e
        try:
            ret140 = cur140.fetchall()
        except Exception as e:
            err140 = e

        if err152 and err140:
            return DIFF.SAME, f"152: {err152}, 140: {err140}"
        
        if not err152 and not err140:
            if len(ret152) != len(ret140):
                return DIFF.LEN, f"152: {len(ret152)}, 140: {len(ret140)}"
            
            ret152.sort()
            ret140.sort()
            for i in range(len(ret152)):
                if ret152[i] != ret140[i]:
                    return DIFF.CONTENT, f"152: {ret152[i]}, 140: {ret140[i]}"

            return DIFF.SAME, "Same ret value"

    return DIFF.CRASH, f"152: {err152}, 140: {err140}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qfile", default="queries_many", required=False)
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
    # queries = queries[:5]

    # execute queries and compare results
    print(f"[MSG] Test starts: {len(queries)} in total")
    diff_query_ids = {DIFF.CRASH.value: [], 
                    DIFF.LEN.value: [], 
                    DIFF.CONTENT.value: []}
    for i, query in enumerate(queries):
        comp, ret_str = execute_and_compare(cur152, cur140, query)
        if (comp != DIFF.SAME):
            diff_query_ids[comp.value].append(i)
        print(f"[{comp}]", ret_str)
        conn152.commit()
        conn140.commit()

    conn152.close()
    conn140.close()

    ncrash = len(diff_query_ids[DIFF.CRASH.value])
    nlen = len(diff_query_ids[DIFF.LEN.value])
    ncontent = len(diff_query_ids[DIFF.CONTENT.value])
    print(f"[MSG] Test finished: crash: {ncrash}, len: {nlen}, content: {ncontent} diffs in total")

    # with open(f"result-{args.qfile}.json", 'w') as out:
    #     json.dump(diff_query_ids, out)
        

if __name__ == "__main__":
    main()
