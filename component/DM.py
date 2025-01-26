from utils import PROMPTS, generate
from support_fn import extract_action_and_argument
    
class DM():
    def __init__(self, history, model, tokenizer, args, logger):
        self.history = history
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        self.logger = logger
        pass

    def __call__(self, tracker, intent, provide_list, last_action):
        
        info_text = tracker.dictionary(intent)
        dm_text = str(info_text)

        nba = PROMPTS['nba']
        adding = ''

        if provide_list:
            nba = PROMPTS['listing_wine'] + nba
            adding = "\nThe action provide_list has greater priority than request_slot! Respect that!"
            dm_text = str(info_text)[:-2] + ", 'provide_list' = True}}" 

        print('REQUIRED USER',  tracker.required_list_user)
        print(last_action)

        if tracker.required_list_user or last_action == 'provide_list':
            nba = PROMPTS['give_list']
            dm_text = str(info_text)[:-2] + ", 'provide_list' = True}}"
        
        adding = adding + PROMPTS["DM_end"]

        if 'ordering' in intent:
            nba = nba + PROMPTS['delivery']
        else:
            nba = nba + PROMPTS['confermation']
        
        prompt = PROMPTS["DM_start"] + nba + adding
        
        dm_text = self.args.chat_template.format(prompt, dm_text)
        self.logger.debug(f"DM input: {dm_text}")
        dm_input = self.tokenizer(dm_text, return_tensors="pt").to(self.model.device)
        dm_output = generate(self.model, dm_input, self.tokenizer, self.args)

        dm_output = dm_output.strip()
        
        self.logger.debug(f"DM output: {dm_output}")
        action, argument = extract_action_and_argument(dm_output)
        return action, argument
