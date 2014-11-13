# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

import math
import collections

"""построить решающее дерево. выборки пополам"""


# /Users/dmitrymakhotin/PycharmProjects/friday/decision_tree

file = open('/Users/dmitrymakhotin/PycharmProjects/friday/decision_tree/zoo.data.txt')

zoo = []

for l in file:
    item = l.strip().split(',')
    assert len(item) == 18
    zoo.append(item)

# def tree():
#     return collections.defaultdict(tree)
#
# t = tree()
# t['1']['3'] = 4
# print t

# print zoo

# считаем энтропию
def entropy(items):
    # e = 0
    # k = float(len(items)) - 1
    # counter=collections.Counter(items[1:])
    # # print counter
    # # print dict(counter)
    # for m in dict(counter).keys():
    #     n = float(m) /  k
    #     e+= -n * math.log(n)
    # return e

    labels = {}
    for item in items:
        label = item[17]
        labels.setdefault(label,0)
        labels[label] +=1
    e = 0.0
    for n in labels.values():
        p = float(n)/float(len(items))
        e+=-p*math.log(p)
    return e

# for z in zoo:
#     print entropy(z)

mamals = [i for i in zoo if i[17] == '1']

# print entropy(mamals)

def information_gain(items, i):
    """i - номер атрибута по которому строим кучку"""
    groups = {}
    gain = entropy(items)
    for item in items:
        value = item[i]
        groups.setdefault(value,[]).append(item)
    # e = entropy(items)
    for group in groups.values():
        p = float(len(group)) / len(items)
        e = entropy(group)
        gain -= p*e
    return gain


def best_match(items):
    #returns most probable class or classes
    groups = {}
    for item in items:
        type = item[17]
        v = groups.setdefault(type,0)
        groups[type]= v+1
    max_val = max(groups.keys(), key = lambda x: groups[x])
    ans = [k for k,v in groups.items() if v==max_val]
    if len(ans) == 1:
        return str(ans[0])
    else:
        return ' or '.join(ans)


def best_atr(items,attributes):
    # returns most informative attribute
    gain = {}
    for atr in attributes:
        gain[atr] = information_gain(items,atr)
    return max(gain.keys(), key = lambda x: gain[x])

def build_tree(items,attributes):
    if len(attributes) == 0:
        """возвращаемся на уровень выше и считаем наиболее вероятный класс"""
        return 'unknown'
    else:
        types = [i[17] for i in items]
        max_entropy = math.log(len(set(types)))
        normal_entropy = 0.25 * max_entropy
        current_entropy = entropy(items)
        if current_entropy == 0:
            return str(items[0][17])
        elif current_entropy <= normal_entropy:
            """find most probable class or classes"""
            return best_match(items)
        else:
            """find most informative attribute"""
            atr = best_atr(items, attributes)
            groups = {}
            for item in items:
                value = item[atr]
                groups.setdefault(value,[]).append(item)
            l = []
            l.append(atr)
            attributes.remove(atr)
            l.append({key:build_tree(groups[key], attributes) for key in groups.keys()})
            return l

def get_type(item,tree):
    if isinstance(tree, str):
        return tree
    else:
        try:
            value = item[tree[0]]
            tree = tree[1][value]
            return get_type(item,tree)
        except KeyError:
            return 'rebuild your tree =)'


t = ['aardvark', 'antelope', 'bear', 'boar', 'buffalo', 'calf', 'cavy', 'cheetah', 'deer', 'dolphin', 'elephant',
     'fruitbat', 'giraffe', 'girl', 'goat', 'gorilla', 'hamster', 'hare', 'leopard', 'lion',
     'chicken', 'crow', 'dove', 'duck', 'flamingo', 'gull', 'hawk', 'kiwi', 'lark', 'pitviper', 'seasnake', 'slowworm',
    'bass', 'carp', 'catfish', 'chub', 'dogfish', 'haddock', 'frog', 'flea', 'gnat', 'honeybee', 'housefly', 'clam',
    'crab', 'crayfish', 'lobster', 'octopus']


test_samples = [item for item in zoo if item[0] in t]
control_samples = [item for item in zoo if item[0] not in t]


# test_samples = [zoo[i] for i in xrange(len(zoo)) if 0<=i<=20 or 41<=i<=50 or 61<=i<=62 or 66<=i<=71 or 79<=i<=80 or
#                 83<=i<=86 or 91<=i<=95]
#
# control_samples = [zoo[i] for i in xrange(len(zoo)) if 21<=i<=40 or 51<=i<=60 or 63<=i<=65 or 72<=i<=78 or 81<=i<=82 or
#                 87<=i<=90 or 96<=i<=100]


atrs = [i for i in xrange(1,17)]

decision_tree = build_tree(test_samples, atrs)

# for sample in test_samples:
#     print sample

print decision_tree

counter = 0
for sample in control_samples:
    # print sample[0], ' - ', get_type(sample,decision_tree), ' - ', sample[17]
    if get_type(sample,decision_tree) == sample[17]:
        counter +=1
    else:
        print sample[0], ' - ', get_type(sample,decision_tree), ' - ', sample[17]

print float(counter)/len(control_samples)*100

# print build_tree(test_samples, atrs)

# print control_samples


# for i in xrange(1,17):
#     print i, information_gain(zoo,i)

# res = [(i,information_gain(zoo,i)) for i in xrange(1,17)]
# res.sort(key = lambda x: x[1])
# atributes = [i[0] for i in res]
# print atributes









