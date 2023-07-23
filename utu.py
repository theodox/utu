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


        def __init__(self, characters = 18):
            self.carousel = js.document.getElementById("mainCarousel")
            self.database = sqlite3.connect('cuneiform.db')
            self.cursor = self.database.cursor()
            r = self.cursor.execute(f'SELECT DISTINCT sign, borger FROM signs ORDER BY RANDOM() LIMIT {characters}')
            self.SIGNS = [self.get_character(c) for (c,*_) in r.fetchall()]
            self.pointer = 0

            self.always_on = False
            self.show_logograms = True
            self.show_syllables = True
  

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

        def toggle_logograms(self, event):
            self.show_logograms = event.target.checked
            for eachrow in self.carousel.getElementsByClassName('display-logograms'):
                if (self.show_logograms):
                    eachrow.classList.remove("collapse")
                else:
                    eachrow.classList.add("collapse")

        def toggle_syllables(self, event):
            self.show_syllables = event.target.checked
            for eachrow in self.carousel.getElementsByClassName('display-syllables'):
                if (self.show_syllables):
                    eachrow.classList.remove("collapse")
                else:
                    eachrow.classList.add("collapse")

        def toggle_always_on(self, event):
            self.always_on = event.target.checked
            for disp in self.carousel.getElementsByClassName('carousel-caption'):
                if self.always_on:
                    disp.classList.add("show")
                else:
                    disp.classList.remove("show")
 
           

        def transition(self, event):
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

            for sign_no in flashcard.getElementsByClassName("borger"):
                sign_no.innerHTML = next_card.borger

            glyph = flashcard.getElementsByClassName("flash")[0]
            glyph.innerHTML = next_card.sign


            for disp in flashcard.getElementsByClassName('carousel-caption'):
                if self.always_on:
                    disp.classList.add("show")
                else:
                    disp.classList.remove("show")
                
            for syl in flashcard.getElementsByClassName("syllables"):
                syl.innerHTML = ' '.join(next_card.syllables)

               
            for log in  flashcard.getElementsByClassName("logograms"):
                log.innerHTML = ' '.join((str(x) for x in next_card.logograms))

    db_proxy = create_proxy(DB())
    transition_proxy = create_proxy(db_proxy.transition)

    carousel = js.document.getElementById("mainCarousel")
    carousel.addEventListener("slide.bs.carousel", transition_proxy)

    toggle_s_proxy = create_proxy(db_proxy.toggle_syllables)
    syllableCheck = js.document.getElementById("showSyllables")
    syllableCheck.addEventListener('input', toggle_s_proxy)

    toggle_logo_proxy = create_proxy(db_proxy.toggle_logograms)
    logoCheck  = js.document.getElementById("showLogograms")
    logoCheck.addEventListener('input', toggle_logo_proxy)

    toggle_always_proxy = create_proxy(db_proxy.toggle_always_on)
    alwaysOnCheck  = js.document.getElementById("alwaysShow")
    alwaysOnCheck.addEventListener('change', toggle_always_proxy)


