#!/usr/bin/python

from dbexecute import grandlivre, loadJournal, strGrandLivre 

if __name__ == '__main__':
    result = grandlivre(loadJournal())
    print strGrandLivre(result).encode('utf-8')

