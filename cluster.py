import collections
import helper
import math

class kCluster:
    # this is a class which represents a single cluster for a k-means algorithm
    def __init__(self, cluster_id):
        # initialized with dictionary for centroid measure
        self.centroid = collections.defaultdict(float)
        self.clusterID = cluster_id
        self.vector_list = []
        self.ids = []

    def put_vector(self, vector_to_be_added):
        self.ids.append(vector_to_be_added[0])
        self.vector_list.append(vector_to_be_added[1])

    # find new centroid after reassigning documents to clusters in a loop
    def recalculate_centroid(self):
        word_doc_count = collections.defaultdict(int)
        word_total_scores = collections.defaultdict(int)
        vector_list = self.vector_list
        centroid_keys = set()
        for vector in vector_list:
            words = vector.keys()
            centroid_keys.update(words)
            for word in words:
                word_doc_count[word] += 1
                word_total_scores[word] += vector[word]

        new_centroid = collections.defaultdict(float)
        for word in centroid_keys:
            # vector_count = len(vector_list)
            # documents_with_word = word_doc_count[word] #
            word_total_score = word_total_scores[word]
            # score = word_total_score / documents_with_word
            # score = word_total_score / vector_count
            score = word_total_score
            if score > 0:
                new_centroid[word] = score
        self.centroid = new_centroid

    # this is useful if you decide to use medioid rather than centroid, which works better in long documents.
    def select_medioid(self):
        vector_list = self.vector_list
        cur_centroid = self.centroid
        medioid = {}
        medioid_index = -1
        max_score = -1
        for ind, vector in enumerate(vector_list):
            score = self.cos_sim(vector, cur_centroid)
            if max_score < score:
                medioid = vector
                medioid_index = ind
                max_score = score
        self.medioid = medioid
        self.medioid_index = medioid_index

    # calculates the cosine similarity between two vectors
    def cos_sim(self, vector_1, vector_2):
        dot_product = 0
        a_length = 0
        b_length = 0
        for token in vector_1:
            dot_product += helper.get_value(vector_1, token) * helper.get_value(vector_2, token)
            a_length += helper.get_value(vector_1, token) * helper.get_value(vector_1, token)
            b_length += helper.get_value(vector_2, token) * helper.get_value(vector_2, token)
        if a_length == 0 or b_length == 0:
            score = 0
        else:
            score = dot_product / (math.sqrt(a_length) * math.sqrt(b_length))
        return score

    # a metric denotes how compact a cluster is
    def get_cluster_cosine_sim(self):
        med = self.medioid
        n = len(self.vector_list)
        total_score = 0
        for vector in self.vector_list:
            total_score += self.cos_sim(vector, med)
        return 0 if n == 0 else total_score / n

    def reset_vector_list(self):
        # resets urls but not centroid measure or clusterID
        self.vector_list = []
        self.ids = []

    def centroid_closeness(self):
        total = sum(self.centroid.values())
        vector_count = len(self.vector_list)
        return total / vector_count if vector_count != 0 else 0

    def medioid_closeness(self):
        total = sum(self.medioid.values())
        vector_count = len(self.vector_list)
        return total / vector_count if vector_count != 0 else 0

    def get_ordered_centroid(self):
        sorted_list = sorted(self.centroid.items(), key=lambda x:x[1])
        sorted_list.reverse()
        return sorted_list

    def get_ordered_medioid(self):
        sorted_list = sorted(self.medioid.items(), key=lambda x:x[1])
        sorted_list.reverse()
