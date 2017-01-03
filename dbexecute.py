#!/usr/bin/python
#@brief Database usage of comptability
#@brief Name of comptability : compta_2015

DBCOMPTA ='compta_2016'

import sys,readline
import json, datetime
import pymongo as mg
from bson import json_util

def usage():
    pass

def livrejournal(journal):
    return journal

def resultatFiscal(Ibalance):
    desc2035 ={ 
        '706' : '1', 
        '606' : '8', 
        '6132': '15',
        '6251':'23',
        '6256':'24',
        '6451':'25',
        '6234':'26',
        '626':'27'
    }
    result  = {}
    for key, item in desc2035.iteritems() : 
        result[item] = 0.

    for compte, valeur in Ibalance.iteritems():
       for  key,item in desc2035.iteritems():
            if key in compte :
                result[item] += abs(valeur['DEBITEUR'] - valeur['CREDITEUR'])
                break
    return result

def resultatComptable(Ibalance):
    result = 0
    for compte, valeur in Ibalance.iteritems():
        if compte[0] in ['6','7']:
            result += valeur['CREDITEUR'] - valeur['DEBITEUR']
    return result

def balance(journal):
    plan = planComptable()
    comptes = list(plan.keys())
    comptes.sort()
    result = {}
    for compte, desc in plan.iteritems():
        v_debiteur = 0
        v_crediteur= 0
        for value in journal:
            for debiteur in value['DEBITEURS']:
                if debiteur['COMPTE'] == compte:
                    v_debiteur += debiteur['MONTANT']
            for crediteur in value['CREDITEURS']:
                if crediteur['COMPTE'] == compte:
                    v_crediteur += crediteur['MONTANT']
            result[compte] = {
                'DESC' : desc,
                'DEBITEUR' : v_debiteur,
                'CREDITEUR' : v_crediteur
            }
    return result
def strBalance(resBalance):
    result ='|COMPTE |DEBITEUR |CREDITEUR|DESCRIPTION|\n'
    comptes = resBalance.keys()
    comptes.sort()
    for c in comptes:
        b=resBalance[c]
        result += '|{0:<7}|{1:9.2f}|{2:9.2f}|{3:<20}|\n'.format(c,\
            b['DEBITEUR'],\
            b['CREDITEUR'],b['DESC'])

    return result
def extraitOrdone(journal):
    result = journal.keys()
    result.sort()
    return result

def extraitCompte(journal, inputCompte):
    result = []
    solde_d = 0.
    solde_c = 0.
    for value in journal:
        addone = {}
        for debiteur in value['DEBITEURS']:
            if debiteur['COMPTE'] == inputCompte:
                solde_d +=  debiteur['MONTANT']
                addone = {
                    'DATE' : value['DATE'],
                    'DESC' : value['DESC'],
                    'DEBIT' : debiteur['MONTANT'],
                    'CREDIT' : 0.,
                    'SOLDE_D' : solde_d,
                    'SOLDE_C' : solde_c
                }
        if len(addone) == 0:
            for crediteur in value['CREDITEURS']:
                if crediteur['COMPTE'] == inputCompte:
                    solde_c += crediteur['MONTANT']
                    addone = {
                        'DATE' : value['DATE'],
                        'DESC' : value['DESC'],
                        'DEBIT' : 0.,
                        'CREDIT' : crediteur['MONTANT'],
                        'SOLDE_D' : solde_d,
                        'SOLDE_C' : solde_c
                     }
        if len(addone) != 0:
            result.append(addone)

    return result

def strExtraitCompte(dExtraitCompte):
    result = ""
    keys = ['DATE', 'DEBIT', 'CREDIT', 'SOLDE_D', 'SOLDE_C', 'DESC']
    formatkeys = ['%8s','%9.2f','%9.2f','%9.2f','%9.2f','%s']
    formatentete= ['%8s','%9s','%9s','%9s','%9s','%s']
    entete = '|'.join([f%k for f,k in zip(formatentete,keys)])
    result += '|' + entete + '|\n'

    for l in dExtraitCompte:
        result += '|' + '|'.join([f%l[k] for f,k in zip(formatkeys,keys)]) + '|\n'
    
    return result

def grandlivre(journal):
    result = {}
    comptes = planComptable()
    for compte, desc in comptes.iteritems():
        result[compte] = {'DESC': desc , 'VALUES' : extraitCompte(journal,compte)}
    return result

def strGrandLivre(outGrandLivre):
    result = ''
    comptes = outGrandLivre.keys()
    comptes.sort()

    for c in comptes:
        result += '---------- %s: %s ----------\n'%(c,outGrandLivre[c]['DESC'])
        result += strExtraitCompte(outGrandLivre[c]['VALUES'])

    return result 
def testError(entree):
    debiteurs = [debiteur['COMPTE'] for debiteur in entree['DEBITEURS']]
    crediteurs = [crediteur['COMPTE'] for crediteur in entree['CREDITEURS']]
    if len(debiteurs) != len(set(debiteurs)):
        print ('%s : Erreur : Les comptes debiteurs ne sont pas uniques')
    if len(crediteurs) != len(set(crediteurs)):
        print ('%s : Erreur : Les comptes crediteurs ne sont pas uniques')
    solde_d = sum([debiteur['MONTANT'] for debiteur in entree['DEBITEURS']])
    solde_c = sum([crediteur['MONTANT'] for crediteur in entree['CREDITEURS']])
    if solde_c != solde_d:
        print('Erreur : Les soldes debiteurs et crediteurs ne sont pas pareils')

