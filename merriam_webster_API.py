# sent a query for a word to the www.merriam-webster.com 

from urllib.request import urlopen 
from bs4 import BeautifulSoup
import re

class merriam_webster_api()
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
    # html soup for it
    soup = None
    # word queried
    soup = None

    def query_API(self, word):
        '''queries a word to www.merriam-webster.com API and retuns a dic 
            with the sintaxes definitions and synonyms and pronunciation '''  
        word = word.rstrip()
        url = API_url_dictionary + word + API_key_dictionary
        json_data = urlopen(url)

    def request_html(self, url):
        '''request a web page html '''
        try:
            html =  urlopen(url)
            return html
        except:
            print(f"{bcolors.FAIL}Could connet to merriam-webster.com{bcolors.ENDC}")
            return None

    def make_html_soup(self, html):
        ''' make an html soup wit the given html file'''
        try:
            soup = BeautifulSoup(html, 'lxml' )
            return soup
        except:
            print(f"{bcolors.FAIL}Couldn't make soup out of html{bcolors.ENDC}")
            return None

    def is_word_not_found(self, soup):
        '''check whether the word was not found '''
        if soup.find_all('div', class_='words_fail_us_cont'):
            return True
        elif soup.find_all('h1', class_='missing-query'):
            return True
        else: 
            return False

    def get_word(self, soup):
        '''gets a the word from a given html soup '''
        # get word 
        try:
            self.word = soup.find('h1', class_='hword')
            return word.string.rstrip()
        except:
            print(f"{bcolors.FAIL}Could not get word{bcolors.ENDC}")
            return None


    def get_pronunciations(self, soup):
        '''gets a the pronunciation for a word from a given html soup '''
        try:
            pronunciations = soup.find_all('span', class_='pr') 
            # clean the children
            return [ pronunciation.get_text().rstrip() for pronunciation in pronunciations ]
        except:
            print(f"{bcolors.WARNING}Could not get pronunciation{bcolors.ENDC}")
            return None

    def get_definitions(self, soup):
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
                    # clean the example tag so it does not appear in the definition
                    [examples.clear() for examples in tag.find_all('span', class_='ex-sent')]
                    # clean the colon tag so it does not appear in the definition
                    [examples.clear() for examples in tag.find_all('strong', class_='mw_t_bc')]
                    # save string defintions
                    definitions[syntaxes[num].string].append([string.rstrip() for string in tag.stripped_strings][0])
            return definitions
        except:
            print(f"{bcolors.FAIL}Could not get definition{bcolors.ENDC}")
            return None

    def get_synonyms(self, soup):
        ''' get the synomyms of the web page '''
        synonyms = []
        try:
            synonym_label = soup.find('div', id='synonyms-anchor').find_all('p', class_="function-label")
            for label in synonym_label:
                if re.match('^Synonym.*$', label.string):
                    synonyms.extend([synonym_tag.string for synonym_tag in label.next_sibling.find_all('a')])
            return synonyms
        except:
            print(f"{bcolors.WARNING}Could not get synonyms{bcolors.ENDC}")
            return None

    def get_antoyms(self, soup):
        ''' get the antonyms of the web page '''
        antonyms = []
        try:
            synonym_label = soup.find('div', id='synonyms-anchor').find_all('p', class_="function-label")
            for label in synonym_label:
                if re.match('^Antonym.*$', label.string):
                    antonyms.extend([antonym_tag.string for antonym_tag in label.next_sibling.find_all('a')])
            return antonyms
        except:
            print(f"{bcolors.WARNING}Could not get antonyms{bcolors.ENDC}")
            return None

    def srap_webpage(self, word):
        '''Query a word using the webpage''' 
        url = dic_url + word
        soup = request_soup(url)

        # get word
        word_name = get_word(soup)
        # get pronunciation 
        pronunciations = get_pronunciations(soup)
        # get word syntax defintion
        definitions = get_definitions(soup)

        # get synonyms 
        synonyms = get_synonyms(soup)
        # get anyonyms
        antonyms = get_antoyms(soup)

        # make a dictionary data of the word
        # if we where unable to get word of definitions then return None
        if word_name is None:
            return None
        elif definitions is None:
            return None
        else:
            word_data = {'word' : word_name, 
                         'pronunciation': pronunciations, 
                         'definitions': definitions, 
                         'synonyms': synonyms,
                         'antonyms': antonyms }
            # return data
            return word_data
       

    def query_word(self, word):
        '''queries a word to dictionary.com and retuns a dic 
           with the sintaxes definitions and synonyms and pronunciation '''  
        self.word = word.rstrip()
        # Try to query word with API
        #definition = query_API(word)
        # if got positive result
        #if definition is not None:
            # fix json format
        #return result
        # try to get word from webpage
        defintion = self.scrap_webpage(word)    

        if defintion is not None:
            return defintion
        else:
            print("could not get definition")
            return None

