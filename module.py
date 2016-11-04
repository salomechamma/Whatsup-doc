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
    # for later, add first and last name and id to info dictionnary to only pass that to summary.html
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
    # create a dictionnary with key as record id : pharn_name, payment, docid,  food_type:
    all_payments = {}
    for result in response.json():
        all_payments[int(result['record_id'])] = [str(result['submitting_applicable_manufacturer_or_applicable_gpo_name']), float(
            result["total_amount_of_payment_usdollars"]), int(result['physician_profile_id']), str(
            result['nature_of_payment_or_transfer_of_value'])]
    # calculate number of doctor on this query by creating a set and looking at its length
    return all_payments

def averg_per_state(all_payments):
    """ XXXXXXXX"""
    doc_nber = set()
    total = 0
    for record in all_payments.items():
        doc_nber.add(record[1][2])
        total += record[1][1]
    nber = len(doc_nber)
    return int(total/nber)
     

def averg_per_company(all_payments):
    """ XXXXXXXX"""
    # ALL PAYMENTS = [{ RECORD ID: PHARMA, PAYMENT, DOCID, TYPE, RECORDID..}
    # (RECORDID, PHARMA, PAYMENT, DOCID, TYPE, RECORDID
    # PHARMA: +PAYMENT , SET(DOCID)
    pharm_paymt = {}
    nb_doc = {}
    avg_pharm = {}
    for record in all_payments.items():
        company = record[1][0]
        pharm_paymt[company] = record[1][1] + pharm_paymt.get(record[1][0],0)
        nb_doc[company] = nb_doc.get(company,set())
        nb_doc[company].add(record[1][2])
       
    for company in pharm_paymt:
        avg_pharm[company] = int(pharm_paymt[company]/len(nb_doc[company]))
    return avg_pharm


def averg_ind_comp_doc(avg_pharm,doc_pay_breakdown):
    """ XXXXXXXX"""

    averg_comp_match_doc = {}
    for company in doc_pay_breakdown:
        if company[0] in avg_pharm.keys():
            if company[0] == 'Other':
                pass
            else:
                averg_comp_match_doc[company[0]] = avg_pharm[(company[0])]
    # import pdb; pdb.set_trace()
    return averg_comp_match_doc






