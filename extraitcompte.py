#!/usr/bin/python

from dbexecute import extraitCompte, loadJournal, strExtraitCompte 

import sys
def usage():
    print('extraitdecompte NUMEROCOMPTE')

if __name__ == '__main__':
    if len(sys.argv) !=2:
        usage()
        exit(0)
    compte = sys.argv[1]
    print ('-------------Extrait de Compte :%s -------------'%compte)
    result = extraitCompte(loadJournal(),compte)
    print (strExtraitCompte(result).encode('utf-8'))

