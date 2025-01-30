# names = ['out_of_domain', 'wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'choosing_food', 'wine_ordering', 'delivery']

# list1 = []
# list2 = []
# list3 = []
# list4 = []
# list5 = []
# list6 = []
# list7 = []
# list8 = []

# for index, name_file in enumerate(names):
#     with open(f"template_dialogues/{name_file}.txt", "r", encoding="utf-8") as f1, open(f"template_dialogues/{name_file}_json.txt", "r", encoding="utf-8") as f2:
#         lines1 = f1.readlines()
#         lines2 = f2.readlines()


import os
import random

# Cartella contenente i file
folder_path = "."  # Modifica se i file si trovano in un'altra cartella

# Lista dei file di testo e JSON
txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt") and "_json" not in f]
json_files = [f for f in os.listdir(folder_path) if f.endswith(".txt") and "_json" in f]



# Controllo che i file JSON corrispondenti esistano
txt_files = [f for f in txt_files if f.replace(".txt", "_json.txt") in json_files]

# Liste per contenere tutte le righe estratte
intents = []
intents_json = []

# Leggere le prime 14 righe di ogni coppia di file
for txt_file in txt_files:
    # Trovare il file JSON corrispondente
    json_file = txt_file.replace(".txt", "_json.txt")
    
    with open(os.path.join(folder_path, txt_file), "r", encoding="utf-8") as f_txt, open(os.path.join(folder_path, json_file), "r", encoding="utf-8") as f_json:
        
        txt_lines = f_txt.readlines()
        json_lines = f_json.readlines()
        
        # Prendere le prime 14 righe, se ci sono abbastanza righe
        num_lines = min(14, len(txt_lines), len(json_lines))
        
        intents.extend(txt_lines[:num_lines])
        intents_json.extend(json_lines[:num_lines])

# Mischiare mantenendo la corrispondenza tra le righe
combined = list(zip(intents, intents_json))
random.shuffle(combined)

# Separare di nuovo le liste dopo la mischiatura
intents, intents_json = zip(*combined)

# Scrivere nei file finali
with open("intents.txt", "w", encoding="utf-8") as f_intents, open("intents_json.txt", "w", encoding="utf-8") as f_json:
    
    f_intents.writelines(intents)
    f_json.writelines(intents_json)

print("File 'intents.txt' e 'intents_json.txt' creati con successo!")
