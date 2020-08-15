#!/usr/bin/python

#   a program to scrap an store the whole wikipedia vertex and edges,
#   so that an ofline program can find the shortes path on this data
#   istahd of having to do online html requests, which take time
#   by Goran Topic

from word import Word
from urllib.request import urlopen 
from bs4 import BeautifulSoup
from multiprocessing import Queue
import networkx as nx
import pickle
import datetime
import random
import collections
import re
import os
import json
        

def start_crawling():

    json_file = open('definitions.json', 'w', encoding='utf-8')
    word_file = open(word_list_filename, 'r')

    for word in  word_file:
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

            # save to json file
            json.dump(word_data, json_file, ensure_ascii=False, indent=4)

            print("got" + word)
        except:
            print("could not get word: " + word)
    word_file.close()

start_crawling()
        

