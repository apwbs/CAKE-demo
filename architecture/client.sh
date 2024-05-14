message_id='9513861866848708097'
reader_address='0xeF4B867984daFD8cbAb41fac185195c18A6ae6Ea'
slice_id='18033260125111666087'

python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -ad --message_id $message_id --reader_address $reader_address --slice_id $slice_id

#slice id: 6678072391299123667
#slice id: 13635621019063986383
#slice id: 10450506680882014878
#message id: 6780287944816327166