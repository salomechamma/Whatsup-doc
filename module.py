"""Module including all functions called by server.py in each routes"""

import os
from jinja2 import StrictUndefined


import requests
from sys import argv
from pprint import pprint
import json
import server



def print_nicely_results(list_results):
    """Fname Lname of results."""
    pprint(list_results)

     

def unique_dico(list_results):
    """ Return list of unique dictionnaries (unique physician ids) """
    id_list = [] #list to store unique physician ids
    new_list = [] # list to store unique dictionnaries and function to return it
    for dico in list_results:
        if int(dico['physician_profile_id']) in id_list:
            pass
        else:
            id_list.append(int(dico['physician_profile_id']))
            new_list.append(dico)
            print id_list
           
    return new_list
     


def total_payments(list_payments):
    """ Return float corresponding to toal amounts received by this doctor """
    t = 0
    for dic in list_payments:
        t = t + float(dic['total_amount_of_payment_usdollars'])
    return t


def perso_doc_info(list_results):
    """ return dictionnary containing personal info on doctor """
    info = {}
    info['specialty'] = list_results[0]['physician_specialty']
    info['street_address'] = list_results[0]['recipient_primary_business_street_address_line1']
    info['zipcode'] = list_results[0]['recipient_zip_code'] 
    info['city'] = list_results[0]['recipient_city']
    info['state'] = list_results[0]['recipient_state']
    info['p_id'] = list_results[0]['physician_profile_id']
    return info

def pay_per_comp(list_results):
    """ Return dictionnary with keys being company names and values 
    being the total payment the company made to that doctor  """
    pay_breakdown = {}
    pharm_name = []
    for dic in list_results:
        dic_key = dic['submitting_applicable_manufacturer_or_applicable_gpo_name']
        if dic_key in pharm_name:
            pay_breakdown[dic_key] = (
                pay_breakdown[dic_key] 
                + float(dic['total_amount_of_payment_usdollars']))
        else:
            pay_breakdown[dic_key] = float(dic['total_amount_of_payment_usdollars']) 
            pharm_name.append(dic['submitting_applicable_manufacturer_or_applicable_gpo_name'])
    return pay_breakdown

def pay_per_comp_filtered(filtered_dic,total_payment):
    """Return"""
    # duplicate dictionnary to be sure to not lost all the data:
    top_pharm = sorted(filtered_dic.items(), key=lambda x:x[1], reverse=True)[:4]
    top_pharm.append(('Other', total_payment - top_pharm[0][1] - top_pharm[1][1] 
    - top_pharm[2][1] - top_pharm[3][1]))
    return top_pharm


def results_per_spe(response):
    """ xxxx"""
    all_payments = {}
    for result in response.json():
        all_payments[str(result['submitting_applicable_manufacturer_or_applicable_gpo_name'])] = float(result["total_amount_of_payment_usdollars"])
    return all_payments

# add payment id , docid, type of food





