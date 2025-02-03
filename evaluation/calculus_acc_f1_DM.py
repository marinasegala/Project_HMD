from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support
import json
def normalize_action(action_line):
    """Normalizza una riga d'azione per separare Action e Argument"""
    action = action_line.split("Action: ")[1]
    action = action.split(",")[0]
    if ", Argument: " in action_line:
        if len(action_line.split("Argument: ")) > 1:
            argument = action_line.split("Argument: ")[1]
            return action.strip(), argument.strip()
    return action.strip(), ""  # Se manca Argument, consideriamo vuoto

def calculate_dm_metrics(true_actions, pred_actions):
    """Calcola accuracy, precision, recall e F1-score per le azioni del DM"""
    
    correct_actions = 0
    correct_arguments = 0
    total = len(true_actions)
    
    action_true_labels = []
    action_pred_labels = []
    argument_true_labels = []
    argument_pred_labels = []
    index = 0
    for true_line, pred_line in zip(true_actions, pred_actions):
        true_action, true_argument = normalize_action(true_line)
        pred_action, pred_argument = normalize_action(pred_line)
        index += 1
        # 📌 Valutazione delle azioni
        action_true_labels.append(true_action)
        action_pred_labels.append(pred_action)
        argument_true_labels.append(true_argument)
        argument_pred_labels.append(pred_argument)

        if true_action == pred_action:
            print(f"Index: {index}")
            correct_actions += 1

            # 📌 Valutazione degli argomenti
            if true_argument == "" or true_argument == pred_argument or (pred_action == "provide_list" and pred_argument == ""):
                correct_arguments += 1  # Accettiamo qualsiasi valore se il ground truth è vuoto

    # 📊 Calcolo delle metriche
    action_accuracy = correct_actions / total
    argument_accuracy = correct_arguments / total
    overall_accuracy = sum(1 for t, p in zip(true_actions, pred_actions) if normalize_action(t) == normalize_action(p)) / total

    precision, recall, f1, _ = precision_recall_fscore_support(action_true_labels, action_pred_labels, average="weighted")

    #calculate precision, recall, f1 for the arguments
    argument_precision, argument_recall, argument_f1, _ = precision_recall_fscore_support(argument_true_labels, argument_pred_labels, average="weighted")

    # Genera il classification report per le azioni
    action_classification_report = classification_report(action_true_labels, action_pred_labels)

    with open(f"score/scores_dm_test.txt", "w", encoding="utf-8") as f:
        f.write(f"Action Accuracy: {action_accuracy:.2f}\n")
        f.write(f"Argument Accuracy: {argument_accuracy:.2f}\n")
        f.write(f"Overall Accuracy (Action + Argument): {overall_accuracy:.2f}\n")
        f.write(f"Action Precision: {precision:.2f}\n")
        f.write(f"Action Recall: {recall:.2f}\n")
        f.write(f"Action F1-score: {f1:.2f}\n")
        f.write("\nAction Classification Report:\n")
        f.write(action_classification_report)  # Aggiungi il classification report delle azioni
        f.write(f"\nArgument Precision: {argument_precision:.2f}\n")
        f.write(f"Argument Recall: {argument_recall:.2f}\n")
        f.write(f"Argument F1-score: {argument_f1:.2f}\n")

    with open(f"score/scores_dm_test.json", "w", encoding="utf-8") as f:
        json.dump({
            "actions": {
                "accuracy": action_accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1,
                # "classification_report": action_classification_report,  # Aggiungi il classification report delle azioni
            },
            "arguments": {
                "accuracy": argument_accuracy,
                "precision": argument_precision,
                "recall": argument_recall,
                "f1": argument_f1,
            },
            "overall_accuracy": overall_accuracy,
        }, f, ensure_ascii=False, indent=4)


# 📂 Caricare le azioni predette e reali
with open("truth_dm.txt", "r", encoding="utf-8") as f:
    true_actions = [line.strip() for line in f if line.strip()]
    true_actions

with open("results_dm.txt", "r", encoding="utf-8") as f:
    pred_actions = [line.strip() for line in f if line.strip()]

# 🚀 Calcolare le metriche
dm_results = calculate_dm_metrics(true_actions[:100], pred_actions[:100])
print("Calcolo delle metriche completato!")



