# -*- coding: utf-8 -*-

__author__ = 'nyash myash'

import math
import random

"""построить решающее дерево"""


file = open('/zoo.data.txt')

zoo = []

for l in file:
    item = l.strip().split(',')
    assert len(item) == 18
    zoo.append(item)

# считаем энтропию
def entropy(items):
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

def new_information_gain(items, i):
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
    return gain,groups


attr_names = ['name', 'hair', 'feathers', 'eggs', 'milk', 'airborne', 'aquatic', 'predator', 'toothed', 'backbone',
              'breathes', 'venomous', 'fins', 'legs', 'tail', 'domestic', 'catsize', 'type']

label_names = ['?', 'mammal', 'bird', 'reptile', 'fish', 'amphibian', 'insect', 'crustacean']


class Node:
    def __init__(self, label, attr = None, children=None):
        self.label = label
        self.attr = attr
        self.children = children

    def dump(self, level = 0):
        indent = '  ' * level
        if self.label:
            print '%s---->%s' %(indent,label_names[int(self.label)])
        else:
            print '%s%s?'%(indent,attr_names[self.attr])
            for v,t in self.children.iteritems():
                print '%s %s:'%(indent,v)
                t.dump(level+1)

    def guess(self,item):
        if self.label:
            return self.label
        v = item [self.attr]
        if v in self.children:
            return self.children[v].guess(item)
        return '0'


def select_label(items):
    # return  None if entropy(items) else 1
    assert len(items)
    l = items[0][17]
    for item in items[1:]:
        if item[17]!= l:
            return None
    return l

def select_attr(items):
    best_attr = 0
    best_gain = 0.0
    best_groups = {}
    for attr in xrange(1,17):
        gain,groups = new_information_gain(items, attr)
        if best_gain < gain:
            best_attr = attr
            best_gain = gain
            best_groups = groups
    return best_attr,best_groups


def learn(items):
    l = select_label(items)
    if l:
        return Node(l)
    else:
        attr, groups = select_attr(items)
        children = {}
        for v, g in groups.iteritems():
            children[v] = learn(g)
        return Node(None,attr,children)


# tree = learn(zoo[:80])
# tree.dump()

# for i in zoo[80:]:
#     l = tree.guess(i)
#     print '%s %s(%s)' %(i[0],label_names[int(l)], label_names[int(i[17])])


test = [random.choice(zoo) for i in xrange(80)]
tree = learn(test)

control = [item for item in zoo if item not in test]

for i in control:
    l = tree.guess(i)
    print '%s %s(%s)' %(i[0],label_names[int(l)], label_names[int(i[17])])





# --------------------------------------------------------------
# another variant



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
        # return 'unknown'
        return best_match(items)
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



#
# t = ['aardvark', 'antelope', 'bear', 'boar', 'buffalo', 'calf', 'cavy', 'cheetah', 'deer', 'dolphin', 'elephant',
#      'fruitbat', 'giraffe', 'girl', 'goat', 'gorilla', 'hamster', 'hare', 'leopard', 'lion',
#      'chicken', 'crow', 'dove', 'duck', 'flamingo', 'gull', 'hawk', 'kiwi', 'lark', 'pitviper', 'seasnake', 'slowworm',
#     'bass', 'carp', 'catfish', 'chub', 'dogfish', 'haddock', 'frog', 'flea', 'gnat', 'honeybee', 'housefly', 'clam',
#     'crab', 'crayfish', 'lobster', 'octopus']
#
#
# test_samples = [item for item in zoo if item[0] in t]
# control_samples = [item for item in zoo if item[0] not in t]


# test_samples = [zoo[i] for i in xrange(len(zoo)) if 0<=i<=20 or 41<=i<=50 or 61<=i<=62 or 66<=i<=71 or 79<=i<=80 or
#                 83<=i<=86 or 91<=i<=95]
#
# control_samples = [zoo[i] for i in xrange(len(zoo)) if 21<=i<=40 or 51<=i<=60 or 63<=i<=65 or 72<=i<=78 or 81<=i<=82 or
#                 87<=i<=90 or 96<=i<=100]


# atrs = [i for i in xrange(1,17)]
#
# decision_tree = build_tree(test_samples, atrs)

# for sample in test_samples:
#     print sample

# print decision_tree
#
# counter = 0
# for sample in control_samples:
#     # print sample[0], ' - ', get_type(sample,decision_tree), ' - ', sample[17]
#     if get_type(sample,decision_tree) == sample[17]:
#         counter +=1
#     else:
#         print sample[0], ' - ', get_type(sample,decision_tree), ' - ', sample[17]
#
# print float(counter)/len(control_samples)*100

# print build_tree(test_samples, atrs)

# print control_samples


# for i in xrange(1,17):
#     print i, information_gain(zoo,i)

# res = [(i,information_gain(zoo,i)) for i in xrange(1,17)]
# res.sort(key = lambda x: x[1])
# atributes = [i[0] for i in res]
# print atributes









