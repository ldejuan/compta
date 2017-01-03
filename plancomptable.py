#!/usr/bin/python
from dbexecute import planComptable, pretty_out

if __name__ == '__main__':
    result = planComptable()
    print (pretty_out(result))
