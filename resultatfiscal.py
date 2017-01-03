#!/usr/bin/python
# coding: utf8 

from dbexecute import balance, loadJournal, resultatFiscal

if __name__ == '__main__':
    result = resultatFiscal(balance(loadJournal()))
    print (result)

