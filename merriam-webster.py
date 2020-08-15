# sent a query for a word to the www.merriam-webster.com 

from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re


# dictionary api 
API_url_dictionary  = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"

API_key_dictionary = "?key=401b3951-f31a-474e-a13e-66fc0d46de0f"

# thesauarus api 
API_url_thesaurus  = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"

API_key_thesaurus = "?key=c7bd68ed-a9c2-47a5-92fc-5764ed7092a4"


def query_word_API(word):
    '''queries a word to www.merriam-webster.com API and retuns a dic 
       with the sintaxes definitions and synonyms and pronunciation '''  

        url = API_url_dictionary + word + API_key_dictionary

    try:
        
        json_data = request_webpage(url)
        print(json)
    except:
    



def request_json(url):
    '''request a web page '''
    try:
        return urlopen(url)
    except:
        print("could not connet to internet")
        return None


def get_word(soup):
    '''gets a the word from a given html suop '''
    # get word 
    try:
        word = soup.find('h1', class_='css-1jzk4d9').contents[0]
        return word
    except:
        print("could not get the word")
        return None


def get_pronunciation(soup):
    '''gets a the pronunciation for a word from a given html suop '''
    pronunciation = ''
    try:
        spell_content = soup.find('span', class_='pron-spell-content') 
        for span in spell_content.descendants:
            if not re.match("^<.*>$", span.__str__()):
                pronunciation += span
        return pronunciation
    except:
        print("could not get pronunciation value")
        return None

def get_syntaxes_and_defintions(soup):
    '''gets a the syntax and definitions for a word from a given html suop '''
    # get syntaxes 
    syntaxes = {}
    try:
        luna_pos = soup.find_all('section', class_='css-pnw38j e1hk9ate0') 
        for luna in luna_pos:
            # get current syntax
            current_syntax = luna.find('span', class_="luna-pos").contents[0]
            # initialize that given syntax as an empty list
            syntaxes[current_syntax] = []
            for definitions in luna.find_all('span', class_="one-click-content css-1p89gle e1q3nk1v4"):
                for definition in definitions:
                    # if it mathec a nomal definion
                    if re.match("^(?!<|Usually|\. | +|\(|\))[^\n]*(?<!>)$", definition.__str__()):
                        # set definition into the list of defintion for that given syntax of the word
                        syntaxes[current_syntax].append(definition)
        return syntaxes
    except:
        print("could not get syntax and definiion")
        return None


def get_synonyms(soup):
    # get synonyms
    synonyms = []
    try:
        synonyms_tags = soup.find('div', class_='css-191l5o0-ClassicContentCard e1qo4u830')
        synonyms_tags = synonyms_tags.find_all('span', class_='css-1y6i96q-WordGridItemBox etbu2a32')
        for tag in synonyms_tags:
            if tag.a is not None:
                synonyms.append(tag.a.string)
            elif tag.span is not None:
                synonyms.append(tag.span.string)
        return synonyms
    except:
        print("could not get synonyms")
        return None
        

