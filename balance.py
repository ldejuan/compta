#!/usr/bin/python
# coding: utf8 

from dbexecute import strBalance, balance, loadJournal
import argparse
if __name__ == '__main__':
    parser  = argparse.ArgumentParser(u'Balance depuis une date donnee')
    parser.add_argument('date',nargs= '?', help=u'date de début %Y%m%d')
    args = parser.parse_args()
    result = strBalance(balance(loadJournal(args.date)))
    print (result.encode('utf-8'))

