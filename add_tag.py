#!/usr/bin/env python

'''
updates product grq metadata with the machine tag
'''
from __future__ import print_function
import json
import requests
from hysds.celery import app

def load_context():
    '''loads the context file into a dict'''
    try:
        context_file = '_context.json'
        with open(context_file, 'r') as fin:
            context = json.load(fin)
        return context
    except:
        raise Exception('unable to parse _context.json from work directory')

def add_tag(index, uid, prod_type, tag):
    '''updates the product with the given tag'''
    grq_ip = app.conf['GRQ_ES_URL'].replace(':9200', '').replace('http://', 'https://')
    grq_url = '{0}/es/{1}/{2}/{3}/_update'.format(grq_ip, index, prod_type, uid)
    es_query = {"doc" : {"metadata": {"user_tags" : [tag]}}}
    print('querying {} with {}'.format(grq_url, es_query))
    response = requests.post(grq_url, data=json.dumps(es_query), timeout=60, verify=False)
    response.raise_for_status()
    print('successfully updated {} with tag {}'.format(uid, tag))

def main():
    '''loads params from context and updates the machine tag on grq'''
    ctx = load_context()
    index = ctx['prod_index']
    uid = ctx['prod_id']
    prod_type = ctx['prod_type']
    tag = ctx['add_tag']
    add_tag(index, uid, prod_type, tag)

if __name__ == '__main__':
    main()
