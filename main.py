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
        self.dm = DM(model, tokenizer, args, logger)
        self.nlg = NLG(self.history, model, tokenizer, args, logger)
        self.logger = logger

    def start(self):
        starting = PROMPTS["START"]
        self.history.add_msg(starting, 'assistant', 'init')
        user_input = input(starting + '\n')
        self.history.add_msg(user_input, 'user', 'input')
        all_slots_filled = False
        # exit the loop using CTRL+C
        while True:
            if all_slots_filled: self.history.update_number_last(2)
            else: self.history.update_number_last(5)
            
            # get the NLU output
            infos = self.nlu(user_input, all_slots_filled)

            intent, all_slots_filled = self.tracker.creation(infos, self.history, True)

            self.logger.info(intent)
            can_search, _ = can_find_wines(self.tracker, self.history)
        
            # get the DM output
            action, arg = self.dm(self.tracker, intent, can_search)
            self.logger.info(f'Action: {action}, Argument: {arg}')
            # print(f'Action: {action}, Argument: {arg}')
            
            if action == 'delivery_info': #TODO DOMANDA
                # print('in teoria creazione del Delivery')
                intent = {'intent': action}
                intent, _ = self.tracker.creation(intent, self.history, False)
                can_search = False

            # get the NLG output + possible list 
            nlg_output = self.nlg(action, arg, intent, can_search)
            self.history.add_msg(nlg_output, 'assistant', action)
            print(nlg_output)

            #TODO - LISTA EMESSA SE - MAGGIOR PARTE CAMPI PIENI O UTENTE LO CHIEDE 
            if action == 'provide_list':
                list_to_print = 'The wines that match the information you provided are:'
                list_wines = searching_wine(self.tracker, intent)
                for value in list_wines:
                    list_to_print = list_to_print + '\n\t' + value
                print(list_to_print)

            user_input = input()
            self.history.add_msg(user_input, 'user', 'input')

def main():
    logging.basicConfig(filename="app.log", encoding="utf-8", filemode="a", level=logging.DEBUG)
    logger.info("Starting the dialogue")

    args = get_args()
    model, tokenizer = load_model(args)
    dg = Dialogue(model, tokenizer, args, logger)
    dg.start()
    print(dg.history.to_msg_history())

if __name__ == "__main__":
    main()
