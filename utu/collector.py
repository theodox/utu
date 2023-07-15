import requests
import bs4
import unicodedata
import re
import csv

if __name__ == '__main__':
    url = 'http://home.zcu.cz/~ksaskova/ListOfCuneiformSigns.html'
    #header = {'Accept-encoding': 'utf-16'}
    r = requests.request('GET', url)# headers=header)
    print (r.headers)
    p = bs4.BeautifulSoup(r.content, 'html.parser', from_encoding="iso-8859-8")


    table = p.find('table')
    rows = iter(table.find_all('tr'))
    cols = (r.find_all('td') for r in rows)

    def sanitize(t):
        return t.strip().replace("\n", " ").replace("\t", "")

    with open ("ksaskova.csv", "wt", encoding='utf-8') as output:
        w = csv.writer(output)
    
        for item in cols:

            char = sanitize(item[0].text)

            name = sanitize(item[2].find('b').text)


            borger = sanitize(item[3].text)
            compound = len(char) > 1
            unicode = " & ".join([f"u+{'%04x' % ord(c)}".upper() for c in char])

            #parse out the sumerogram list, which has inline notes
            doubtful = item[2].find_all('p')[1].text.strip()  # raw text
            doubtful = doubtful.replace('\n', '').replace('\t', '').replace(";", ",")[1:-1]  # remove white space
            doubtful = re.sub("\(.*\)", "", doubtful)
            raw_sumerograms = (a.strip() for a in doubtful.split(",") if a)
            fix_crosses = (t.replace("x ", " x ") for t in raw_sumerograms)
            fix_over = (t.replace("over", " over ").replace("crossing", " crossing ") for t in fix_crosses)
            skip_refs = (t for t in fix_over if not ":" in t)
            not_esd = (t for t in skip_refs if t not in ('ePSD', 'Akkadian Dictionary'))
            #sumerograms = list(not_esd)


            
        
            # d_meanings = doubtful_text.split(",")
            # d_meanings_all = [m.partition("(")[0].strip() for m in d_meanings]
            # d_meanings_all = [j + "?" for j in d_meanings_all if j]


            record =  [char, name, borger, unicode, compound]
            record.extend(not_esd)
            print (record)
            w.writerow(record)