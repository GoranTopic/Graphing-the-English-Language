
class Word:
    def __init__(self, word, pronunciation = [], definitions = {}):
        self.word = word
        self.pronunciations = prounications
        self.definitions = definitions
        self.notes = []
        

    def __str__(self):
        return self.word

    def add_definition(self, syntax, defintion):
        self.syntax_def[syntax] = [ defintion ]

    def set_syntax_def(self, syntax_def):
        self.syntax_def = syntax_def
    
       

