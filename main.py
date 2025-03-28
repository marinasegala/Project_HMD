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


class Dialogue:
    def __init__(self, model, tokenizer, args, logger):
        self.tracker = Tracker(logger)
        self.history = History()
        self.nlu = NLU(self.history, model, tokenizer, args, logger)
        self.dm = DM(self.history, model, tokenizer, args, logger)
        self.nlg = NLG(self.history, model, tokenizer, args, logger)
        self.logger = logger

    def start(self):
        starting = PROMPTS["START"]
        self.history.add_msg(starting, 'assistant', 'init')
        user_input = input(starting + '\n')
        self.history.add_msg(user_input, 'user', 'input')
        slots_empty = 1
        action = ''
        # exit the loop using CTRL+C
        while True:
            if slots_empty == 0: self.history.update_number_last(2)
            else: self.history.update_number_last(5)
            
            # get the NLU output
            infos = self.nlu(user_input, slots_empty)

            intent, total_slots, full_slot = self.tracker.creation(infos, self.history, True)
            slots_empty = total_slots - full_slot

            self.logger.info(intent)
            can_search, _ = can_find_wines(self.tracker, self.history)
        
            # get the DM output
            action, arg, _ = self.dm(self.tracker, intent, can_search, action)
            self.logger.info(f'Action: {action}, Argument: {arg}')
            # print(f'Action: {action}, Argument: {arg}')
            
            if action == 'delivery_info':
                # print('in teoria creazione del Delivery')
                intent = {'intent': action}
                intent, _, _= self.tracker.creation(intent, self.history, False)
                can_search = False

            # get the NLG output + possible list 

            nlg_output = self.nlg(action, arg, intent, can_search, slots_empty == total_slots)
            self.history.add_msg(nlg_output, 'assistant', action)
            print(nlg_output)

            if action == 'give_list':
                to_save = ''
                # print('The top three choices I find are:\n')
                list_wines,to_save = searching_wine(self.tracker, intent, to_save)
                if len(list_wines) == 0:
                    print('No wine respects the characteristics you want')
                    self.history.add_msg_complete('No wine respects the characteristics you want')
                else:
                    for value in list_wines:
                        print(value)
                        to_save = to_save + '\n' + value.convert_to_string()
                    self.history.add_msg_complete(to_save)

            other_int = self.history.get_other_int()
            if other_int > 0 and (slots_empty == 0 or action == 'give_list'):
                action = 'new_intent'
                arg = other_int[0]
                slots_empty = 0
                #remove other_int[0] from the list
                self.history.remove_other_int()
                nlg_output = self.nlg(action, arg, '', False, False)
                self.history.add_msg(nlg_output, 'assistant', action)
                print(nlg_output)
    
            user_input = input()
            self.history.add_msg(user_input, 'user', 'input')

def main():
    logging.basicConfig(filename="prova2.log", encoding="utf-8", filemode="a", level=logging.DEBUG)
    logger.info("Starting the dialogue")

    args = get_args()
    model, tokenizer = load_model(args)
    dg = Dialogue(model, tokenizer, args, logger)
    dg.start()
    print(dg.history.to_msg_history())

if __name__ == "__main__":
    main()
