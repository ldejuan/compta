#!/usr/bin/python
# coding: utf8 

from dbexecute import balance, loadJournal, resultatComptable

if __name__ == '__main__':
    result = resultatComptable(balance(loadJournal()))
    print (result)

