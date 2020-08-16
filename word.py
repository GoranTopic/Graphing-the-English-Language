
class Word:
    def __init__(self, word, pronunciation = '', syntax_def = {}):
        self.word = word
        self.pronunciation = pronunciation
        self.synta_def = syntax_def 
        self.notes = []
        

    def __str__(self):
        return self.word

    def add_definition(self, syntax, defintion):
        self.syntax_def[syntax] = [ defintion ]

    def set_syntax_def(self, syntax_def):
        self.syntax_def = syntax_def
    
       

