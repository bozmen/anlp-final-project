from collections import defaultdict
from math import log
import helper

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

stop_words = set()
stop_words.update(GERMAN_STOP_WORDS)
stop_words.update(ENGLISH_STOP_WORDS)

# document : String
def calculate_tf_scores(tokens):
    tf_dict = defaultdict(int)
    N = len(tokens)
    for token in tokens:
        if token in stop_words:
            continue
        tf_dict[token] += 1
    for token in set(tokens):
        cur = tf_dict[token]
        # tf_dict[word] = log(1 + cur)
        tf_dict[token] = cur / N
    return tf_dict

# corpus : List<String>
# corpus is a list of documents
def calculate_idf_scores(corpus):
    N = len(corpus)
    idf_dict = defaultdict(float)
    token_appers = defaultdict(int)
    all_tf_scores = []
    for token_set in corpus:
        tf_scores = calculate_tf_scores(token_set)
        all_tf_scores.append(tf_scores)
        for token in tf_scores:
            token_appers[token] += 1
    for token in token_appers:
        nToken = helper.get_value(token_appers, token)
        # idf_dict[token] = log(1 + (N / nToken))
        idf_dict[token] = log(N / (nToken + 1))
        ################ SCIENTIFIC MAGIC ######################
        if (nToken <= 5):
            idf_dict[token] = 0
        ################ GRANULARITY ######################
    return idf_dict

def calculate_tf_idf_scores(corpus):
    tf_idf_vectors = []
    idf_dict = calculate_idf_scores(corpus)
    for token_set in corpus:
        tf_idf_dict = defaultdict(float)
        tf_scores = calculate_tf_scores(token_set)
        for token in token_set:
            tf_idf_dict[token] = helper.get_value(tf_scores, token) * helper.get_value(idf_dict, token)
        tf_idf_vectors.append(tf_idf_dict)
    return tf_idf_vectors
