from nltk import ngrams
import nltk.data
import preprocessor as pp

# creates a list of tokens from a document
def ngram_tokens(document, n):
    document = preprocess_input(document)
    sentencizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = sentencizer.tokenize(document)
    tokens = []
    for sentence in sentences:
        sentence = preprocess_input(sentence, remove_punctuation=True, remove_stop_words=True)
        grams = ngrams(sentence.split(), n)
        for gram in grams:
            tokens.append(gram)
    return tokens

def word_tokens(document):
    return document.split()

def preprocess_input(document, lower=True, remove_punctuation=False, remove_stop_words=False):
    preprocessor = pp.Preprocessor()
    if lower:
        document = document.lower()
    if remove_punctuation:
        document = preprocessor.remove_punctuation(document)
    if remove_stop_words:
        document = preprocessor.remove_stop_words(document, german=True, english=True)
    return document