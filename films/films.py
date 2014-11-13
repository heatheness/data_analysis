# -*- coding: utf-8 -*-

# sites.google.com/site/programmingtechniques

__author__ = 'nyash myash'
import codecs

def load_films():
    films = {}
    f = open('/Users/dmitrymakhotin/PycharmProjects/friday/films/namefilms.txt')
    for line in f:
        parts = line.split('\t')
        if len(parts) == 2:
            film_id = int(parts[0].strip())
            film_name = parts[1].strip()
            films[film_id]=film_name
    return films

# for user_id,score in scores.iteritems():
#     pass
#
# film_scores[user_id] -> score_1
#
# all_scores[film] -> fil,_scores



def load_scores():
    """пишем функцию, которая вернет all_scores"""
    all_scores = {}
    user_scores = {}
    for line in codecs.open('/Users/dmitrymakhotin/PycharmProjects/friday/films/inputrates.txt',encoding='utf'):
        parts = line.split('\t')
        user_id = int(parts[0].strip())
        film_id = parts[1].strip()
        score = float(parts[2].strip())/10.0
        if user_id not in user_scores:
            user_scores[user_id] = score


        # all_scores[film_id][user_id] = score
        all_scores.setdefault(film_id,{})[user_id] = score
    return all_scores



def calc_avg_score(all_scores):
    avg_score = {}
    # for film_scores in all_scores.values():
    #     for user_id in film_scores.keys():
    #         for id in all_scores.keys():






def calc_main_score(film_scores):
    s = 0.0
    for user_id, score in film_scores.iteritems():
        s+=score
    return s/float(len(film_scores))


def calc_similarity(scores1,scores2):
    #надо пронормировать функцию по средней оценке каждого пользователя
    #нужно сначала посчитать эту оценку
    # коэффициент корреляции прямая и обратная
    n = 0.0
    for user, score in scores1.iteritems():
        if user in scores2:
            m = score - scores2[user]
            n+=m*m

    return n

films = load_films()
all_scores = load_scores()
res = []

for film_id, film_scores in all_scores.iteritems():
    n = len(film_scores)
    if n < 5:
        continue
    m = calc_main_score(film_scores)
    res.append((m,n,film_id))

res.sort()

# for item in res:
#     m,n,id = item
#     id = int(id)
#     if id in films:
#         print m,n,films[id] # каго лешего не пашет???

# mean_scores = calc_mean_scores(all_scores)

# сколько пар фильмов были посмотрены хотя бы n пользователями
t = []
for film1,scores1 in all_scores.iteritems():
    for film2,scores2 in all_scores.iteritems():
        if film1<=film2:
            continue
        n = 0
        for user, score in scores1.iteritems():
            if user in scores2:
                n +=1
        if n>= 10:
            f = calc_similarity(scores1,scores2)
            t.append((f,film1,film2))
t.sort

# выводим результат
for x in t:
    f,i,j = x
    i = int(i)
    j = int(j)
    if i in films and j in films:
        print f, films[i], films[j]





