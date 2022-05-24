# IN="$(python3 -V)"
# versions=$(echo $IN | tr "." "\n")
# IFS=' '
# read -ra VALS <<< "$versions"

# for addr in $versions
# do
#     echo "> [$addr]"
# done

python3 ./db/database_migration.py