from math import *
from attributeclass import*
import random
import numpy as np

label = Attr('IsBadBuy', False, [0, 1])


def give_split(data, attr):
    zero_data = data[data["IsBadBuy"] == 0]
    one_data = data[data["IsBadBuy"] == 1]
    if (len(zero_data) == 0) | (len(one_data) == 0):
        attr.split = []
        return
    zero_mean = np.mean(np.array(zero_data[attr.name]))
    one_mean = np.mean(np.array(one_data[attr.name]))
    zero_std = np.std(np.array(zero_data[attr.name]))
    one_std = np.std(np.array(one_data[attr.name]))
    if zero_std == 0:
        zero_std = 0.1
    if one_std == 0:
        one_std = 0.1
    attr.split = [(zero_mean*one_std + one_mean*zero_std)/(zero_std + one_std)]
    return


def attr_slice(data, attr):
    if attr.if_cont:
        data_slice = [0]*(len(attr.split)+1)
        if len(attr.split) == 0:
            data_slice[0] = data
        else:
            try:
                data_slice[0] = data[data[attr.name] <= attr.split[0]]
            except:
                print(attr.split, attr.name)
            for i in range(len(attr.split)-1):
                data_slice[i+1] = data[np.array(data[attr.name] > attr.split[i]) & np.array(data[attr.name] <= attr.split[i+1])]
            data_slice[len(attr.split)] = data[data[attr.name] > attr.split[-1]]
    else:
        data_slice = []
        for i in range(len(attr.split)):
            data_slice.append(data[data[attr.name] == attr.split[i]])
    return data_slice


def entropy(data, attr):
    if len(data) == 0:
        return 0
    data_slice = attr_slice(data, attr)
    result = 0
    for s in data_slice:
        if len(s) != 0:
            prob = float(len(s))/len(data)
            result += -prob*log(prob, 2)
    return result


def information_gain(data, attr):
    post_entropy = 0
    data_slice = attr_slice(data, attr)
    for s in data_slice:
        post_entropy += entropy(s, label) * float(len(s)) / len(data)
    gain = entropy(data, label) - post_entropy
    return gain


def gain_ratio(data, attr):
    e = entropy(data, attr)
    if e == 0:
        return 0
    ratio = information_gain(data, attr)/e
    return ratio


def gini_gain(data, attr):
    data_slice = attr_slice(data, attr)
    post_gini = 0
    for s in data_slice:
        post_gini += gini_index(s) * float(len(s)) / len(data)
    reduction = gini_index(data) - post_gini
    return reduction


def gini_index(data):
    if len(data) == 0:
        return 0
    p0 = float(sum(data[label.name] == 0))/len(data)
    p1 = 1 - p0
    result = 1 - p0*p0 - p1*p1
    return result


def attribute_selection_method(data, attr_dict, method, criterion):
    if (sum(data["IsBadBuy"]) == len(data)) | (sum(data["IsBadBuy"]) == 0):
        return [False, []]
    score = {}
    for attr in attr_dict.values():

        if attr.if_cont:
            give_split(data, attr)

        if method == 1:
            score[attr.name] = information_gain(data, attr)
        elif method == 2:
            score[attr.name] = gini_gain(data, attr)
        elif method == 3:
            score[attr.name] = gain_ratio(data, attr)

    max_score = max(score.values())
    if max_score > criterion:
        if_split = True
        selected_name_list = [k for (k, v) in score.iteritems() if v == max_score]
        if len(selected_name_list)==1:
            selected_name = selected_name_list[0]
        else:
            selected_name = random.sample(set(selected_name_list), 1)[0]

        selected_attr = attr_dict[selected_name]
        selected_attr = Attr(selected_attr.name, selected_attr.if_cont, selected_attr.split)
        return [if_split, selected_attr]
    else:
        return[False, []]
