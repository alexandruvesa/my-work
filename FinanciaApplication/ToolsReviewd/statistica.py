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

def analizaRIR(pathOrig):
    workbook = load_workbook(filename = pathOrig)
    
    ProiectiiFinInvestitie = workbook['3A-Proiectii_fin_investitie']
    
    
    ### 3.Venituri din vanzari marfuri
    venitAn1= ProiectiiFinInvestitie['E73'] .value
    venitAn2 =  ProiectiiFinInvestitie['F73'] .value
    venitAn3=  ProiectiiFinInvestitie['G73'] .value

    coefAn1= analizaIndicator(venitAn1)
    coefAn2 = analizaIndicator(venitAn2)
    coefAn3= analizaIndicator(venitAn3)
        
    crestere_venituri = (coefAn1 + coefAn2 + coefAn3) *100
    
    cheltuieliMateriiPrimeAn1 = analizaIndicator(ProiectiiFinInvestitie['E79'].value)
    cheltuieliMateriiPrimeAn2=analizaIndicator(ProiectiiFinInvestitie['F79'].value)
    cheltuieliMateriiPrimeAn3=analizaIndicator(ProiectiiFinInvestitie['G73'].value)
    
    cheltuieliMarfuriAn1 = analizaIndicator(ProiectiiFinInvestitie['E84'].value)
    cheltuieliMarfuriAn2 =analizaIndicator( ProiectiiFinInvestitie['F84'].value)
    cheltuieliMarfuriAn3 = analizaIndicator(ProiectiiFinInvestitie['G84'].value)
    
    cheltuieliMaterialeAlteleAn1 = analizaIndicator(ProiectiiFinInvestitie['E85'].value)
    cheltuieliMaterialeAlteleAn1 = analizaIndicator(ProiectiiFinInvestitie['F85'].value)
    cheltuieliMaterialeAlteleAn1 =analizaIndicator( ProiectiiFinInvestitie['G85'].value)
    
    cheltuieliEnergieAn1 =analizaIndicator( ProiectiiFinInvestitie['E88'].value)
    cheltuieliEnergieAn2 =analizaIndicator( ProiectiiFinInvestitie['F88'].value)
    cheltuieliEnergieAn3 = analizaIndicator(ProiectiiFinInvestitie['G88'].value)
    
    cheltuieliSalarAn1 =  analizaIndicator(ProiectiiFinInvestitie['E98'].value)
    cheltuieliSalarAn2 =  analizaIndicator(ProiectiiFinInvestitie['F98'].value)
    cheltuieliSalarAn3 =  analizaIndicator(ProiectiiFinInvestitie['G98'].value)

    cheltuieliExploatareAn1 = analizaIndicator(ProiectiiFinInvestitie['E102'].value)
    cheltuieliExploatareAn2 = analizaIndicator(ProiectiiFinInvestitie['F102'].value)
    cheltuieliExploatareAn3 = analizaIndicator(ProiectiiFinInvestitie['G102'].value)
    
    crestereCheltuieli = (cheltuieliMateriiPrimeAn1 + cheltuieliMateriiPrimeAn2 + cheltuieliMateriiPrimeAn3 + \
        cheltuieliMarfuriAn1 +cheltuieliMarfuriAn2 +cheltuieliMarfuriAn3 + cheltuieliMaterialeAlteleAn1 + \
            cheltuieliEnergieAn1 + cheltuieliEnergieAn2 +  cheltuieliEnergieAn3 +  cheltuieliSalarAn1 + \
             cheltuieliSalarAn2 + cheltuieliSalarAn3 + cheltuieliExploatareAn1 +cheltuieliExploatareAn2+\
                 cheltuieliExploatareAn3)*100
    
    print("Ati avut o crestere pe venituri de {} %  si o crestere pe chelutuieli de {} %" .format(crestere_venituri ,crestereCheltuieli))

def set_arguments():
    # Set arguments
    ap = argparse.ArgumentParser(description='Statistics')

    ap.add_argument("-p", "--path", required=False, type=str)

    args = vars(ap.parse_args())
    return args

args = set_arguments()


    
analizaRIR(args["path"])  
