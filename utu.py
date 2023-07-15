from pyodide.ffi import create_proxy

import pyodide

import js
import os
import csv

# todo: this should be a binary dump of a sqllite db
with open("signlist.tsv", "r") as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    cuneform = [r for r in reader if len(r['Unicode']) and r['worthington'] == 'TRUE']
    
print(cuneform[0])
print(f"loaded {len(cuneform)} characters")

def main():
    class DB:
        pointer = 0
        rota = 0

        def __init__(self):
            self.carousel = js.document.getElementById("mainCarousel")
            
            for idx, item in enumerate(self.carousel.getElementsByClassName("flash")):
                item.innerHTML = cuneform[idx]['Unicode'].split()[-1]

            

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

            next_card = cuneform[self.pointer]
            print (next_card)

            flashcard = event.relatedTarget.getElementsByClassName("flash")[0]
            flashcard.innerHTML = next_card['Unicode'].split()[-1]
        
            main_caption = event.relatedTarget.getElementsByClassName("carousel-caption")[0]
            header = main_caption.getElementsByClassName('caption-header')[0]
            details = main_caption.getElementsByClassName('caption-details')[0]
            header.innerHTML = next_card['Sign Name']
            details.innerHTML = next_card['MesZL']
    

    db_proxy = create_proxy(DB())
    proxy = create_proxy(db_proxy.test)

    carousel = js.document.getElementById("mainCarousel")
    carousel.addEventListener("slide.bs.carousel", proxy)
