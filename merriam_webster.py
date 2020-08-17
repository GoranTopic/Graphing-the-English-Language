# sent a query for a word to the www.merriam-webster.com 

from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re


# www.merrian-webster.com url 
dic_url = 'https://www.merriam-webster.com/dictionary/' 

# thesaurus url
thesa_url = 'https://www.merriam-webster.com/thesaurus/'

# dictionary api 
API_url_dictionary  = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
API_key_dictionary = "?key=401b3951-f31a-474e-a13e-66fc0d46de0f"

# thesauarus api 
API_url_thesaurus  = "https://www.dictionaryapi.com/api/v3/references/thesaurus/json/"
API_key_thesaurus = "?key=c7bd68ed-a9c2-47a5-92fc-5764ed7092a4"







def query_API(word):
    '''queries a word to www.merriam-webster.com API and retuns a dic 
       with the sintaxes definitions and synonyms and pronunciation '''  
    word = word.rstrip()

    url = API_url_dictionary + word + API_key_dictionary
    print("quering: " + url )
        
    json_data = urlopen(url)
    print(json_data)
        



def request_webpage(url):
    '''request a web page '''
    try:
        return urlopen(url)
    except:
        print("could not connet to internet")
        return None


def get_word(soup):
    '''gets a the word from a given html soup '''
    # get word 
    try:
        word = soup.find('h1', class_='hword')
        return word.string
    except:
        print("could not get the word")
        return None


def get_pronunciations(soup):
    '''gets a the pronunciation for a word from a given html soup '''
    try:
        pronunciations = soup.find_all('span', class_='pr') 
        return [ pronunciation.string for pronunciation in pronunciations ]
    except:
        print("could not get pronunciation value")
        return None

def get_definitions(soup):
    '''gets a the syntax and definitions for a word from a given html soup '''
    # get syntaxes 
    definitions = {}
    try:
        syntaxes = soup.find_all('span', class_="fl")
        definition_divs = soup.find_all('div', id=re.compile("dictionary\-entry\-[1-9]"))
        for num in range(0, len(definition_divs)):
            definitions[syntaxes[num].string] = [] 
            definition_tags = definition_divs[num].find_all('span', class_="dtText")
            for tag in definition_tags:    
                definitions[syntaxes[num].string].append([string for string in tag.stripped_strings][1])
        return definitions
    except:
        print("could not get definitions")
        return None

def get_synonyms(soup):
    ''' get the synomyms of the web page '''
    synonyms = []
    try:
        synonym_label = soup.find('div', id='synonyms-anchor').find_all('p', class_="function-label")
        for label in synonym_label:
            if re.match('^Synonym.*$', label.string):
                synonyms.extend([synonym_tag.string for synonym_tag in label.next_sibling.find_all('a')])
        return synonyms
    except:
        print("could not get synonyms")
        return None

def get_antoyms(soup):
    ''' get the antonyms of the web page '''
    antonyms = []
    try:
        synonym_label = soup.find('div', id='synonyms-anchor').find_all('p', class_="function-label")
        for label in synonym_label:
            if re.match('^Antonym.*$', label.string):
                antonyms.extend([antonym_tag.string for antonym_tag in label.next_sibling.find_all('a')])
        return antonyms
    except:
        print("could not get antonyms")
        return None

def scrap_webpage(word):
    '''Query a word using the webpage''' 
    url = dic_url + word
    
    page_html = request_webpage(url)
    soup = BeautifulSoup(page_html, 'lxml' )

    # get word
    word_name = get_word(soup)
    print(word_name)
    # get pronunciation 
    pronunciations = get_pronunciations(soup)
    # get word syntax defintion
    definitions = get_definitions(soup)

    # get synonyms 
    synonyms = get_synonyms(soup)
    # get anyonyms
    antonyms = get_antoyms(soup)

    # change to thesaurus webpage
    #thesaurus_link = soup.find('a', class_='css-1pfx2g8 e12fnee32')['href']
    #page_html = request_webpage(thesaurus_link)
    #soup = BeautifulSoup( page_html, 'lxml' )


    # make a dictionary data of the word
    word_data = {   'word' : word_name, 
                    'pronunciation': pronunciations, 
                    'definitions': definitions, 
                    'synonyms': synonyms,
                    'antonyms': antonyms }
    # return data
    return word_data
       

def query_word(word):
    '''queries a word to dictionary.com and retuns a dic 
       with the sintaxes definitions and synonyms and pronunciation '''  
    word = word.rstrip()
    
    # Try to query word with API
    #definition = query_API(word)
    # if got positive result
    #if definition is not None:
        # fix json format
        #return result
    
    # try to get word from webpage
    defintion = scrap_webpage(word)    
    if defintion is not None:
        return defintion

    print("could not get definition")
    return None


