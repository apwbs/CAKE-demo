python3 data_owner.py -hs
echo "✅ Data owner handshake done"
python3 data_owner.py -c -d $1 -e $2 -p $3
echo "✅ Data owner cipher done"