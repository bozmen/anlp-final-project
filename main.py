import cluster
import random
import math
import collections
import tfidf
import jsonreader as inputreader
import helper
import preprocessor as pp
import pandas as pd
import tokenizer
import operator

# called initially. randomly assigns vectors to the clusters.
def initial_assign(tag_vectors, n):
    # randomly distribute vectors in clusters
    clusters = []
    for i in range(n):
        clusters.append(cluster.kCluster(str(i)))
    for id, v in enumerate(tag_vectors):
        clusters[random.randint(0, n - 1)].put_vector((id, v))
    # calculate initial scores
    for c in clusters:
        c.recalculate_centroid()
        c.select_medioid()
    return clusters

# assigns a vector to one cluster from a set based on the consıne sımılarıty to all clusters
def match_member(id_vector_pair, clusters):
    vector = id_vector_pair[1]
    id = id_vector_pair[0]
    best_score = 0
    best_cluster = int()
    for c in clusters:
        standart = c.medioid
        dot_product = 0
        a_length = 0
        b_length = 0
        for word in vector:
            vector_score = helper.get_value(vector, word)
            standart_score = helper.get_value(standart, word)
            dot_product += vector_score * standart_score
            a_length += vector_score * vector_score
            b_length += standart_score * standart_score
        if a_length == 0 or b_length == 0:
            continue
        cos_sim = dot_product / (math.sqrt(a_length) * math.sqrt(b_length))
        if cos_sim > best_score:
            best_score = cos_sim
            best_cluster = c.clusterID
    for c in clusters:
        if c.clusterID == best_cluster:
            c.put_vector((id, vector))
    return best_score

# loops a number of times through a set of clusters
def loopMatches(tag_vectors, no_of_clusters=25, no_of_loops=20):
    # randomly distribute tag vectors to clusters
    clusters = initial_assign(tag_vectors, no_of_clusters)
    # reassign everything to a better cluster no_of_loops times
    for i in range(no_of_loops):
        for c in clusters:
            c.reset_vector_list()
        for index, vector in enumerate(tag_vectors):
            match_member((index, vector), clusters)
            l = len(tag_vectors)
            progress = ((i * l) + index) / (no_of_loops * l)
            print("Progress: ", progress * 100, "%")
        for c in clusters:
            c.recalculate_centroid()
            c.select_medioid()
    return clusters

# read the xlsx file into python list using panda convention
def read_ads_to_list(xlsx_file):
    xls = pd.ExcelFile(xlsx_file)
    df1 = pd.read_excel(xls, 'data_frame')
    main_text = df1['Main Text']
    loc = df1['Location']
    bez = df1['Bezirk']
    zipped = zip(main_text, loc, bez)
    return list(zipped)[1:]

'''
def score_clusters_tfidf(clusters):
    corpus = []
    for cluster in clusters:
        document = ''
        vector_list = cluster.vector_list
        for vector in vector_list:
            document = ' '.join(vector.keys())
'''

# hierarchical implementation of k means that splits a corpus into a small number of clusters and then iterates
# on the 'least grouped' resulting cluster
def n_secting_k_means(clusters, max_clusters, split_k=2, no_of_loops=15):
    min_clust_id = None
    min_clust_score = None

    if len(clusters) >= max_clusters:
        # base case
        return clusters

    for ind, cluster in enumerate(clusters):

        cur_score = cluster.get_cluster_cosine_sim()
        if min_clust_score is None or cur_score < min_clust_score:
            min_clust_id = ind
            min_clust_score = cur_score

    cluster_to_be_clustered = clusters[min_clust_id]
    del clusters[min_clust_id]

    new_clusters = loopMatches(cluster_to_be_clustered.vector_list, split_k, no_of_loops)
    # name the new clusters such that their parent can be traced back in the heirarchy
    new_clusters[0].clusterID = cluster_to_be_clustered.clusterID + '0'
    new_clusters[1].clusterID = cluster_to_be_clustered.clusterID + '1'
    clusters.extend(new_clusters)
    return n_secting_k_means(clusters, max_clusters, split_k, no_of_loops)


texts = []

ads_list = read_ads_to_list('gesucht.xlsx')[:1000]
gesucht = [x[0] for x in ads_list]
locations = [x[1] for x in ads_list]
bezirks = [x[2] for x in ads_list]

preprocessor = pp.Preprocessor()

texts.extend(gesucht)

token_sets = []
for text in texts:
    token_sets.append(tokenizer.ngram_tokens(text, 1))

tfidf_vectors = tfidf.calculate_tf_idf_scores(token_sets)

cluster_number = input('How many clusters do you want?\n')
loop_number = input('How many loops?\n')

result_clusters = loopMatches(tfidf_vectors, int(cluster_number), int(loop_number))

# below code for n sectıng k means
# first_clusters = loopMatches(tfidf_vectors, 2, int(loop_number))
# result_clusters = n_secting_k_means(first_clusters, int(cluster_number), no_of_loops=int(loop_number))

output = ''

