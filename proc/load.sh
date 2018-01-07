#!/bin/bash

python3 targz_to_csv.py


comm=$(mktemp)

echo "1. vytvarim databazi"
sqlite3 ../vystupy/data.db < cte.sql

cat <<EOF > $comm
.mode csv
.import /dev/stdin firmy
EOF

echo "2. nahravam firmy"
tail -n +2 ../vystupy/firmy.csv | sqlite3 --init $comm ../vystupy/data.db

cat <<EOF > $comm
.mode csv
.import /dev/stdin posoby
EOF

echo "3. nahravam pravnicke osoby"
tail -n +2 ../vystupy/posoby.csv | sqlite3 --init $comm ../vystupy/data.db

cat <<EOF > $comm
.mode csv
.import /dev/stdin fosoby
EOF

echo "4. nahravam fyzicke osoby"
tail -n +2 ../vystupy/fosoby.csv | sqlite3 --init $comm ../vystupy/data.db

echo "5. indexuji"
sqlite3 ../vystupy/data.db < index.sql
