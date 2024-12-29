from utils import PROMPTS, generate_response_Ollama
import re

def extract_action_and_argument(input_string):
    ## TODO add check in case there is more in the output string from the LLM
    # Remove any ' characters from the input string
    input_string = input_string.replace("'", "")
    input_string = input_string.replace("\"", "")
    # Define the regex pattern for extracting action and argument
    pattern = r'(\w+)\(([\w\s=]+)\)' #r'(\w+)\((.*)\)\s*=\s*(.*)' #r'(\w+)\((\w+)\)'
    match = re.match(pattern, input_string)
    
    if match:
        action = match.group(1)  # Extract the action
        argument = match.group(2)  # Extract the argument
        if '=' in argument:
            argument = argument.split('=')[1]
        return action, argument
    
class DM():
    def __init__(self):
        pass

    def __call__(self, tracker, intent):
        
        self.info_text = tracker.dictionary(intent)
        dm_text = PROMPTS["DM"] +'\n'+ str(self.info_text)
        dm_output = generate_response_Ollama(dm_text)
        dm_output = dm_output.strip()

        with open("dm_output.txt", "w") as file:
            file.write(dm_output)
        
        # logger.debug(f"DM output: {dm_output}")
        action, argument = extract_action_and_argument(dm_output)
        return action, argument