import argparse
from argparse import Namespace
from typing import Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BatchEncoding,
    PreTrainedTokenizer,
    PreTrainedModel,
)

PROMPTS = {
    "START": """Hi, I am your wine assistant. How can I help you?""",

    "wine-details": """The intent extracted is 'wine_details'. Extract the slots values from the input of the user.
The slots are: [flavor, grape, color, sparkling, abv, year, typology].
""",

    "wine-origin": """The intent extracted is 'wine_origin'. Extract the slots values from the input of the user.
The slots are: [country, region, typology, title_bottle].
""",

    "wine-production": """The intent extracted is 'wine_production'. Extract the slots values from the input of the user.
The slots are: [grape, abv, closure].
""",

    "wine-conservation": """The intent extracted is 'wine_conservation'. Extract the slots values from the input of the user.
The slots are: [fridge, cellar, temperature].
""",

    "wine-paring": """The intent extracted is 'wine_paring'. Extract the slots values from the input of the user.
The slots are: [style, color, typology].
""",

    "food-paring": """The intent extracted is 'food_paring'. Extract the slots values from the input of the user.
The slots are: [food, style, abv].
""",

    "wine-ordering": """The intent extracted is 'wine_ordering'. Extract the slots values from the input of the user.
The slots are: [typology, color, quantity, budget, title_bottle].
""",

    "wine_delivery": """The intent extracted is 'wine_delivery'. Extract the slots values from the input of the user.
The slots are: [address, phone, gift, kind_pagament].
""",

    "NLU_slots": """You are a component for a wine bot assistant.  Do not invent! If values are not present in the user input, and so they are not specified, you have to put 'null' as value in the slot.
Do not assume any value as default! If they are not specified by the user, put 'null' as value.
If the user specifies a value, put it in the slot. If the user specifically says that does not know somwthing, put 'null' in the slot.
Return only the json object composed as {"intent": "", "slots": {}}.
Return ONLY the json
""", 

    "PRE-NLU": """Break the user input into multiple sentences based on the following intents:
- wine_details: if the user wants to know more about the characteristics of a wine.
- wine_origin: if the user wants to know more about the origin of a wine.
- wine_production: if the user wants to know more about the production of a wine.
- wine_conservation: if the user wants to know more about the conservation of a wine.
- wine_paring: if the user has a wine and he wants to pair it with a food.
- food_paring: if the user has a dish and he wants to pair it with a wine.
- wine_ordering: if the user wants to buy wine.
Only provide the sequences of intents, as follow: ["sentence1", "sentence2", ...]
Return only the list.
""",

    "NLU_intents": """You are a component for a wine bot assistant.
Break the user input into multiple sentences based on the following intents:
- general_info: if the user wants general informations about a wine.
- wine_details: if the user wants to know more about the characteristics of a wine or he wants general informations about it.
- wine_origin: if the user wants to know more about the origin of a wine.
- wine_production: if the user wants to know more about the production of a wine.
- wine_conservation: if the user wants to know more about the conservation of a wine.
- wine_paring: if the user has a wine and he wants to pair it with a food.
- food_paring: if the user has a dish and he wants to pair it with a wine.
- wine_ordering: if the user wants to buy wine.
- delivery: if the user is giving information about the delivery.
- out_of_domain, if the input does not match any of the above and none of them is predicted.
Provide a list of intents as follow: ["intent1", "intent2", ...].
Return ONLY the list of intents, nothing more!
""",

    "DM_start": """You are the Dialogue Manager of a wine bot assistent.
Given the output of the NLU component, you should ONLY generate the next best action from this list: """,

    "DM_end": """ You need to write the name of the action with also the correspondings parameters.
Return ONLY the next best action!""",

    "list_nba": """
- request_info(slot), if a slot value is missing (null)
- goal_assistant(intent), if the intent is equal to out_of_domain
- repeat(slot), if the system needs clarification on a slot value""",

    "general_info":"""
- specific_info(intent), if the intent is equal to general_info""",

    "confermation": """
- confermation(intent), if all slots have been filled""",

    "list_wine": """
- provide_list(intent), if there are sufficient slots filled or the user asks for a list of wines""",

    "delivery": """
- delivery_info(intent), if all slots have been filled""",

    "DM2": """You are the Dialogue Manager of a wine bot assistent.
Given the output of the NLU component, you should ONLY generate the next best action from this list:
- request_info(slot), if a slot value is missing (null)
- provide_suggestios(intent),
- goal_assistant(intent), if the intent is equal to out_of_domain
- repeat(slot), if the system needs clarification on a slot value
- confermation(intent), if all slots have been filled
You need to write the name of the action with also the correspondings parameters.
Return ONLY the next best action! """,

    "NLG": """You are the NLG component of a wine bot assistent: you must be very polite.
Given the next best action classified by the Dialogue Manager (DM), you should only generate a lexicalized response for the user.
The response has to match the next best action of the DM.
Possible next best actions are:
""", 

    "list_nba_nlg": """
- request_info(slot): generate an appropriate question to ask the user for the missing slot value
- goal_assistant(intent): generate an appropriate message with the domain of the bot
- repeat(slot): generate a message to ask the user to repeat the information""",

    "general_info":"""
- specific_info(intent): generate a message where there is a list of possible information that the user can ask. These are: deatils of the wine, origin of the wine, production of the wine, conservation of the wine""",

    "confermation_nlg": """
- confermation(intent): generate an appropriate confirmation message for the user intent""",

    "list_wine_nlg": """
- provide_list(intent): generate an appropriate message for introducing the list of wines to the user""",

    "shopper_nlg": """
- delivery_info(intent), if all slots have been filled"""

}

MODELS = {
    "llama2": "meta-llama/Llama-2-7b-chat-hf",
    "llama3": "meta-llama/Meta-Llama-3-8B-Instruct",
}

TEMPLATES = {
    "llama2": "<s>[INST] <<SYS>>\n{}\n<</SYS>>\n\n{} [/INST]",
    "llama3": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{}<|eot_id|><|start_header_id|>assistant<|end_header_id|>",
}

def get_args() -> Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m query_model",
        description="Query a specific model with a given input.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "model_name",
        type=str,
        choices=list(MODELS.keys()),
        help="The model to query.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="The device to use for the model.",
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Split the model across multiple devices.",
    )
    parser.add_argument(
        "--dtype",
        type=str,
        choices=["f32", "bf16"],
        default="bf16",
        help="The data type to use for the model.",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=128,
        help="The maximum sequence length to use for the model.",
    )

    parsed_args = parser.parse_args()
    parsed_args.chat_template = TEMPLATES[parsed_args.model_name]
    parsed_args.model_name = MODELS[parsed_args.model_name]

    return parsed_args

def load_model(args: Namespace) -> Tuple[PreTrainedModel, PreTrainedTokenizer]:
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        device_map="auto" if args.parallel else args.device, 
        torch_dtype=torch.float32 if args.dtype == "f32" else torch.bfloat16,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    return model, tokenizer  # type: ignore


def generate(
    model: PreTrainedModel,
    inputs: BatchEncoding,
    tokenizer: PreTrainedTokenizer,
    args: Namespace,
) -> str:
    output = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=args.max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
    )
    return tokenizer.decode(
        output[0][len(inputs.input_ids[0]) :], skip_special_tokens=True
    )