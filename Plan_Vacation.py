# -*- coding: utf-8 -*-
"""
Author: COlin Cambo
cwb35@wildcats.unh.edu

This program returns the best vacationing towns and businesses for any state
given to it. More customization options are available like selecting specific
categories, so you could look for the best pizza places in NY for example

This is project I built for practice with web scraping and using API's
"""

import sys
import argparse
import requests
from bs4 import BeautifulSoup
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import pandas as pd
import os
import errno
import re
import json
import io

creds = json.load(io.open(r'C:\Users\Colin\Documents\Python Scripts\Vacation_Planner\config_secret.json'))
auth = Oauth1Authenticator(**creds)
client = Client(auth)

def export_to_csv(town_dict, output):
    """
    Exports the data stored in town_dict to csv output
    """
    for i, (key, value) in enumerate(town_dict.items(), start=1):
        btype, bname, brating, bcity, baddress, bphone = ([] for i in range(6))
        for k, v in value.items():
            for business in v:
                btype.append(k)
                bname.append(business.name)
                brating.append(business.rating)
                bcity.append(business.location.city)
                if len(business.location.address) != 0:
                    baddress.append(business.location.address[0])
                else:
                    baddress.append('None')
                bphone.append(str(business.display_phone))
        town_df = pd.DataFrame({'Type':btype, 'Name':bname, 'Rating':brating,
                           'City':bcity, 'Address':baddress, 'Phone':bphone},
                           columns=['Type', 'Name', 'Rating', 'City', 
                           'Address', 'Phone'])
        town_df.to_csv(output+'Top_Places_'+str(key)+'.csv',index=False)
        
def print_businesses(town_dict):
    """
    Prints out the data about businesses stored in town_dict
    """
    for i, (key, value) in enumerate(town_dict.items(), start=1):
        print('#{} Destination: {}'.format(i, key))
        for k, v in value.items():
            print('  Top {} {} businesses!'.format(len(v), k))
            for business in v:
                print('\tName: {}'.format(business.name))
                print('\t\tRating:  {}'.format(business.rating))
                print('\t\tCity:    {}'.format(business.location.city))
                if len(business.location.address) != 0:
                    print('\t\tAddress: {}'.format(business.location.address[0]))
                else:
                    print('\t\tAddress: None')
                print('\t\tPhone:   {}'.format(str(business.display_phone)))
            
def get_link(state):
    """
    Scrapes TripAdvisor's tourism map for the tourism URL for "state"  
    """
    response = requests.get('https://www.tripadvisor.com/MapPopup?geo=191')
    soup = BeautifulSoup(response.text,"lxml")
    
    link_reg = re.compile(r"'(.+)'")
    
    return link_reg.findall(str(soup.find('area',{'alt':state})))[0]

def get_popular_towns(state_link):
    """
    Scrapes TripAdvisor's tourism page at the link specified for top towns
    """
    link = 'https://www.tripadvisor.com/'
    
    response = requests.get(link+state_link)
    soup = BeautifulSoup(response.text,"lxml")
    
    towns = []
    
    popular_towns = soup.find_all('span',{'class':'name'})
    for row in popular_towns:
        towns.append(row.text)
    if len(popular_towns) == 0:
        for i, tag in enumerate(soup.find_all('div',{'class':'neighborhoodName'})):
            if i<3:
                towns.append(tag.text)
    if len(towns) == 0:
        towns.append(soup.find('h1',{'id':'HEADING'}).text)
    return towns
    
def find_popular_town_businesses(state, output, num, terms):        
    """
    Extracts information about local businesses for every town specified on
    TripAdvisor's tourism site
    """
    state_link = get_link(state)
    my_towns = get_popular_towns(state_link)
    town_dict = {town:{term:[] for term in terms} for town in my_towns}
    
    for i, town in enumerate(my_towns, start=1):
        
        search_str=town+' '+state
        
        for term in terms:
            params = {
                'term': term,
                'lang': 'en',
                'limit':num,
                'sort':2
            }
            r = client.search(search_str, **params)
            for business in r.businesses:
                town_dict[town][term].append(business)
                
    print_businesses(town_dict)      
    if output != False:
        try:
            newd = os.getcwd()+'\\Vacation-'+str('_'.join(state.split(' ')))+'\\'
            os.makedirs(newd)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        export_to_csv(town_dict, newd)
        
def main():
    """
    Parses arguments given to command line
    """
    parser = argparse.ArgumentParser()
    
    parser.add_argument('program', metavar='PROG', type=str)
    parser.add_argument('state', metavar='state', type=str)
    parser.add_argument('num_business', metavar='N', type=int)
    parser.add_argument('-terms', metavar='terms', type=str, nargs='+')
    parser.add_argument('-categories', metavar='C', type=str, nargs='+')
    parser.add_argument('-output', metavar='out', type=str)
    
    arg_dict = vars(parser.parse_args(sys.argv))
    
    if arg_dict['output']!=None:
        output = arg_dict['output']
    else:
        output = False
        
    if arg_dict['terms']!=None:
        terms = arg_dict['terms']
    else:
        terms = ['food', 'hotel', 'active']
        
    params = {
        'state':arg_dict['state'],
        'num':arg_dict['num_business'],
        'output':output,
        'terms':terms
    }
    
    find_popular_town_businesses(**params)
    
if __name__ == '__main__':
    main()
