#!/bin/bash

BASE="/home/mysql/ast2023-project/sqlancer_logs"
#NAME="33logs_1685867597"
#NAME="33logs_1685823328"
NAME="11logs_1685808316"
#BASE="/home/mysql/sqlancer/target"
#NAME="logs_33_4hour"
for (( i=0; i<=99; i++ ))
do
	./list_queries.py --cur 1 --logbase $BASE --logname $NAME --testdb database$i
done
