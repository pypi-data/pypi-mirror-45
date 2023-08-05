# encoding: utf-8

class Condition(object):

    def __init__(self, name, operator, value, with_and=False):
        self.name     = name
        self.operator = operator
        self.value    = value
        self.with_and = with_and


    def __str__(self):
        q = '%s %s %s ' % (self.name, self.operator, self.value)
        if self.with_and:
            q = 'and ' + q
        return q



class Select(object):

    def __init__(self, table, columns='*', with_where=False):
        self.table      = table
        self.columns    = columns
        self.with_where = with_where

    def __str__(self):
        q = 'select %s from %s ' % (self.columns, self.table)
        if self.with_where:
            q += 'where '
        return q



class Query(object):

    def __init__(self):
        self.query = ''

    def __iadd__(self, v):
        self.query += str(v)
        return self
