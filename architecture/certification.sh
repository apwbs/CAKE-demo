# Read public key of manufacter and suppliers
set -e

# READ PUBLIC KEY OF MANUFACTURER AND SUPPLIERS
python3 certifier.py -o 0 --reader 'A'
echo "✅ Read public key of A"
python3  certifier.py -o 0  --reader 'B'
echo "✅ Read public key of B"
python3  certifier.py -o 0  --reader 'C'
echo "✅ Read public key of C"

 # READ PUBLIC KEY OF SKM
python3  certifier.py -o 1
echo "✅ Read public key of skm"

# CERTIFY ATTRIBUTES
python3  certifier.py -o 2
echo "✅ Attribute certifier done"