import numpy as np

def pearson (t_list):
    a_list = np.array([t[0] for t in t_list])
    b_list = np.array([t[1] for t in t_list])
    sum_ab = sum(a_list*b_list)
    n = len(t_list)
    mean_a = sum(a_list)*1.0/n
    mean_b = sum(b_list)*1.0/n
    sd_a = (sum((a_list-mean_a)**2)/n)**0.5
    sd_b = (sum((b_list-mean_b)**2)/n)**0.5
    return (sum_ab - n*mean_a*mean_b)/(n*sd_a*sd_b)

def check_corr (t_list):
    return abs(pearson (t_list))>0.5:
