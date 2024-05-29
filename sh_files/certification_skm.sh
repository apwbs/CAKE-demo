# Read public key of manufacter and suppliers
set -e

# READ PUBLIC KEY OF SKM
python3  ../src/certifier.py -o 1
echo "✅ Read public key of skm"