import ast
import json
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report


def normalize_slots(slots):
    return {k: (v if v not in ["", "null", None] else None) for k, v in slots.items()}

# Extract sections using string parsing
def extract_list(label, text):
    start = text.find(label) + len(label)
    end = text.find("\n\n", start)  # Assuming double newlines separate sections
    if end == -1:
        end = len(text)  # In case it's the last element
    list_str = text[start:end].strip()
    return ast.literal_eval(list_str)  # Convert string representation of list to actual list

def calculate_slot_metrics(slots_true, slots_pred):
    true_positive, false_positive, false_negative = 0, 0, 0

    for true_slots, pred_slots in zip(slots_true, slots_pred):
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

# Read the text file

name = 'evaluation5'

with open(f"{name}.txt", "r", encoding="utf-8") as file:
    data = file.read()

# Extracting data
intents_true = extract_list("Intents True:", data)
intents_pred = extract_list("Intents Predicted:", data)
slots_true = extract_list("Slots True:", data)
slots_pred = extract_list("Slots Predicted:", data)


# intents_true = intents_true[:-2]
# intents_pred = intents_pred[:-2]
# slots_true = slots_true[:-2]
# slots_pred = slots_pred[:-2]

slots_true = [normalize_slots(s) if s != {} else {} for s in slots_true]
slots_pred = [normalize_slots(s) if s != {} else {} for s in slots_pred]



for x in slots_pred:
    # remove the 'giving_list_wine': 'null'
    x.pop('giving_list_wine', None)

print(slots_pred)

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

with open(f"scores_nlu_{name}.txt", "w", encoding="utf-8") as f:
    f.write(f"Intent Accuracy: {intent_accuracy:.2f}\n")
    f.write("Intent Classification Report:\n")
    f.write(classification_report(intents_true, intents_pred))
    f.write(f"Slot Extraction Metrics : Precision={precision:.2f}, Recall={recall:.2f}, F1 Score={f1:.2f}\n")
    f.write(f"Overall Accuracy (Intent + Slots): {overall_accuracy:.2f}\n")

with open(f"scores_nlu_{name}.json", "w", encoding="utf-8") as f:
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
        "overall_accuracy": overall_accuracy
    }, f, ensure_ascii=False, indent=4)