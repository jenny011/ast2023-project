#!/bin/bash

BASE="/home/mysql/ast2023-project/sqlancer_logs"
LOGNAME="11logs_1685808316"
#DIR="/home/mysql/ast2023-project/sqlancer_logs/33logs_1685867597/mysql"
#DIR="/home/mysql/sqlancer/target/logs_33_4hour/mysql"
#DIR="/home/mysql/ast2023-project/sqlancer_logs/33logs_1685823328/mysql"
DIR="$BASE/$LOGNAME/mysql"

if [ ! -d ./result_$LOGNAME ]; then
	mkdir ./result_$LOGNAME
fi

for (( i=0; i<=99; i++ ))
do
	./test.py --cur 1 --logdir $DIR --logname $LOGNAME --testdb database$i
done
