#!/bin/bash

DB_FILE=./Mac.db
read -p "Enter MAC (like askg4h2g):" mac
#echo $mac
#Maybe use sqlite3 = `which sqlite3`
pat="^[0-9a-z]{1,12}$"
if [[ $mac =~ $pat ]]; then

Result=$(sqlite3 $DB_FILE "SELECT * FROM mac_addresses WHERE mac LIKE '%$mac%';")

if [ -z "$Result" ]; then
echo "Nothing in the table"
else echo "$Result"

exit 0
fi

else echo "Incorrect input"
fi
exit 1