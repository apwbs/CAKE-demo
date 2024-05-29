#!/bin/sh

# Initialize variables
reader_address=""
message_id=""
slice_id=""
output_folder=""

# Parse command-line arguments
while [ $# -gt 0 ]; do
  key="$1"
  case $key in
    --reader_address)
      reader_address="$2"
      shift # past argument
      shift # past value
      ;;
    --message_id)
      message_id="$2"
      shift # past argument
      shift # past value
      ;;
    --slice_id)
      slice_id="$2"
      shift # past argument
      shift # past value
      ;;
    --output_folder)
      output_folder="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

# Check if mandatory arguments are provided
if [ -z "$reader_address" ] || [ -z "$message_id" ] || [ -z "$slice_id" ] || [ -z "$output_folder" ]; then
  echo "Usage: $0 --reader_address <reader_address> --message_id <message_id> --slice_id <slice_id> --output_folder <output_folder>"
  exit 1
fi

# Run the commands with the provided arguments
python3 ../src/client.py --handshake --reader_address "$reader_address"
python3 ../src/client.py -gs --message_id "$message_id" --reader_address "$reader_address"
python3 ../src/client.py -af --message_id "$message_id" --reader_address "$reader_address" --slice_id "$slice_id" --output_folder "$output_folder"
