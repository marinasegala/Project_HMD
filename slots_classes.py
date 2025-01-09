from extractor_data import *

possible_title_bottle = extract_db_init('title_bottle')
possible_typology = extract_db_init('typology')
possble_year = extract_db_init('year')
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
        self.title_bottle = None
        self.phone = None
        self.gift = None
        self.pagament = None
        #self.price = None

        self.possibilities = {
            "title_bottle": possible_title_bottle,
            "typology": possible_typology,
            "quantity": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "gift": [True, False],
            "pagament": ['cash', 'credit card', 'paypal'],
            #"price": True
        }

        self.required = ['title_bottle', 'quantity', 'address', 'gift', 'pagament']

    def __str__(self):
        return f"Title: {self.title_bottle}, Typology: {self.typology}, Quantity: {self.quantity}, Address: {self.address}, Phone: {self.phone}, Gift: {self.gift}, Pagament: {self.pagament}"

    def extract(self):
        return {
            "title_bottle": self.title_bottle,
            "typology": self.typology,
            "quantity": self.quantity,
            "address": self.address,
            "phone": self.phone,
            "gift": self.gift,
            "pagament": self.pagament
        }

class ParingFood():
    def __init__(self):
        self.title_bottle = None
        self.typology = None
        self.food = None
        self.year = None
        self.grape = None
        self.color = None
        self.style = None

        self.possibilities = {
            "title_bottle": possible_title_bottle,
            "typology": possible_typology,
            "food": possible_food,
            "year": possble_year,
            "grape": possible_grape,
            "color": ['white', 'red', 'rose'],
            "style": possible_style   
        }

        self.required = ['food', 'color']

    def __str__(self):
        return f"Title: {self.title_bottle}, Typology: {self.typology}, Food Pairing: {self.food}, Year: {self.year}, Grape: {self.grape}, Color:{self.color}, Style: {self.style}"

    def extract(self):
        return {
            "typology": self.typology,
            "food": self.food,
            "year": self.year,
            "title_bottle": self.title_bottle,
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
        self.title_bottle = None

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
            'title_bottle': possible_title_bottle
        }

        self.required = []
        
    def __str__(self):
        return f"Title: {self.title_bottle}, typology: {self.typology}, Country: {self.country}, Region: {self.region}, Color: {self.color}, Grape: {self.grape}, ABV: {self.abv}, Closure: {self.closure}, Flavor: {self.flavor}, Style: {self.style}"
    
    def extract(self):
        return {
            "title_bottle": self.title_bottle,
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
