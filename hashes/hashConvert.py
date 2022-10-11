import json
import os

# Clear the console after run.
os.system('cls')

# Function to get hash from the hashes JSON.
def getHash(hash, hashes):
    carName = hashes.get(hash)
    if not carName:
        return '(Unknown Hash)'
    return carName


# Ask the user for the hash.
hash = input("Input the car's hash: ")

# Clear the console.
os.system('cls')

# Open the hashes file.
with open("./hashes.json") as hashes:
    hashes = json.load(hashes)

# Call the function to get the car's name.
carName = getHash(hash, hashes)

print(f"{hash} = {carName}\n")
