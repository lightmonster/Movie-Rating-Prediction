__author__ = 'swangust'

'''
Define the class object to store attribute information
'''


class Attr:
    def __init__(self, name, if_cont, split):
        self.name = name
        self.if_cont = if_cont
        self.split = split

'''
name is a string representing the name of the attribute, e.g.:make
if_cont is a boolean showing if the attribute is continuous or not.
domain stores
    either:
    list all the possible value(strings) for a discrete attribute
    or
    empty list for continuous attributes(since there is no need for representing its range)
    or
    list of real numbers indicating the method for splitting
'''
