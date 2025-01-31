from component.NLU import NLU
from component.DM import DM
from utils import get_args, load_model, PROMPTS
from support_classes import History, Tracker
import logging
import random
import json
from support_fn import can_find_wines

logger = logging.getLogger('Dialogue')
logger.setLevel(logging.DEBUG)


intents_true, intents_pred = [], []
slots_true, slots_pred = [], []

def selection_phrase(test_data, name_file):

    with open(f"template_dialogues/nlu/{name_file}.txt", "r", encoding="utf-8") as f1, open(f"template_dialogues/nlu/{name_file}_json.txt", "r", encoding="utf-8") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    list_ind = []
    for i in range(0,100):
        list_ind.append(i)
        user_input = lines1[i].strip() 
        phrase2 = lines2[i].strip()
        phrase2 = phrase2.replace('None', "'None'")
        if 'out_of_domain' in phrase2:
            ground_truth = {"intent": "out_of_domain"}
        else:
            ground_truth = json.loads(phrase2.replace("'", "\""))  
            
        test_data.append({"user_input": user_input, "ground_truth": ground_truth})

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
        self.dm = DM(self.history, model, tokenizer, args, logger)
        # self.nlg = NLG(self.history, model, tokenizer, args, logger)
        self.logger = logger

    def start(self):
        test_data = []
        test_data = selection_phrase(test_data, "intents")
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
            # ground_truth_slots = ground_truth["slots"] if "slots" in ground_truth else []

            self.history.clear()
            starting = PROMPTS["START"]
            self.history.add_msg(starting, 'assistant', 'init')
            if (ground_truth_intent == 'wine_delivery'):
                self.history.update_last_int('delivery')
            
            infos = self.nlu(user_input, 0)
            intent, total_slots, full_slot = self.tracker.creation(infos, self.history, True)
            
            can_search, _ = can_find_wines(self.tracker, self.history)
        
            # get the DM output
            action, arg, ret = self.dm(self.tracker, intent, can_search, action)
            with open("action_predict.txt", "a") as f:
                f.write(f"{action}({arg})\n")
            with open("json_after_dm.txt", "a") as f:
                f.write(f"{ret}\n")
            
            # Estrarre intent e slots previsti
        #     predicted_intent = prediction.get("intent", "")
        #     predicted_slots = prediction.get("slots", {})

        #     # Salvare per valutazione
        #     intents_true.append(ground_truth_intent)
        #     intents_pred.append(predicted_intent)
        #     slots_true.append(ground_truth_slots)
        #     slots_pred.append(predicted_slots)
        #     # intents_true, intents_pred, slots_true, slots_pred = evaluate_nlu(self.nlu, test_data)

        # #save intents_true, intents_pred, slots_true, slots_pred in a file
        # with open("evaluation3.txt", "w", encoding="utf-8") as f:
        #     f.write(f"Intents True: \n{intents_true}\n\n")
        #     f.write(f"Intents Predicted: \n{intents_pred}\n\n")
        #     f.write(f"Slots True:\n {slots_true}\n\n")
        #     f.write(f"Slots Predicted: \n{slots_pred}")

        # with open("evaluation3.json", "w", encoding="utf-8") as f:
        #     json.dump(test_data, f, ensure_ascii=False, indent=4)

        print('OK')

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
