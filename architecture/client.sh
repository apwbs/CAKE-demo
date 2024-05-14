message_id='14160621064142517685'
reader_address='0xC79d7CEF68F2B4b6eEBb19aCDe35455492d53D57'
slice_id='2995392129270261562'

python3 client.py --handshake --message_id $message_id --reader_address $reader_address
python3 client.py -gs --message_id $message_id --reader_address $reader_address 
python3 client.py -ad --message_id $message_id --reader_address $reader_address --slice_id $slice_id

#slice id: 6678072391299123667
#slice id: 13635621019063986383
#slice id: 10450506680882014878
#message id: 6780287944816327166