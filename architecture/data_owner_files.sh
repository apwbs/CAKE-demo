python3 data_owner_files.py -hs
echo "✅ Data owner handshake done"
python3 data_owner_files.py -c -i $1 -p $2
echo "✅ Data owner cipher done"