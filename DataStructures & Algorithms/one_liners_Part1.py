# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 07:46:13 2021

@author: Alex
"""

import time

text = "Call me Ishamel. Some years ago - never mind how long precisely - having little or no money in my purse\
    and nothing particular to interest me on shore"
    
    
w = [[x for x in line.split() if len(x)>3] for line in text.split('\n')]


text_2 = ['lambda functions are anonymous functions.',
          'anonymous functions dont have a name.',
          'functions are objects in Python']*10000000



start = time.time()
mark_map = list(map(lambda s: (True,s) if 'anonymous' in s else(False,s),text_2))
print(time.time()-start)



start = time.time()

mark_list = [(True,s) if 'anonymous' in s else (False,s) for s in text_2 ]

print(time.time()-start)

letter_amazon = " We spent several years building our own database engine, Amazon Aurora, a fully-managed MySQL and PostgresSQL\
    with the same or better durability and availability as the commercial enginers, but at one tenth of the cost. We were\
        not surprised when this worked "
        
find = lambda x, q:x[x.find(q)-18:x.find(q)+18] if q in x else -1

find(letter_amazon, 'SQL')



companies = { "CoolCompany" : {'Alice':33, 'Bob':28, 'Frank':29},
             'CheapCompany':{'Ann':4, 'Lee':9, 'Chrisi':7},
                             'SOsoCompany':{'Esther':38,'Cole':8,'Paris':18}}

ilegal = [x for x in companies if any(y <9 for y in companies[x].values())]


columns_names = ['name', 'salary', 'job']
db_rows = [('Alice', 180000,'data scientist'),
           ('Bob', 99000, 'mid-level manager'),
           ('Frank', 87000, 'CEO' )]*3000000

start = time.time()
links = [dict(zip(columns_names,row))for row in db_rows]
print(time.time()-start)

start = time.time()
lista = []
for row in db_rows:
    lista.append(dict(zip(columns_names,row)))
print(time.time()-start)