# deprecated approach for assessıng end clusters: tdıdf measures of the clusters as documents ın a corpus of all clusters
'''
def clustered_documents(clusters):
    result = ''
    for c in clusters:
        result += '\n Cluster ID: ' + str(c.clusterID)
        c_ids = c.ids
        for doc_id in c_ids:
            result += '\n\t' + texts[doc_id]
    return result

def tfidf_clusters(corpus, clusters):
    cluster_as_docs = []
    for c in clusters:
        doc_ids = c.ids
        cluster_as_doc = ' '.join([corpus[id] for id in doc_ids])
        cluster_as_docs.extend([cluster_as_doc])
    token_sets = []
    for doc in cluster_as_docs:
        token_sets.append(tokenizer.ngram_tokens(doc, 1))
    return tfidf.calculate_tf_idf_scores(token_sets)

tfidf_cluster_scores = tfidf_clusters(texts, result_clusters)

output = ''
for score in tfidf_cluster_scores:
    sorted_list = sorted(score.items(), key=lambda x: x[1])
    sorted_list.reverse()
    output += '\n\n' + str(sorted_list)
'''


def token_counts_corpus(token_sets):
    token_counts_corpus = collections.defaultdict(int)
    for token_set in token_sets:
        for token in token_set:
            token_counts_corpus[token] += 1
    return token_counts_corpus


def token_counts_doc_corpus(token_sets):
    token_counts_doc_corpus = collections.defaultdict(int)
    for token_set in token_sets:
        for token in set(token_set):
            token_counts_doc_corpus[token] += 1
    return token_counts_doc_corpus


token_counts_corpus = token_counts_corpus(token_sets)
token_counts_doc_corpus = token_counts_doc_corpus(token_sets)

token_to_keep_by_cluster = {}
count_of_tokens_in_clusters = collections.defaultdict(int)
for c in result_clusters:
    cluster_as_percent_corpus_docs = len(c.vector_list) / len(token_sets)
    cluster_token_doc_count = collections.defaultdict(int)
    cluster_token_count = collections.defaultdict(int)
    cluster_tokens_keep = []
    ids = c.ids
    for index in ids:
        token_set = token_sets[index]
        for token in token_set:
            cluster_token_count[token] += 1
        for unique_token in set(token_set):
            cluster_token_doc_count[unique_token] += 1
    count_of_tokens_in_clusters[c.clusterID] = sum(cluster_token_count.values())
    for token in cluster_token_count.keys():
        perc = cluster_token_count[token] / token_counts_corpus[token]
        perc_doc = cluster_token_doc_count[token] / token_counts_doc_corpus[token]
        if perc > cluster_as_percent_corpus_docs:
            cluster_tokens_keep.append((token,
                                        cluster_token_count[token], token_counts_corpus[token], perc,
                                        cluster_token_doc_count[token], token_counts_doc_corpus[token], perc_doc))

    token_to_keep_by_cluster[c.clusterID] = set(cluster_tokens_keep)

'''
for c in result_clusters:
    output += '\n\n\t\tCluster ' + str(c.clusterID)
    output += '\n\t\tSize: ' + str(len(c.vector_list))
    sorted_list = sorted(c.centroid.items(), key=lambda x: x[1])
    tokens = {token[0] for token in token_to_keep_by_cluster[c.clusterID]}
    sorted_list = [x for x in sorted_list if x[0] in tokens]
    sorted_list.reverse()
    output += '\n\n' + str(sorted_list[:50])
'''

# output += '\n\n' + str(token_to_keep_by_cluster)

for c in result_clusters:
    ind = c.clusterID
    output += '\n\nCluster ID: ' + str(ind)
    output += '\tCluster doc size: ' + str(len(c.vector_list))
    cluster_percent = count_of_tokens_in_clusters[c.clusterID] / sum(count_of_tokens_in_clusters.values())
    output += '\tCluster token percent: ' + str(cluster_percent)
    output += '\n'
    location_counts = collections.defaultdict(int)
    bezirk_counts = collections.defaultdict(int)
    for elem in c.ids:
        location_counts[locations[elem]] += 1
        bezirk_counts[bezirks[elem]] += 1

    f_loc = "{:30}{:5}"
    output += f_loc.format("Location Name", "Number of Docs")
    for location in location_counts.keys():
        output += '\n'
        output += f_loc.format(location, str(location_counts[location]))
    output += '\n'
    output += '\n'
    output += f_loc.format("Bezirk Name", "Number of Docs")
    for bezirk in bezirk_counts.keys():
        output += '\n'
        output += f_loc.format(bezirk, str(bezirk_counts[bezirk]))

    f = "{:30}{:>5}{:>5}{:>10}{:>5}{:>5}{:>10}"
    output += "\n"
    output += f.format("Token", "LC", "GC", "Perc", "LDC", "GDC", "Perc Doc")
    cluster_tokens = list(token_to_keep_by_cluster[ind])
    cluster_tokens.sort(key=operator.itemgetter(2))
    cluster_tokens.reverse()
    for elem in cluster_tokens:
        if elem[2] < 15:
            continue
        '''
        if elem[3] < (cluster_percent * 2):
            continue
        '''
        output += "\n"
        output += f.format(str(elem[0]), str(elem[1]), str(elem[2]), str(round(elem[3], 5)), str(elem[4]), str(elem[5]),
                           str(round(elem[6], 5)))

file = open('cluster_results', 'w')
file.write(output)
file.close()
