import string

ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"])

file = open('german-stop-words.txt')
file_content = file.read()
GERMAN_STOP_WORDS = set(file_content.split())

class Preprocessor:
    def __init__(self):
        self.english_words = set()
        self.english_stop_words = ENGLISH_STOP_WORDS
        self.german_stop_words = GERMAN_STOP_WORDS

    def remove_punctuation(self, text, replacer=' ', remove_periods=True):
        punctuation = string.punctuation
        do_not_remove_this = '-'
        if not remove_periods:
            do_not_remove_this += '.'
        for char in do_not_remove_this:
            period_index = punctuation.rfind(char)
            punctuation = punctuation[:period_index] + punctuation[period_index + 1:]
        return ''.join(c if c not in punctuation else replacer for c in text)

    def remove_english_words(self, text):
        if len(self.english_words) == 0:
            file = open('english-words.txt')
            file_content = file.read()
            self.english_words = set(file_content.split())
        new_text = []
        for word in text.split(' '):
            if word.lower() in self.english_words:
                continue
            new_text.append(word)
        result = ' '.join(new_text)
        return result

    # stop words are common words of a language. since they appear in nearly a lot of documents, we remove them
    # in order to keep them out of calculations.
    def remove_stop_words(self, document, german=True, english=True):
        new_doc = []
        for word in document.split():
            should = True
            if german:
                if word in self.german_stop_words:
                    should = False
            if english:
                if word in self.english_stop_words:
                    should = False
            if should:
                new_doc.append(word)
        return ' '.join(new_doc)