def testJournal(journal):
    for entree in journal:
        testError(entree)

def pretty_out(catalogue):
    return json.dumps(catalogue, default=json_util.default, sort_keys = True, indent = 4, separators = (',',': '))

def planComptable():
    dbCompta = mg.MongoClient()[DBCOMPTA]
    dbplanComptable = dbCompta['planComptable'].find({},{'_id':0})
    result = {}
    for c in dbplanComptable:
        result.update(c)
    return result

def loadJournal(startDate = None):
    dbCompta = mg.MongoClient()[DBCOMPTA]
    if startDate is None:
        dbjournal = dbCompta['journal'].find({},{'_id':0}).sort('DATE')
    else:
        if not isinstance(startDate, datetime.datetime):
            startDate = datetime.datetime.strptime(startDate, "%Y%m%d")
        dbjournal = dbCompta['journal'].find({"DATE":{"$gte":startDate}}).sort('DATE')
    journal = [ e for e in dbjournal]
    for e in journal:
        e['DATE'] = e['DATE'].strftime('%Y%m%d')
    return journal

def strJournal(journal):
    result = ''
    for e in journal:
        result += e['DATE'] +  ':' + e['DESC']+ '\n'
        m_debiteur = 0.
        m_crediteur =0.
        for d in e['DEBITEURS']:
            result +=\
            '|{0:<7}|{1:<7}|{2:9.2f}|{3:<9}|\n'.format(d['COMPTE'],'',d['MONTANT'],'')
            m_debiteur += d['MONTANT']
        for d in e['CREDITEURS']:
            result +=\
            '|{0:<7}|{1:<7}|{2:<9}|{3:9.2f}|\n'.format('', d['COMPTE'],'',d['MONTANT'])
            m_crediteur += d['MONTANT'] 
 
        result += '|{0:<15}|{1:9.2f}|{2:9.2f}|\n\n'.format('Total', m_debiteur,m_crediteur)

    return result

def inputdate():
    while 1:
        d = raw_input('Date %Y%m%d:\n')
        try:
            dt = datetime.datetime.strptime(d,'%Y%m%d')
            return dt
        except ValueError:
            print('Erreur de date %s: Ressayer\n '%d) 
        except:
            print('Erreur de date %s: Ressayer\n '%d)

def inputDocuments():
    while 1:
        inputDocs = raw_input('Documents,')
        docs = inputDocs.split(',')
        return docs

def inputComptes(dbComptes, typeCompte = 'DEBITEURS'):
    while 1:
        try:
            entrees = raw_input('Entree %s:Montant,%s:Montant...\n'%(typeCompte, typeCompte))
            compteMontants = entrees.split(',')
            result =[]
            for c in compteMontants:
                c1,m1 = c.split(':')
                if c1 not in dbComptes:
                    raise Exception ('Compte %s non defini'%c1)
                result.append({ "COMPTE"  : c1,
                               "MONTANT" : float(m1)
                    })
            return result
        except Exception as inst :
            print ('Erreur %s: Ressayer \n'%inst.args)
class DefaultCompte():
    
    def __init__(self,dbComptes):
        self._comptes = dbComptes
    
    def complete(self, text,state):
        if state == 0:
            if text:
                self.matches = [c for c in self._comptes if c and
                c.startswith(text)]
            else:
                self.matches = self._comptes[:]
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

def inputNumCompte(dbComptes):
    while 1:
        compte = raw_input('Numero Compte Taille 7\n')
        if len(compte) == 7 and compte not in dbComptes:
            return compte
        print('taille  doit etre egale a 7:')

def entreeCompte():
    dbCompta = mg.MongoClient()[DBCOMPTA]
    dbComptes = planComptable().keys()
    dbComptes.sort()
    compte = inputNumCompte(dbComptes)
    desc = raw_input('Description\n')
    result = dbCompta.planComptable.insert_one({
            compte : desc.upper()
        })
    print ('Sauve: %s, %s'%(result.inserted_id, compte))

def entreecriture():
    dbCompta = mg.MongoClient()[DBCOMPTA]
    dbComptes = planComptable().keys()
    dbComptes.sort()
    d = inputdate()
    desc =  raw_input('Description\n ')
    docs = inputDocuments()
    readline.set_completer(DefaultCompte(dbComptes).complete)
    readline.parse_and_bind('tab: complete')
    debiteurs = inputComptes(dbComptes, 'DEBITEURS') 
    crediteurs = inputComptes(dbComptes, 'CREDITEURS')

    ecriture = {
        "DATE" : d,
        "DESC" : desc,
        "DOCS" : docs,
        "DEBITEURS" : debiteurs,
        "CREDITEURS": crediteurs,
        "TYPE" : "MANUAL" 
    }

    result = dbCompta.journal.insert_one(ecriture)
    print 'id: %s \n, Entree: %s\n'%(result.inserted_id, ecriture)
