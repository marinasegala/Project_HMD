# Creiamo due file separati: uno per gli intent e uno per i valori degli slot.

# Contenuto originale del file
with open("truth_nlu_json.txt", "r") as f:
    data = f.read().splitlines()

# Estraiamo gli intent e i valori degli slot: data[i] è una striga

intent_list = []
slots_values_list = []

for i in range(len(data)):
    # Estraiamo l'intent
    intent = data[i].split('intent')[1].split(',')[0].replace('"', "").replace("'", "").replace(":", "")
    intent_list.append(intent.strip())

    # Estraiamo i valori degli slot
    slots = data[i].split('slot')[1].split('{')[1][:-1]
    slots = '{'+slots
    slots_values_list.append(slots)
   

# Percorsi dei file
intent_file_path = "truth_nlu_intent.txt"
slots_file_path = "truth_nlu_slots.txt"

# Scriviamo i file
with open(intent_file_path, "w") as f:
    f.write("\n".join(intent_list))

with open(slots_file_path, "w") as f:
    f.write("\n".join(slots_values_list))
