from component.NLU import NLU
from utils import get_args, load_model, PROMPTS
from support_classes import History, Tracker
import logging
import random
import json

logger = logging.getLogger('Dialogue')
logger.setLevel(logging.DEBUG)


intents_true, intents_pred = [], []
slots_true, slots_pred = [], []

def selection_phrase(test_data, name_file, num_phrases=14):

    with open(f"template_dialogues/{name_file}.txt", "r", encoding="utf-8") as f1, open(f"template_dialogues/{name_file}_json.txt", "r", encoding="utf-8") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    list_ind = []
#    index = random.randint(0, len(lines1) - 1)
    for i in range(0,100):  # Ogni esempio è su 2 righe consecutive
        list_ind.append(i)
        user_input = lines1[i].strip()  # Prima riga: frase utente
        phrase2 = lines2[i].strip()
        phrase2 = phrase2.replace('None', "'None'")
        if 'out_of_domain' in phrase2:
            ground_truth = {"intent": "out_of_domain"}
        else:
            ground_truth = json.loads(phrase2.replace("'", "\""))  # Seconda riga: JSON
#        num = random.randint(0, len(lines1) - 1)
#        while num in list_ind:
#            num = random.randint(0, len(lines1) - 1)
#        index = num
        test_data.append({"user_input": user_input, "ground_truth": ground_truth})
#        print(user_input)
#        print(ground_truth)
    return test_data

def evaluate_nlu(nlu, test_data):
    """
    Evaluate NLU component on a test dataset.

    Args:
        nlu: NLU component instance.
        test_data: List of dictionaries with "user_input", "expected_intent", and "expected_slots".

    Returns:
        A dictionary with evaluation metrics for intents and slots.
    """
    

    return 

class Dialogue:
    def __init__(self, model, tokenizer, args, logger):
        self.tracker = Tracker(logger)
        self.history = History()
        self.nlu = NLU(self.history, model, tokenizer, args, logger)
        # self.dm = DM(self.history, model, tokenizer, args, logger)
        # self.nlg = NLG(self.history, model, tokenizer, args, logger)
        self.logger = logger

    def start(self):
        test_data = []
        test_data = selection_phrase(test_data, "intents")
#        test_data = selection_phrase(test_data, "wine_details", 15)
#        test_data = selection_phrase(test_data, "wine_origin", 14)
#        test_data = selection_phrase(test_data, "wine_production", 15)
#        test_data = selection_phrase(test_data, "wine_conservation", 14)
#        test_data = selection_phrase(test_data, "wine_paring", 14)
#        test_data = selection_phrase(test_data, "wine_ordering", 14)
#        test_data = selection_phrase(test_data, "delivery", 14)

        # starting = PROMPTS["START"]
        # self.history.add_msg(starting, 'assistant', 'init')
#        user_input = input(starting + '\n')
#        self.history.add_msg(user_input, 'user', 'input')
        slots_empty = 1
        action = ''
        # exit the loop using CTRL+C
        count = 0
        for sample in test_data:
            count += 1
            print(f"\n\n---------\n{count}\n-------\n")
            user_input = sample["user_input"]
            ground_truth = sample["ground_truth"]
            ground_truth_intent = ground_truth["intent"]
            ground_truth_slots = ground_truth["slots"] if "slots" in ground_truth else []

            self.history.clear()
            starting = PROMPTS["START"]
            self.history.add_msg(starting, 'assistant', 'init')
            if (ground_truth_intent == 'wine_delivery'):
                self.history.update_last_int('delivery')
            prediction = self.nlu(user_input, 0)
            # intent, total_slots, full_slot = self.tracker.creation(prediction, self.history, True)
            # slots_empty = total_slots - full_slot  # Se tutti i valori sono vuoti, consideriamo slots_empty=True

            # Estrarre intent e slots previsti
            predicted_intent = prediction.get("intent", "")
            predicted_slots = prediction.get("slots", {})

            # Salvare per valutazione
            intents_true.append(ground_truth_intent)
            intents_pred.append(predicted_intent)
            slots_true.append(ground_truth_slots)
            slots_pred.append(predicted_slots)
            # intents_true, intents_pred, slots_true, slots_pred = evaluate_nlu(self.nlu, test_data)

        #save intents_true, intents_pred, slots_true, slots_pred in a file
        with open("evaluation3.txt", "w", encoding="utf-8") as f:
            f.write(f"Intents True: \n{intents_true}\n\n")
            f.write(f"Intents Predicted: \n{intents_pred}\n\n")
            f.write(f"Slots True:\n {slots_true}\n\n")
            f.write(f"Slots Predicted: \n{slots_pred}")

        with open("evaluation3.json", "w", encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False, indent=4)

        print('OK')

            # Accuracy sugli intents
            # intent_accuracy = accuracy_score(intents_true, intents_pred)
            # print(f"Intent Accuracy: {intent_accuracy:.2f}")

            # # Precision, Recall, F1 sugli intents
            # print("Intent Classification Report:")
            # print(classification_report(intents_true, intents_pred))

            # # intent, total_slots, full_slot = self.tracker.creation(infos, self.history, True)
            # # slots_empty = total_slots - full_slot

            # # Calcolare metriche sugli slots
            # precision, recall, f1 = calculate_slot_metrics(slots_true, slots_pred)
            # print(f"Slot Extraction Metrics : Precision={precision:.2f}, Recall={recall:.2f}, F1 Score={f1:.2f}") 

def main():
    logging.basicConfig(filename="eval.log", encoding="utf-8", filemode="a", level=logging.DEBUG)
    logger.info("Starting the dialogue")

    args = get_args()
    model, tokenizer = load_model(args)
    dg = Dialogue(model, tokenizer, args, logger)
    dg.start()
    print(dg.history.to_msg_history())

if __name__ == "__main__":
    main()
