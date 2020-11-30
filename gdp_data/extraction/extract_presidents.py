# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 09:46:30 2020

@author: 01est
"""

from bs4 import BeautifulSoup
import urllib
import re
from datetime import datetime, timedelta
import pandas as pd
import json

#downloading united states presidents from wikipedia
us_p_ws = r'https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States'
us_p_html = urllib.request.urlopen(us_p_ws)
us_p_soup = BeautifulSoup(us_p_html, 'lxml')

#extracting html table
table = us_p_soup.find_all('table')[1]

#extracting information in table
presidents = {}
for tr in table.find_all('tr'):
    tds = tr.find_all('td')
    
    #the desired information is contained within the tds that have a len(td) > 4
    if len(tds) > 4:
        for td in tds:
            while td == True: 
                #separating term_start and term_end
                information = td.text.split('–')
                #cleaning date string
                term_start = re.sub(r'(\[.\])$', '', information[0])
                #date conversion
                term_start = str(datetime.strptime(term_start, "%B %d, %Y").date())
     
                term_end = information[1].strip()
                #date conversion to handle the term for the last presidency
                try:
                    term_end = str(datetime.strptime(term_end, "%B %d, %Y").date())
                except:
                    term_end = str('2021-01-22')
            
            #scraping precidency number
            presidentNum = tr.find('th').text.strip()
            #scraping president's name
            name = re.sub(r'(\[.\])$|(\n)$','', tds[2].text)
            #scraping political party
            political_party = re.sub(r'(\[.\])$|(\n)$','', tds[4].text)
            #creating dictionary (unique keys)
            presidents[name] = {
                    'number': presidentNum,
                    'start': term_start,
                    'end': term_end,
                    'party': political_party
                    }
            
def export_presidents():
    '''stores list of presidents in a .json file'''
    with open('presidents.json', 'w') as outfile:
        json.dump(presidents, outfile)
        
def read_presidents():
    '''reads and builds pd.dataframe() from the .json files containing
    the list of presidents'''
    
    with open('presidents.json', 'r') as infile:
        return pd.DataFrame(json.load(infile))

if __name__=="__main__":
    
    #export presidents to a .json file
    export_presidents()
    
    #reads and builds president data
    a = read_presidents()
    
    
    
        
        