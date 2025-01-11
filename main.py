import logging
from utils import generate, load_model, get_args, PROMPTS, TEMPLATES, MODELS
from support_fn import searching_wine
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
        self.nlg = NLG(self.history, model, tokenizer, args)

    def start(self):
        starting = PROMPTS["START"]
        self.history.add_msg(starting, 'assistant', 'init')
        user_input = input(starting + '\n')
        self.history.add_msg(user_input, 'user', 'input')

        # exit the loop using CTRL+C
        while True:
            
            # get the NLU output
            infos = self.nlu(user_input)
            print(f"NLU: {infos}")
            intent = self.tracker.update(infos)

            logger.info(intent)
            #TODO possible_wine_list = searching_wine(self.tracker, intent)

            # get the DM output
            action, arg = self.dm(self.tracker, intent)
            logger.info(f'Action: {action}, Argument: {arg}')
            
            #TODO - FINIRE DI SISTEMARE IL DM - ESTARRE CORRETTAMENTE LE AZIONI E GLI ARGOMENTI
            
            # get the NLG output
            nlg_output = self.nlg(action, arg)
            self.history.add_msg(nlg_output, 'assistant', action)
            
            user_input = input(nlg_output + '\n')
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
