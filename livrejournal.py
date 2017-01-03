#!/usr/bin/python

from dbexecute import grandlivre, loadJournal,  strJournal 

if __name__ == '__main__':
    print strJournal(loadJournal()).encode('utf-8')

