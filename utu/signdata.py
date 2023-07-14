import csv
import sqlite3
import os
import string
from dataclasses import dataclass
from typing import Tuple

@dataclass
class CuneiformSign:
    sign: str
    borger: str
    syllables: Tuple
    logograms: Tuple
    determinative: str = ''

os.remove("cuneiform.db")

db = sqlite3.connect("cuneiform.db")
cursor = db.cursor()
cursor.execute('''

    CREATE TABLE signs (
        sign VARCHAR(8) NOT NULL UNIQUE PRIMARY KEY,
        name VARCHAR(16) NOT NULL,
        borger VARCHAR(8),
        determinative VARCHAR(72),
        correct INTEGER DEFAULT 0,
        incorrect INTEGER DEFAULT 0
        );
''')
cursor.execute('''
    CREATE TABLE syllables(
        syllable VARCHAR(16) NOT NULL UNIQUE PRIMARY KEY
    );
''')
cursor.execute('''
    CREATE TABLE logograms(
        logogram VARCHAR(16) NOT NULL UNIQUE PRIMARY KEY
    );
''')

cursor.execute('''
    CREATE TABLE syllabic (
        id INTEGER PRIMARY KEY,
        sign INTEGER,
        syllable INTEGER,
        FOREIGN KEY(sign) REFERENCES signs(id),
        FOREIGN KEY(syllable) REFERENCES syllables(id)
    )
''')

cursor.execute('''
    CREATE TABLE logographic (
        id INTEGER PRIMARY KEY,
        sign INTEGER,
        logogram INTEGER,
        FOREIGN KEY(sign) REFERENCES signs(id),
        FOREIGN KEY(logogram) REFERENCES logograms(id)
    )'''
)

SUB = 0x2080 # delta between unicode digit and subscript
def subscripted(str):
    if not str:
        return str
    if '/' in str: return str
    has_char = any (d not in string.digits for d in str)
    if not has_char: return str

    return  ''.join(chr(SUB + int(c)) if c in string.digits else c for c in str)

def token_args(*args):
    return ','.join(['?']*len(args))

with open("sourcedata.tsv", "rt", encoding='utf-8') as srcfile:
    reader = csv.DictReader(srcfile, delimiter='\t')
    for r in reader:


        if r['syllabic']:

            det = ''
            if r['PREFIX']:
                det = r['PREFIX']
            elif r['POSTFIX']:
                det = "+" + r['POSTFIX']
            # add the main ref
            cursor.execute('''
                INSERT INTO signs
                (name, sign, borger, determinative)
                values
                (?, ?, ?, ?)
            ''', (r['name'], r['sign'], r['meszl'], det))

        

            # insert syllables
            tokens =  [x.strip() for x in r['syllabic'].split(",")]
            tokenized = ((a,) for a in tokens if a)
            cursor.executemany('''INSERT OR IGNORE INTO syllables (syllable) values ( ?)''', tokenized)
        
            selector = (f'''
            SELECT * FROM syllables WHERE syllable in ({token_args(*tokens)})''')#, tokens).fetchall()

            syllabs = [(r['sign'], t) for t in tokens]

            for s in syllabs:
                cursor.execute('''INSERT INTO syllabic(sign, syllable) VALUES (?,?)''', s)

            logograms = [subscripted(r['name'].strip())]
            for num in range(1, 14):
                raw = r[f'sumerogram{num}'].strip().replace('  ', ' ')
                if raw:
                    log = subscripted(raw)
                    if log:
                        logograms.append(log)
            cursor.executemany('''INSERT OR IGNORE INTO logograms (logogram) values (?)''', ((k,) for k in logograms))
    
            for j in logograms:
                cursor.execute('''INSERT INTO logographic(sign, logogram) VALUES (?,?)''', (r['sign'], j))

def get_character(char):
    syllabs = cursor.execute(
        ''' 
        SELECT syllable FROM 
            syllabic
        WHERE
             syllabic.sign = ?
        ''',
        (char, )
    ).fetchall()

    logograms = cursor.execute(
        '''
          SELECT logogram FROM 
            logographic
        WHERE
             logographic.sign = ?
        ''', (char,)
    ).fetchall()

    signinfo = cursor.execute(
        '''
        SELECT * from  signs
        WHERE sign = ?
        ''', (char,)
    ).fetchone()

    return CuneiformSign(
        signinfo[0],
        signinfo[2],
        tuple(k[0] for k in syllabs),
        tuple(k[0] for k in logograms),
        signinfo[3]
    )


def get_random():
    result = cursor.execute('select sign from signs order by RANDOM() limit 1').fetchone()
    print(get_character(result[0]))

get_random()
get_random()
get_random()

print (get_character('𒊩'))

def find_syllable(syllab):
    r = cursor.execute('''
        SELECT sign from syllabic
        where syllable glob ?
    ''', (syllab,)).fetchall()
    return [a[0] for a in r]

print (find_syllable('*al'.lower()))