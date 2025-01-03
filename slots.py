from extractor_data import *

possible_title = extract_db_init('title')
possible_typology = extract_db_init('typology')
possble_year = extract_db_init('vintage')
possible_grape = extract_db_init('grape') + extract_db_init('Secondary grape')
possible_style = extract_db_init('style')
possible_region = extract_db_init('region')
possible_abv = extract_db_init('abv')
possible_food = extract_db_init('food')
possible_flavor = extract_db_init('flavor')

class Ordering():
    def __init__(self):
        self.typology = None
        self.quantity = None
        self.address = None
        self.title = None
        self.phone = None
        self.gift = None
        self.pagament = None
        #self.price = None

        self.possibilities = {
            "title": possible_title,
            "typology": possible_typology,
            "quantity": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "gift": [True, False],
            "pagament": ['cash', 'credit card', 'paypal'],
            #"price": True
        }

        self.required = ['title', 'quantity', 'address', 'gift', 'pagament']

    def __str__(self):
        return f"Title: {self.title}, Typology: {self.typology}, Quantity: {self.quantity}, Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.pagament}"

    def extract(self):
        return {
            "title": self.title,
            "typology": self.typology,
            "quantity": self.quantity,
            "address": self.address,
            "phone": self.phone,
            "gift": self.gift,
            "pagament": self.pagament
        }

class ParingFood():
    def __init__(self):
        self.title = None
        self.typology = None
        self.food = None
        self.year = None
        self.grape = None
        self.color = None
        self.style = None

        self.possibilities = {
            "title": possible_title,
            "typology": possible_typology,
            "food": possible_food,
            "year": possble_year,
            "grape": possible_grape,
            "color": ['white', 'red', 'rose'],
            "style": possible_style   
        }

        self.required = ['food', 'color']

    def __str__(self):
        return f"Title: {self.title}, Typology: {self.typology}, Food Pairing: {self.food}, Year: {self.year}, Grape: {self.grape}, Color:{self.color}, Style: {self.style}"

    def extract(self):
        return {
            "typology": self.typology,
            "food": self.food,
            "year": self.year,
            "title": self.title,
            "grape": self.grape,
            "color": self.color,
            "style": self.style
        }

class AskInfo():
    def __init__(self):
        self.typology = None
        self.country = None
        self.region = None
        self.color = None
        self.grape = None
        self.abv = None
        self.closure = None
        self.flavor = None
        self.style = None
        self.title = None

        self.possibilities = {
            'typology': possible_typology,
            'country': ['italy', 'france'],
            'region': possible_region,
            'color': ['white', 'red', 'rose'],
            'grape': possible_grape,
            'abv': possible_abv,
            'closure': ['natural cork', 'screwcap', 'synthetic cork'],
            'flavor': possible_flavor,
            'style': possible_style,
            'title': possible_title
        }

        self.required = []
        
    def __str__(self):
        return f"Title: {self.title}, typology: {self.typology}, Country: {self.country}, Region: {self.region}, Color: {self.color}, Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}, Flavor: {self.flavor}, Style: {self.style}"
    
    def extract(self):
        return {
            "title": self.title,
            "typology": self.typology,
            "country": self.country,
            "region": self.region,
            "color": self.color,
            "grape": self.grape,
            "abv": self.abv,
            "closure": self.closure,
            "flavor": self.flavor,
            "style": self.style
        }
    

def assign_field (intent: object, field: str, value: str):
    # find the correct possible field
    for possible_field in intent.possibilities:
        if field in possible_field:
            # check if the value is in the possible values
            for ins in intent.possibilities[possible_field]:
                if ins == value or (ins == value.lower()):
                    setattr(intent, field, value)
                    break
            expanded_search(field, value, intent)
            break

def expanded_search(field_to_exclude, value, intent):
    for new_field in intent.possibilities:
        if field_to_exclude in new_field:
            continue

        for ins in intent.possibilities[new_field]:
            if ins == value:
                setattr(intent, new_field, value)
                break
