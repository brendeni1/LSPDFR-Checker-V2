import json
import os

# Clear the console after run.
os.system('cls')

# Function to get hash from the hashes JSON.
def getHash(hash, hashes):
    carName = hashes.get(str(hash))
    if not carName:
        return '(Unknown Hash)'
    return carName


# Ask the user for the hash.
hashOld = input("Input the car's hash: ")

if hashOld.startswith("0x"):
    hash = int(hashOld, 16)
else:
    raise ValueError("INVALID HASH. Please only provide hashes in hex 16 form. Example: '0xb779a091'")
    

# Clear the console.
os.system('cls')

# Open the hashes file.
with open("./hashes/hashes.json") as hashes:
    hashes = json.load(hashes)

# Call the function to get the car's name.
carName = getHash(hash, hashes)

print(f"{hashOld} ({hash}) = {carName}\n")
