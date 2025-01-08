from utils import PROMPTS, generate
from support_fn import extract_action_and_argument
    
class DM():
    def __init__(self, model, tokenizer, args):
        self.model = model
        self.tokenizer = tokenizer
        self.args = args
        pass

    def __call__(self, tracker, intent, refactor):
        
        self.info_text = tracker.dictionary(intent)
        dm_text = str(self.info_text) + '\n' + str(refactor)
        
        dm_text = self.args.chat_template.format(PROMPTS["DM2"], dm_text)
        dm_input = self.tokenizer(dm_text, return_tensors="pt").to(self.model.device)
        dm_output = generate(self.model, dm_input, self.tokenizer, self.args)

        dm_output = dm_output.strip()

        with open("dm_output.txt", "w") as file:
            file.write(dm_output)
        
        # logger.debug(f"DM output: {dm_output}")
        action, argument = extract_action_and_argument(dm_output)
        return action, argument
