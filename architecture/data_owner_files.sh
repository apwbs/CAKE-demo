#!/bin/sh

# Initialize variables
action="cipher"
input=""
policies=""

# Parse command-line arguments
while [ $# -gt 0 ]; do
  key="$1"
  case $key in
    -c|--cipher)
      action="cipher"
      shift # past argument
      ;;
    -i|--input)
      input="$2"
      shift # past argument
      shift # past value
      ;;
    -p|--policies)
      policies="$2"
      shift # past argument
      shift # past value
      ;;
    *)
      echo "Unknown option $1"
      exit 1
      ;;
  esac
done

# Check if input folder exists
if [ -n "$input" ] && [ ! -d "$input" ]; then
  echo "Input folder '$input' does not exist"
  exit 1
fi

# Check if policies file exists
if [ -n "$policies" ] && [ ! -f "$policies" ]; then
  echo "Policies file '$policies' does not exist"
  exit 1
fi

# Run the Python script with the provided arguments
if [ "$action" = "cipher" ]; then
  # Automatically perform handshake before ciphering
  python3 data_owner_files.py -hs
  echo "✅ Data owner handshake done"
  python3 data_owner_files.py -c -i "$input" -p "$policies"
  echo "✅ Data owner cipher done"
fi
