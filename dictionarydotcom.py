# sent a query for a word to the dictonary.com 

from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re

# dictonary.com url 
dic_url = 'https://www.dictionary.com/browse/' 

# thesaurus.com url
thesa_url = 'https://www.thesaurus.com/browse/'


def request_webpage(url):
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
        

def query_word(word):
    '''queries a word to dictionary.com and retuns a dic 
       with the sintaxes definitions and synonyms and pronunciation '''  
    url = dic_url + word

    try:
        page_html = request_webpage(url)
        # make soup....hmmm yummi =) lxml to make it fast 
        soup = BeautifulSoup( page_html, 'lxml' )
        # find the section of the word
        soup = soup.find('div', class_='css-1urpfgu')

        # get word
        word_name = get_word(soup)

        # get pronunciation 
        pronunciation = get_pronunciation(soup)
        # get word syntax defintion
        definitions = get_syntaxes_and_defintions(soup)

        # change to thesaurus webpage
        thesaurus_link = soup.find('a', class_='css-1pfx2g8 e12fnee32')['href']
        page_html = request_webpage(thesaurus_link)
        soup = BeautifulSoup( page_html, 'lxml' )

        # get synonyms 
        synonyms = get_synonyms(soup)

        # make a dictionary data of the word
        word_data = { 'word' : word_name, 'pronunciation': pronunciation , 'definitions': definitions, 'synonyms': synonyms }
        # return word data
        return word_data
    except:
        print("could not get word: " + word)
        return None


