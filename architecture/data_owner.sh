python3 data_owner.py -hs -s 'MANUFACTURER'
echo "✅ Data owner handshake done"
python3 data_owner.py -c -d $1 -e $2 -p $3 -s 'MANUFACTURER'
echo "✅ Data owner cipher done"