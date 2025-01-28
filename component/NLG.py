from utils import PROMPTS, generate
from support_fn import searching_wine
class NLG():
    def __init__(self, history, model, tokenizer, args, logger):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        self.logger = logger
        pass

    def __call__(self, action, argument, intent, possible_list, slots_empty):
        last_int = self.history.last_iterations()
        
        nlg_text =  f"{action}({argument})\n" + last_int 

        #get the 
        if slots_empty > 0 and action == 'request_info' and intent in ['wine_details', 'wine_origin', 'wine_production', 'wine_conservation', 'choosing_food']:
            nba_add = PROMPTS['knowing_title_nlg'] + PROMPTS['nba_nlg']
        else:
            nba_add = PROMPTS['request_info_nlg'] + PROMPTS['nba_nlg']

        if intent == "delivery_info": nba_add = PROMPTS['nba_nlg'] + PROMPTS['delivery_nlg']
        else: nba_add = PROMPTS['nba_nlg'] + PROMPTS['confermation_nlg']

        if possible_list:
            nba_add = PROMPTS['listing_wine_nlg'] + nba_add

        if action == 'give_list':
            nba_add = PROMPTS['give_list_nlg']
         
        prompt = PROMPTS["NLG"] + nba_add + PROMPTS["NLG_end"]

        nlg_text = self.args.chat_template.format(prompt, nlg_text)
        nlg_input = self.tokenizer(nlg_text, return_tensors="pt").to(self.model.device)
        nlg_output = generate(self.model, nlg_input, self.tokenizer, self.args)
        self.logger.info(f"NLG: {nlg_text}")
        nlg_output = nlg_output.strip()

        return nlg_output
