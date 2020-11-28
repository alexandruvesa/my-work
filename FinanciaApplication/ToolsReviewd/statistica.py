# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 18:34:26 2020

@author: alexandru.vesa
"""


import pandas as pd
from openpyxl.utils import FORMULAE  

from openpyxl import load_workbook , Workbook
import xlwings as xw
import argparse


def analizaIndicator(indicator):

    if indicator is int:
        pass
    else:
        splitString = indicator.split("*")[-1].split('+')[0]
                    
    return float(splitString)

def analiza_venituri_fara_investitie(pathOrig):
    
    workbook_value=xw.App(visible=False)
    workbook_value = xw.Book(pathOrig)
    
    cifra_afaceri = workbook_value.sheets['1B-ContPP'].range('C6').value
    #Venituri fara investitie
    an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D17').value
    an_implementare = an_implementare /1.19
    
    an1_fara_investitie =  workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E17').value
    an1_fara_investitie = an1_fara_investitie /1.19
    
    an2_fara_investitie =  workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F17').value
    an2_fara_investitie = an2_fara_investitie /1.19
    
    an3_fara_investitie =  workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G17').value
    an3_fara_investitie = an3_fara_investitie /1.19
       
    
    
    crestere_an_implementare = (an_implementare * 100) / cifra_afaceri
    crestere_an1_fara_investitie = (an1_fara_investitie*100) / cifra_afaceri
    crestere_an2_fara_investitie = (an2_fara_investitie*100)/cifra_afaceri
    crestere_an3_fara_investitie = (an3_fara_investitie*100)/cifra_afaceri

    
    crestere_venituri_fara_investitie = crestere_an_implementare/100 + crestere_an1_fara_investitie/100 + crestere_an2_fara_investitie/100  + crestere_an3_fara_investitie/100
    workbook_value.close()
    return crestere_venituri_fara_investitie
    
def analiza_venituri_cu_investitie(pathOrig):
    workbook_value=xw.App(visible=False)
    workbook_value = xw.Book(pathOrig)
    
    cifra_afaceri = workbook_value.sheets['1B-ContPP'].range('C6').value

    
    an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D73').value
    an_implementare = an_implementare /1.19
    
    an1_cu_investitie =  workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E73').value
    an1_cu_investitie = an1_cu_investitie /1.19
    
    an2_cu_investitie =  workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F73').value
    an2_cu_investitie = an2_cu_investitie /1.19
    
    an3_cu_investitie =  workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G73').value
    an3_cu_investitie = an3_cu_investitie /1.19
    
    crestere_an_implementare = (an_implementare * 100) / cifra_afaceri
    crestere_an1_cu_investitie = (an1_cu_investitie*100) / cifra_afaceri
    crestere_an2_cu_investitie = (an2_cu_investitie*100)/cifra_afaceri
    crestere_an3_cu_investitie = (an3_cu_investitie*100)/cifra_afaceri
    
    crestere_venituri_cu_investitie = crestere_an_implementare/100 + crestere_an1_cu_investitie/100 + crestere_an2_cu_investitie/100  + crestere_an3_cu_investitie/100
    workbook_value.close()

    return crestere_venituri_cu_investitie


def analiza_cheltuieli_fara_investitie(pathOrig):
    
    workbook_value=xw.App(visible=False)
    workbook_value = xw.Book(pathOrig)
    
    #Materii prime
    cheltuieli_contPP_materii_prime = workbook_value.sheets['1B-ContPP'].range('C14').value + workbook_value.sheets['1B-ContPP'].range('C15').value
    
    cheltuieli_materii_prime_an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D23').value /1.19
    cheltuieli_an_1_materii_prime = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E23').value /1.19
    cheltuieli_an_2_materii_prime = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F23').value /1.19
    cheltuieli_an_3_materii_prime = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G23').value /1.19

    crestere_an_implementare_materii_prime = (cheltuieli_materii_prime_an_implementare * 100) / cheltuieli_contPP_materii_prime
    crestere_an1_materii_prime = (cheltuieli_an_1_materii_prime*100) / cheltuieli_contPP_materii_prime
    crestere_an2_materii_prime = (cheltuieli_an_2_materii_prime*100) / cheltuieli_contPP_materii_prime
    crestere_an3_materii_prime = (cheltuieli_an_3_materii_prime*100) / cheltuieli_contPP_materii_prime
    
    #Marfuri
    cheltuieli_contPP_marfuri = workbook_value.sheets['1B-ContPP'].range('C17').value

    cheltuieli_marfuri_an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D28').value /1.19
    cheltuieli_an_1_marfuri= workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E28').value /1.19
    cheltuieli_an_2_marfuri = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F28').value /1.19
    cheltuieli_an_3_marfuri = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G28').value /1.19

    crestere_an_implementare_marfuri = (cheltuieli_marfuri_an_implementare * 100) / cheltuieli_contPP_marfuri
    crestere_an1_marfuri = (cheltuieli_an_1_marfuri*100) / cheltuieli_contPP_marfuri
    crestere_an2_marfuri= (cheltuieli_an_2_marfuri*100) / cheltuieli_contPP_marfuri
    crestere_an3_marfuri = (cheltuieli_an_3_marfuri*100) / cheltuieli_contPP_marfuri
    
    #Energia 
    cheltuieli_contPP_energie = workbook_value.sheets['1B-ContPP'].range('C16').value
    
    cheltuieli_energie_an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D32').value /1.19
    cheltuieli_an_1_energie= workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E32').value /1.19
    cheltuieli_an_2_energie = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F32').value /1.19
    cheltuieli_an_3_energie = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G32').value /1.19

    crestere_an_implementare_energie = (cheltuieli_energie_an_implementare * 100) / cheltuieli_contPP_energie
    crestere_an1_energie  = (cheltuieli_an_1_energie *100) / cheltuieli_contPP_energie
    crestere_an2_energie = (cheltuieli_an_2_energie *100) / cheltuieli_contPP_energie
    crestere_an3_energie  = (cheltuieli_an_3_energie *100) / cheltuieli_contPP_energie
    
    #Exploatare
    cheltuieli_contPP_exploatare = workbook_value.sheets['1B-ContPP'].range('C22').value
    
    cheltuieli_exploatare_an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D46').value /1.19
    cheltuieli_an_1_exploatare= workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E46').value /1.19
    cheltuieli_an_2_exploatare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F46').value /1.19
    cheltuieli_an_3_exploatare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G46').value /1.19

    crestere_an_implementare_exploatare = (cheltuieli_exploatare_an_implementare * 100) / cheltuieli_contPP_exploatare
    crestere_an1_exploatare  = (cheltuieli_an_1_exploatare *100) / cheltuieli_contPP_exploatare
    crestere_an2_exploatare = (cheltuieli_an_2_exploatare *100) / cheltuieli_contPP_exploatare
    crestere_an3_exploatare  = (cheltuieli_an_3_exploatare *100) / cheltuieli_contPP_exploatare
    
    #Financiare
    cheltuieli_contPP_Asigurare  = workbook_value.sheets['1B-ContPP'].range('C36').value
    
    cheltuieli_Asigurare_an_implementare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('D50').value 
    cheltuieli_an_1_Asigurare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('E50').value 
    cheltuieli_an_2_Asigurare  = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('F50').value 
    cheltuieli_an_3_Asigurare = workbook_value.sheets['3A-Proiectii_fin_investitie'].range('G50').value 

    crestere_an_implementare_Asigurare  = (cheltuieli_Asigurare_an_implementare * 100) / cheltuieli_contPP_Asigurare 
    crestere_an1_Asigurare  = (cheltuieli_an_1_Asigurare  *100) / cheltuieli_contPP_Asigurare 
    crestere_an2_Asigurare = (cheltuieli_an_2_Asigurare  *100) / cheltuieli_contPP_Asigurare 
    crestere_an3_Asigurare   = (cheltuieli_an_3_Asigurare  *100) / cheltuieli_contPP_Asigurare 
    
    
    
    #Suma cresteri
    crestere_cheltuieli_materii_prime = crestere_an_implementare_materii_prime/1000+crestere_an1_materii_prime/100+crestere_an2_materii_prime/100+crestere_an3_materii_prime/100
    crestere_cheltuieli_marfuri = (crestere_an_implementare_marfuri/1000+crestere_an1_marfuri/100+crestere_an2_marfuri/100+crestere_an3_marfuri/100)
    crestere_cheltuieli_energie = (crestere_an_implementare_energie/1000+crestere_an1_energie/100+crestere_an2_energie/100+crestere_an3_energie/100)
    crestere_cheltuieli_exploatare = (crestere_an_implementare_exploatare/1000 +crestere_an1_exploatare/100 +crestere_an2_exploatare/100 +crestere_an3_exploatare/100 )
    crestere_cheltuieli_financiare = (crestere_an_implementare_Asigurare +crestere_an1_Asigurare +crestere_an2_Asigurare +crestere_an3_Asigurare )/1000
    
    crestere_finala = crestere_cheltuieli_materii_prime + crestere_cheltuieli_marfuri + crestere_cheltuieli_energie + crestere_cheltuieli_exploatare + crestere_cheltuieli_financiare
    workbook_value.close()
    return crestere_finala
        
    
pathOrig = r'C:\\Users\\alexandru.vesa\\Desktop\\Research\\New_Personal_Program_DL_Programming\\GitMy\\my-work\\FinanciaApplication\\21.11.20\\SideFINAL.xlsx'
crestere_venituri_fara_investitie = analiza_venituri_fara_investitie(pathOrig)
crestere_cheltuieli_fara_investitie = analiza_cheltuieli_fara_investitie(pathOrig)
crestere_venituri_cu_investitie = analiza_venituri_cu_investitie(pathOrig)
        
    
    

# def set_arguments():
#     # Set arguments
#     ap = argparse.ArgumentParser(description='Statistics')

#     ap.add_argument("-p", "--path", required=False, type=str)

#     args = vars(ap.parse_args())
#     return args

# args = set_arguments()


    
# analizaRIR(args["path"])  
