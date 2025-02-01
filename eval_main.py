import logging
from utils import generate, load_model, get_args, PROMPTS, TEMPLATES, MODELS
from support_fn import searching_wine, can_find_wines
from extractor_data import *
from component.NLU import NLU
from component.DM import DM
from component.NLG import NLG
from support_classes import History, Tracker

logger = logging.getLogger('Dialogue')
logger.setLevel(logging.DEBUG)

def selection_phrase(test_data, name_file, num_phrases=14):

    with open(f"template_dialogues/nlu/{name_file}.txt", "r", encoding="utf-8") as f1, open(f"template_dialogues/nlu/{name_file}_json.txt", "r", encoding="utf-8") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    list_ind = []
#    index = random.randint(0, len(lines1) - 1)
    for i in range(0, 5):  # Ogni esempio è su 2 righe consecutive
        list_ind.append(i)
        user_input = lines1[i].strip()  # Prima riga: frase utente
        phrase2 = lines2[i].strip()
        phrase2 = phrase2.replace('None', "'None'")
        if 'out_of_domain' in phrase2:
            ground_truth = {"intent": "out_of_domain"}
 #       else:
#            ground_truth = json.loads(phrase2.replace("'", "\""))  # Seconda riga: JSON
#        num = random.randint(0, len(lines1) - 1)
#        while num in list_ind:
#            num = random.randint(0, len(lines1) - 1)
#        index = num
        test_data.append({"user_input": user_input}) #, "ground_truth": ground_truth})

    return test_data

class Dialogue:
    def __init__(self, model, tokenizer, args, logger):
        self.tracker = Tracker(logger)
        self.history = History()
        self.nlu = NLU(self.history, model, tokenizer, args, logger)
        self.dm = DM(self.history, model, tokenizer, args, logger)
        self.nlg = NLG(self.history, model, tokenizer, args, logger)
        self.logger = logger

    def start(self):
        
        # exit the loop using CTRL+C
        test_data = []
        slots_nlu_pred = []
        intents_nl_pred = []
        action_dm_pred = []
        outputs_nlg = []
        test_data = selection_phrase(test_data, "input2")
        count = 0   
        for data in test_data:
            self.history.clear()
            print(self.history.get_history())
            count += 1
            print(f"\n\n---------\n{count}\n-------\n")     

            starting = PROMPTS["START"]
            self.history.add_msg(starting, 'assistant', 'init')
            print(data['user_input'])
            user_input = data['user_input']
#            ground_truth = data["ground_truth"]
#            ground_truth_intent = ground_truth["intent"]
            self.history.add_msg(user_input, 'user', 'input')
            slots_empty = 1
            action = ''

            if slots_empty == 0: self.history.update_number_last(2)
            else: self.history.update_number_last(5)
            
#            if (ground_truth_intent == 'wine_delivery'):
#                self.history.update_last_int('delivery')
            # get the NLU output
            infos = self.nlu(user_input, slots_empty)

            
            predicted_intent = infos.get("intent", "")
            predicted_slots = infos.get("slots", {})
            slots_nlu_pred.append(predicted_slots)
            intents_nl_pred.append(predicted_intent)

            intent, total_slots, full_slot = self.tracker.creation(infos, self.history, True)
            slots_empty = total_slots - full_slot

            self.logger.info(intent)
            can_search, _ = can_find_wines(self.tracker, self.history)
        
            # get the DM output
            action, arg, _ = self.dm(self.tracker, intent, can_search, action)
            self.logger.info(f'Action: {action}, Argument: {arg}')
            # print(f'Action: {action}, Argument: {arg}')

            action_dm_pred.append(f'Action: {action}, Argument: {arg}')

            
            if action == 'delivery_info':
                # print('in teoria creazione del Delivery')
                intent = {'intent': action}
                intent, _, _= self.tracker.creation(intent, self.history, False)
                can_search = False

            # get the NLG output + possible list 

            nlg_output = self.nlg(action, arg, intent, can_search, slots_empty == total_slots)
            self.history.add_msg(nlg_output, 'assistant', action)
            print(nlg_output)
            to_save = nlg_output
            if action == 'give_list':
                # print('The top three choices I find are:\n')
                list_wines, to_save = searching_wine(self.tracker, intent, to_save)
                if len(list_wines) == 0:
                    print('No wine respects the characteristics you want')
                    to_save = to_save + '\nNo wine respects the characteristics you want'
                    self.history.add_msg('No wine respects the characteristics you want', 'assistant', 'give_list')
                else:
                    for value in list_wines:
                        print(value)
                        to_save = to_save + f'\n{value}'
                        self.history.add_msg(value, 'assistant', 'give_list')
            outputs_nlg.append(to_save)
            self.history.clear()
        with open('4results_nlu_intents.txt', 'w') as f:
            #write items of intents_nl_pred and slots_nlu_pred: one item per line
            for i in range(len(intents_nl_pred)):
                f.write(f"{intents_nl_pred[i]}\n")
        with open('4results_nlu_slots.txt', 'w') as f:
            for i in range(len(slots_nlu_pred)):
                f.write(f"{slots_nlu_pred[i]}\n")

        with open('4results_dm.txt', 'w') as f:
            for i in range(len(action_dm_pred)):
                f.write(f"{action_dm_pred[i]}\n")
        
        with open('4results_nlg.txt', 'w') as f:
            for i in range(len(outputs_nlg)):
                f.write(f"{outputs_nlg[i]}\n")

def main():
    logging.basicConfig(filename="app1-eval-try.log", encoding="utf-8", filemode="a", level=logging.DEBUG)
    logger.info("Starting the dialogue")

    args = get_args()
    model, tokenizer = load_model(args)
    dg = Dialogue(model, tokenizer, args, logger)
    dg.start()
    print(dg.history.to_msg_history())

if __name__ == "__main__":
    main()

