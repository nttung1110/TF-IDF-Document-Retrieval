import json
import nltk
import pdb
import copy

from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.corpus import stopwords


# Lemmatizer is an actual language word while stemmer is not. Stemmer is much faster
# Lem and stem both brings the world to its root form


class TextProcessor():
    def __init__(self):
        self.list_stop_word = self.get_stopword("english")


    def tokenizer(self, sentence):
        # word_tokens = word_tokenize(sentence)
        word_tokens = RegexpTokenizer(r'\w+').tokenize(sentence)
        return word_tokens

    def lemmatizer(self, sentence):
        token_words = self.tokenizer(sentence)
        stem_sentence=[]
        for word in token_words:
            stem_sentence.append(WordNetLemmatizer().lemmatize(word))
        return " ".join(stem_sentence)

    def stemmer_by_porter(self, sentence):
        token_words = self.tokenizer(sentence)
        stem_sentence=[]
        for word in token_words:
            stem_sentence.append(PorterStemmer().stem(word))
        return " ".join(stem_sentence)

    def stemmer_by_lancaster(self, sentence):
        token_words = self.tokenizer(sentence)
        stem_sentence=[]
        for word in token_words:
            stem_sentence.append(LancasterStemmer().stem(word))
        return " ".join(stem_sentence)

    def get_stopword(self, language):
        return stopwords.words(language)

    def standard_process_word(self, word):
        if word in self.list_stop_word:
            return None

        processed_word = copy.copy(word)

        # lemmatize
        # processed_word = LancasterStemmer().stem(word)

        # lowercase
        processed_word = processed_word.lower()

        return processed_word

    def standard_process_sentence(self, sentence):
        token_words = self.tokenizer(sentence)

        processed_sentence = []
        for word in token_words:
            processed_word = self.standard_process_word(word)
            
            if processed_word is None:
                continue
            processed_sentence.append(processed_word)

        return " ".join(processed_sentence)
        

            

