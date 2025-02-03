# 📂 File di input
actions_file = "truth_dm.txt"  # Il file con le azioni DM
arguments_file = "truth_nlu_intent.txt"  # Il file con gli intent corrispondenti

# 📥 Leggere i file
with open(actions_file, "r", encoding="utf-8") as f:
    actions = f.readlines()

with open(arguments_file, "r", encoding="utf-8") as f:
    arguments = f.readlines()

# 🛠️ Pulire le liste (rimuovere spazi e newline)
actions = [line.strip() for line in actions]
arguments = [line.strip() for line in arguments]

# 🚀 Aggiungere gli Argument mancanti
updated_actions = []
arg_index = 0  # Indice per scorrere il file degli argument

for line in actions:
    if ", Argument:" not in line:  # Se manca l'argomento, aggiungilo
        line = f"{line}, Argument: {arguments[arg_index]}"
        arg_index += 1
    updated_actions.append(line)

# ✍️ Scrivere il file aggiornato
output_file = "updated_actions.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(updated_actions))

print(f"✅ File aggiornato salvato in {output_file}")
