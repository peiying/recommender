# -*- coding: utf-8 -*-
from math import sqrt
import numpy as np
import collections

users_views = {"David": ["b", "c", "d"],
               "Matt": ["a", "b", "e"],
               "Ben": ["a", "b", "c", "d"],
               "Chris": ["a", "c", "d"],
               "Tori": ["b"]}
users_dic = {"David": [0, 1, 1, 1, 0],
               "Matt": [1, 1, 0, 0, 1],
               "Ben": [1, 1, 1, 1, 0],
               "Chris": [1, 0, 1, 1, 0],
               "Tori": [0, 1, 1, 0, 1]}
users_matrix = [[0, 1, 1, 1, 0], [1, 1, 0, 0, 1], [1, 1, 1, 1, 0], [1, 0, 1, 1, 0], [0, 1, 1, 0, 1]]


def compute_cosine_similarity(user1, user2):
    num = 0
    dem1 = 0
    dem2 = 0
    for x in range(len(user1)):
        num += user1[x] * user2[x]
        dem1 += user1[x] ** 2
        dem2 += user2[x] ** 2
    return num / (sqrt(dem1) * sqrt(dem2))

users_matrix = np.array(users_matrix)
items = ['a', 'b', 'c', 'd', 'e']

item_matrix = np.array([array for array in users_matrix.transpose()])
interest_similarities = [[compute_cosine_similarity(user_vector_i, user_vector_j)
                          for user_vector_j in item_matrix]
                         for user_vector_i in item_matrix]
itemsDict = {}
for i in range(len(items)):
    itemsDict[items[i]] = interest_similarities[i]

def most_similar_interests_to(name):
    similarities = itemsDict[name]
    pairs = [(items[i], similarity)
              for i, similarity in enumerate(similarities)
              if similarity > 0 and name != items[i]]
    return sorted(pairs, key=lambda (_, similarity): similarity, reverse=True)

def item_based_suggestions(user_name, include_current_interests=False):
    #user_id 暂时为0到4
    suggestions = collections.defaultdict(float)
    user_interest_vector = users_dic[user_name]
    for interest_id, is_interested in enumerate(user_interest_vector):
        if is_interested == 1:
            similar_interests = most_similar_interests_to(items[interest_id])
            for interest, similarity in similar_interests:
                suggestions[interest] += similarity
    #根据权重排序
    suggestions = sorted(suggestions.items(), key=lambda (_,similarity): similarity, reverse=True)

    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) for suggestion, weight in suggestions if suggestion not in users_views[user_name]]

print item_based_suggestions("Tori", False)

