from pyodide.ffi import create_proxy
import pyodide
import js
import os
import sqlite3
from dataclasses import dataclass
from typing import Sequence



def main():
    
    @dataclass
    class CuneiformSign:
        sign: str
        borger: str
        syllables: Sequence
        logograms: Sequence
        determinative: str = ''
    
    class DB:


        def __init__(self, characters = 12):
            self.carousel = js.document.getElementById("mainCarousel")
            self.database = sqlite3.connect('cuneiform.db')
            self.cursor = self.database.cursor()
            r = self.cursor.execute(f'SELECT DISTINCT sign, borger FROM signs ORDER BY RANDOM() LIMIT {characters}')
            self.SIGNS = [self.get_character(c) for (c,*_) in r.fetchall()]
            self.pointer = 0
  

        def get_character(self, char):
            syllabs = self.cursor.execute(
                ''' 
                SELECT syllable FROM 
                    syllabic
                WHERE
                    syllabic.sign = ?
                ''',
                (char, )
            ).fetchall()

            logograms = self.cursor.execute(
                '''
                SELECT logogram FROM 
                    logographic
                WHERE
                    logographic.sign = ?
                ''', (char,)
            ).fetchall()

            signinfo = self.cursor.execute(
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


        def test(self, event):
            t = event.to
            f = event.from_
            delta = t - f
            if abs(delta) == 1:
                self.pointer += delta
            else:
                if t < f:
                    self.pointer += 1
                else:
                    self.pointer -= 1

            self.pointer %= len(self.SIGNS)

            next_card =self.SIGNS[self.pointer]

            flashcard = event.relatedTarget
            glyph = flashcard.getElementsByClassName("flash")[0]
            glyph.innerHTML = next_card.sign


            for disp in flashcard.getElementsByClassName('card-body'):
                js.console.log (disp)
                

            for syl in flashcard.getElementsByClassName("syllables"):
                js.console.log(syl)
                syl.innerHTML = ' '.join(next_card.syllables)
            
            for log in  flashcard.getElementsByClassName("logograms"):
                js.console.log(log)
                log.innerHTML = ' '.join((str(x) for x in next_card.logograms))

    db_proxy = create_proxy(DB())
    proxy = create_proxy(db_proxy.test)

    carousel = js.document.getElementById("mainCarousel")
    carousel.addEventListener("slide.bs.carousel", proxy)

