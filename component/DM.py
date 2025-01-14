from utils import PROMPTS, generate
from support_fn import extract_action_and_argument
    
class DM():
    def __init__(self, model, tokenizer, args, logger):
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        self.logger = logger
        pass

    def __call__(self, tracker, intent, provide_list):
        
        info_text = tracker.dictionary(intent)
        dm_text = str(info_text)

        if intent == "wine_ordering": nba = PROMPTS['list_nba'] + PROMPTS['delivery']
        elif intent == "general_info": nba = PROMPTS['general_info'] + PROMPTS['list_nba']
        else: nba = PROMPTS['list_nba'] + PROMPTS['confermation']

        if provide_list:
            nba = PROMPTS['list_wine'] + nba
        
        if intent == 'wine_origin': nba = nba + PROMPTS['origin_dm']
        prompt = PROMPTS["DM_start"] + nba + PROMPTS["DM_end"]
        
        dm_text = self.args.chat_template.format(prompt, dm_text)
        dm_input = self.tokenizer(dm_text, return_tensors="pt").to(self.model.device)
        dm_output = generate(self.model, dm_input, self.tokenizer, self.args)

        dm_output = dm_output.strip()
        
        self.logger.debug(f"DM output: {dm_output}")
        action, argument = extract_action_and_argument(dm_output)
        return action, argument
