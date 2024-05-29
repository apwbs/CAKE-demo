# Go to the directory where the databases are stored
cd ../databases

# Create attribute_certifier database
cd attribute_certifier
sqlite3 attribute_certifier.db < ../commands.sql
echo "attribute_certifier.db created (1/5)"

# Create data_owner database
cd ../data_owner
sqlite3 data_owner.db < ../commands.sql
echo "data_owner.db created (2/5)"

# Create reader database
cd ../reader
sqlite3 reader.db < ../commands.sql
echo "reader.db created (3/5)"

# Create sdm database
cd ../sdm
sqlite3 sdm.db < ../commands.sql
echo "sdm.db created (4/5)"

# Create skm database
cd ../skm
sqlite3 skm.db < ../commands.sql
echo "skm.db created (5/5)"