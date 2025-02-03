import ast
import json
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report


def normalize_slots(slots):
    #normalize for null values
    #normilize if value = True 
    norm = {}
    for k, v in slots.items():
        if v in ["", '', "null", None]:
            norm[k] = None
        elif v == "True" or v == "true" or v == True or v == "yes" or v == "Yes":
            norm[k] = True
        elif v == "False" or v == "false" or v == False or v == "no" or v == "No":
            norm[k] = False
        else:
            norm[k] = v

    return norm

# Extract sections using string parsing
def extract_list(name):
    with open(f"{name}.txt", "r", encoding="utf-8") as f:
        text = f.readlines()
    # elimine '\n' in each line
    text = [line.strip() for line in text]
    return text[:100]

def extract_slots(name):
    with open(f"{name}.txt", "r", encoding="utf-8") as f:
        text = [line.strip() for line in f if line.strip()]  # Rimuove spazi e righe vuote
    
    slots_list = []
    for line in text:
        try:
            slots_list.append(ast.literal_eval(line))  # Converte la stringa in dizionario
        except (SyntaxError, ValueError):
            print(f"⚠️ Errore nel parsing della riga: {line}")
            slots_list.append({})  # Se il parsing fallisce, aggiunge un dizionario vuoto
    
    return slots_list

def calculate_slot_metrics(slots_true, slots_pred):
    true_positive, false_positive, false_negative = 0, 0, 0

    for true_slots, pred_slots in zip(slots_true, slots_pred):
        true_slots = normalize_slots(true_slots)
        pred_slots = normalize_slots(pred_slots)
        for slot, value in true_slots.items():
            if slot in pred_slots and pred_slots[slot] == value:
                true_positive += 1  # Slot corretto
            elif slot in pred_slots and pred_slots[slot] != value:
                false_positive += 1  # Slot errato
            else:
                false_negative += 1  # Slot mancante

    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1

def calculate_slot_accuracy(slots_true, slots_pred):
    correct_slots = sum(
        sum(1 for slot, value in true_slots.items() if slot in pred_slots and pred_slots[slot] == value)
        for true_slots, pred_slots in zip(slots_true, slots_pred)
    )
    total_slots = sum(len(s) for s in slots_true)  # Numero totale di slot etichettati
    return correct_slots / total_slots if total_slots > 0 else 0


def calculate_overall_accuracy(intents_true, intents_pred, slots_true, slots_pred):
    correct = sum(1 for i in range(len(intents_true)) if 
                  intents_true[i] == intents_pred[i] and slots_true[i] == slots_pred[i])
    return correct / len(intents_true)

def calculate_partial_slot_accuracy(slots_true, slots_pred, threshold=0.8):
    """
    Calcola l'accuracy considerando corrette le predizioni con almeno l'80% di slot corretti.
    """
    correct_predictions = 0  # Conta le predizioni con almeno il threshold% degli slot corretti
    total_predictions = len(slots_true)  # Numero totale di predizioni

    for true_slots, pred_slots in zip(slots_true, slots_pred):
        true_slots = normalize_slots(true_slots)
        pred_slots = normalize_slots(pred_slots)

        # Conta solo gli slot presenti nel ground truth
        relevant_slots = {k: v for k, v in true_slots.items() if v is not None}
        total_slots = len(relevant_slots)

        if total_slots == 0:
            continue  # Salta i casi senza slot da valutare

        # Conta gli slot corretti
        correct_slots = sum(1 for slot, value in relevant_slots.items() if pred_slots.get(slot) == value)

        # Se almeno l'80% degli slot è corretto, consideriamo la predizione giusta
        if correct_slots / total_slots >= threshold:
            correct_predictions += 1

    return correct_predictions / total_predictions if total_predictions > 0 else 0

# Read the text file

# Extracting data
intents_true = extract_list('truth_nlu_intent')
print(len(intents_true))
intents_pred = extract_list("results_nlu_intents")
slots_true = extract_slots("truth_nlu_slots")
slots_pred = extract_slots("results_nlu_slots")

# Accuracy sugli intents
intent_accuracy = accuracy_score(intents_true, intents_pred)
print(f"Intent Accuracy: {intent_accuracy:.2f}")

# Precision, Recall, F1 sugli intents
print("Intent Classification Report:")
print(classification_report(intents_true, intents_pred))

intent_precision, intent_recall, intent_f1, _ = precision_recall_fscore_support(
    intents_true, intents_pred, average="weighted"
)

# Calcolare metriche sugli slots
precision, recall, f1 = calculate_slot_metrics(slots_true, slots_pred)
slot_accuracy = calculate_slot_accuracy(slots_true, slots_pred)

print(f"Slot Extraction Metrics : Precision={precision:.2f}, Recall={recall:.2f}, F1 Score={f1:.2f}")

overall_accuracy = calculate_overall_accuracy(intents_true, intents_pred, slots_true, slots_pred)
print(f"Overall Accuracy (Intent + Slots): {overall_accuracy:.2f}")

partial_slot_accuracy = calculate_partial_slot_accuracy(slots_true, slots_pred, threshold=0.8)
print(f"Slot Accuracy Parziale (≥80% slot corretti): {partial_slot_accuracy:.2f}")


with open(f"scores_nlu_test.txt", "w", encoding="utf-8") as f:
    f.write(f"Intent Accuracy: {intent_accuracy:.2f}\n")
    f.write("Intent Classification Report:\n")
    f.write(classification_report(intents_true, intents_pred))
    f.write(f"Slot Extraction Metrics : Precision={precision:.2f}, Recall={recall:.2f}, F1 Score={f1:.2f}\n")
    f.write(f"Overall Accuracy (Intent + Slots): {overall_accuracy:.2f}\n")
    f.write(f"Slot Accuracy Parziale (≥80% slot corretti): {partial_slot_accuracy:.2f}\n")

with open(f"scores_nlu_test.json", "w", encoding="utf-8") as f:
    json.dump({
        "intent": {
            "accuracy": intent_accuracy,
            "precision": intent_precision,
            "recall": intent_recall,
            "f1": intent_f1,
        },
        "slots": {
            "accuracy": slot_accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        },
        "overall_accuracy": overall_accuracy,
        "partial_slot_accuracy": partial_slot_accuracy,
    }, f, ensure_ascii=False, indent=4)
