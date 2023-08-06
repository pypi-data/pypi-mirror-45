from spellchecker import SpellChecker
import spacy
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS as stopwords
import en_core_web_sm
import copy
import string

class NormalizeText:
    def __init__(self):
        self.stopwords = list(stopwords)
        self.spell_checker = None
        
    def add_to_stopwords(self, words: list):
        """
        add stop words to the list of stopwords.
        Parameter
        ---------
        words - a list of words to add to the stop word list.
        Note: These words will be removed from your text!!!
        """
        self.stopwords += words
        
    def remove_stopwords(self, text: str) -> str:
        """
        Gets rid of stop words
        Parameter
        ---------
        text - string to process
        Output
        ------
        string with stop words removed
        """
        words = [self.strip_punctuation(word)
                 for word in text.split()]
        return " ".join([word for word in words
                         if word not in self.stopwords])
        
    def normalize_case(self, text: str) -> str:
        """
        standardize case to lower case for all characters.
        Parameter
        ---------
        text - string to process
        Output
        ------
        string in lowercase
        """
        return text.lower()
        
    def initialize_spellchecker(self, text='', words=[], add_ner=False):
        """
        * Initializes the spellchecker and allows for 
        words that are proper knowns.
        Parameters
        ----------
        words - a custom list of words to not adjust
        add_ner - add all words found in the text 
        that are named entities to the list of words 
        to not adjust
        """
        nlp = en_core_web_sm.load()
        if add_ner:
            doc = nlp(text)
            words += [entity.text
                      for entity in doc.ents]
        self.spell_checker = SpellChecker()
        self.spell_checker.word_frequency.load_words(words)

    def strip_punctuation(self, word, return_punctuation=False):
        """
        This method strips punctuation at the end of a word.
        Parameter
        ---------
        word - a string to be stripped
        return_punctuation - if set to True, return the punctuation 
        that was split off as well.
        Output
        ------
        new_word - a new string without punctuation
        [optional] punctuation - the stripped punctuation
        """
        punctuation = ''
        for char in string.punctuation:
            if char in word:
                punctuation += char
        new_word = word.replace(punctuation, "")
        if return_punctuation:
            return new_word, punctuation
        else:
            return new_word
        
    def correct_spelling(self, text: str) -> str:
        """
        * Corrects the spelling of likely misspelled words.
        * Initialized with initialize_spellchecker method.
        * If there are spellings you want to not be corrected, 
        call initialize_spellchecker explicitly with those words.
        
        Parameter
        ---------
        text - string to process
        Output
        ------
        Spell checked string
        """

        # This is enough work that it should be its
        # own library.  
        # Making the spell checking better -
        # predict the next word based on the
        # previous words in the sentence
        # if previous words not available
        # use the next word and run through the
        # list of possible candidates
        # whatever word has the highest probability of
        # coming next, use that word
        # features to use -
        # word embedding?
        # ngrams?
        # tfidf?
        # BERT?
        
        tokens = text.split()
        misspelled = self.spell_checker.unknown(tokens)
        words = []
        for word in misspelled:
            word, punctuation = self.strip_punctuation(word,
                                                       return_punctuation=True)
            new_word = self.spell_checker.correction(word)
            new_word += punctuation
            words.append(new_word)
        return " ".join(words)
        
    def correct_whitespace(self, text: str) -> str:
        """
        Corrects the whitespace in text, so that 
        there is one white space between each word.
        Parameter
        ---------
        text - string to process
        Output
        ------
        string with one white space between strings 
        and no white space before or after
        """
        return " ".join(text.strip().split())
        


    
