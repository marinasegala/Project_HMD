import random
import json
# Load the text file lines
with open("wine_details.txt", "r", encoding="utf-8") as f1, open("wine_details_json.txt", "r", encoding="utf-8") as f2:
    lines1 = f1.readlines()
    lines2 = f2.readlines()

# Pick a random index
index = random.randint(0, len(lines1) - 1)

# Get the corresponding lines
phrase1 = lines1[index].strip()
phrase2 = lines2[index].strip()

phrase2 = phrase2.replace('None', "'None'")

phrase3 = json.loads(phrase2.replace("'", "\""))

print(phrase1)
print(phrase2)
print(type(phrase3))