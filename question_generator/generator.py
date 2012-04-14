# Question Generator
# Reads the countries.db database to generate basic random questions.

# Author: Thibaut Labarre for OLPC UW club http://students.washington.edu/olpc/

import sqlite3 as lite
import sys,csv
import operator
import re

con = None

class Question:
    def __init__(self, idNum, text, answer, hints, rewards):
        self.idNum = idNum
        self.text = text
        self.answer = answer
        self.hints = hints
        self.rewards = rewards

    def console_print(self):
        answer = 'toto' # raw_input(self.text)
        print self.text

        if answer == self.answer:
            print 'Well done! It was ' + self.answer
        else:
            print 'Wrong... The right answer is ' + self.answer
        

class database:
    def __init__(self,database):
        self.con = lite.connect(database)

    def fill_database(self,csv_file):
        try:
            con = self.con
            
            cur = con.cursor()    

            cur.execute('DROP TABLE country')
            cur.execute('CREATE TABLE IF NOT EXISTS country (territory VARCHAR,totalkm VARCHAR,totalsqmi VARCHAR,landkm2 VARCHAR,landsqmi VARCHAR,waterkm2 VARCHAR,watersqmi VARCHAR,perwater VARCHAR,Christian VARCHAR,Muslim VARCHAR,Buddhist VARCHAR,Hindu VARCHAR,Others VARCHAR,Nonreligious VARCHAR,Population VARCHAR,CountryCode VARCHAR,LongName VARCHAR,Region VARCHAR,IncomeGroup VARCHAR,CurrencyUnit VARCHAR,Constitutionalform VARCHAR,Headofstate VARCHAR,Basisofexecutivelegitimacy VARCHAR)')

            reader = csv.reader(open(csv_file, "rb"))
            for territory,totalkm,totalsqmi,landkm2,landsqmi,waterkm2,watersqmi,perwater,Christian,Muslim,Buddhist,Hindu,Others,Nonreligious,Population,CountryCode,LongName,Region,IncomeGroup,CurrencyUnit,Constitutionalform,Headofstate,Basisofexecutivelegitimacy,null in reader:
                print territory
                cur.execute('INSERT OR IGNORE INTO country (territory,totalkm,totalsqmi,landkm2,landsqmi,waterkm2,watersqmi,perwater,Christian,Muslim,Buddhist,Hindu,Others,Nonreligious,Population,CountryCode,LongName,Region,IncomeGroup,CurrencyUnit,Constitutionalform,Headofstate,Basisofexecutivelegitimacy) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (unicode(territory),unicode(totalkm),unicode(totalsqmi),unicode(landkm2),unicode(landsqmi),unicode(waterkm2),unicode(watersqmi),unicode(perwater),unicode(Christian),unicode(Muslim),unicode(Buddhist),unicode(Hindu),unicode(Others),unicode(Nonreligious),unicode(Population),unicode(CountryCode),unicode(LongName),unicode(Region),unicode(IncomeGroup),unicode(CurrencyUnit),unicode(Constitutionalform),unicode(Headofstate),unicode(Basisofexecutivelegitimacy)))
                con.commit()

        except lite.Error, e:
            
            print "Error %s:" % e.args[0]
            sys.exit(1)
            

    def display_tables(self):
        con = self.con
        cur = con.cursor()    
        cur.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name;')
            
        for row in cur:
            print row[0]

    def display_tables(self):
        con = self.con
        cur = con.cursor()    
        cur.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY name;')
            
        for row in cur:
            print row[0]

    def display_table_fields(self,table_name):
        con = self.con
        cur = con.cursor()    
        cur.execute('PRAGMA table_info(' + table_name + ');')
            
        for row in cur:
            print row


    # Which is the biggest country between...
    def create_country_size_question(self):
        con = self.con
        cur = con.cursor()    
        cur.execute('SELECT * FROM country ORDER BY RANDOM() LIMIT 5;')

        countries = {}
        for row in cur:
            try:
                countries[row[0]] = float(row[1])
            except ValueError:
                countries[row[0]] = 0

        question = ''

        question += 'Between\n'

        for country in countries:
            question += ' - ' + country + '\n'

        question += 'which is the largest one?\n'

        biggestCountry = max(countries.iteritems(), key=operator.itemgetter(1))[0]

        return Question(0,question,biggestCountry,'','')



    # Which is the biggest country between...
    def create_country_religion_question(self):
        con = self.con
        cur = con.cursor()    
        cur.execute('SELECT territory,Christian,Muslim,Buddhist,Hindu,Others,Nonreligious FROM country ORDER BY RANDOM() LIMIT 1;')

        religions = ['Christian','Muslim','Buddhist','Hindu','Others','Non Religious']

        for row in cur:
            question = 'What is the religion of ' + row[0] + '?\n'
            for i in range(1,7):
                question += '- ' + religions[i-1] + '\n'

            maxPer = 0
            maxId = 0
            for i in range(1,7):
                parsedLine = re.search("(?P<number>\d+)",row[i])
                if parsedLine:
                    if int(parsedLine.group("number")) > maxPer:
                        maxPer = int(parsedLine.group("number"))
                        maxId = i

        answer = religions[maxId-1]

        return Question(0,question,answer,'','')


    def close_connection(self):
        if con:
            con.close()

db = database('countries.db')
# db.fill_database('countryfactsv2.csv')
db.display_tables()
db.display_table_fields('country')
# question = db.create_country_size_question()
question = db.create_country_religion_question()

question.console_print()

db.close_connection()
