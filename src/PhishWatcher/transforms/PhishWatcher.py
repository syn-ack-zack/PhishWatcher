#!/usr/bin/env python

from canari.maltego.utils import debug, progress
from canari.maltego.entities import Domain
from canari.framework import configure #, superuser
'''
Domain Permutation functionality utilized from DNSTwist

Canari port of https://github.com/brianwarehim/goldphish
'''

__author__ = 'Zack Nagaich'
__copyright__ = 'Copyright 2016, Phishwatcher Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Zack Nagaich'
__email__ = 'zacknagaich@gmail.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate' # comment out this line if you don't need this function.
]

def bitsquatting(domain):
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]
    masks = [1, 2, 4, 8, 16, 32, 64, 128]

    for i in range(0, len(dom)):
        c = dom[i]
        for j in range(0, len(masks)):
            b = chr(ord(c) ^ masks[j])
            o = ord(b)
            if (o >= 48 and o <= 57) or (o >= 97 and o <= 122) or o == 45:
                out.append(dom[:i] + b + dom[i+1:] + '.' + tld)

    return out

def homoglyph(domain):
    glyphs = {
    'd':['b', 'cl'], 'm':['n', 'nn', 'rn'], 'l':['1', 'i'], 'o':['0'],
    'w':['vv'], 'n':['m'], 'b':['d'], 'i':['1', 'l'], 'g':['q'], 'q':['g']
    }
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for ws in range(0, len(dom)):
        for i in range(0, (len(dom)-ws)+1):
            win = dom[i:i+ws]

            j = 0
            while j < ws:
                c = win[j]
                if c in glyphs:
                    for g in glyphs[c]:
                        win = win[:j] + g + win[j+1:]

                        if len(g) > 1:
                            j += len(g) - 1
                        out.append(dom[:i] + win + dom[i+ws:] + '.' + tld)

                j += 1

    return list(set(out))

def repetition(domain):
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(0, len(dom)):
        if dom[i].isalpha():
            out.append(dom[:i] + dom[i] + dom[i] + dom[i+1:] + '.' + tld)

    return list(set(out))

def transposition(domain):
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(0, len(dom)-1):
        if dom[i+1] != dom[i]:
            out.append(dom[:i] + dom[i+1] + dom[i] + dom[i+2:] + '.' + tld)

    return out

def replacement(domain):
    keys = {
    '1':'2q', '2':'3wq1', '3':'4ew2', '4':'5re3', '5':'6tr4', '6':'7yt5', '7':'8uy6', '8':'9iu7', '9':'0oi8', '0':'po9',
    'q':'12wa', 'w':'3esaq2', 'e':'4rdsw3', 'r':'5tfde4', 't':'6ygfr5', 'y':'7uhgt6', 'u':'8ijhy7', 'i':'9okju8', 'o':'0plki9', 'p':'lo0',
    'a':'qwsz', 's':'edxzaw', 'd':'rfcxse', 'f':'tgvcdr', 'g':'yhbvft', 'h':'ujnbgy', 'j':'ikmnhu', 'k':'olmji', 'l':'kop',
    'z':'asx', 'x':'zsdc', 'c':'xdfv', 'v':'cfgb', 'b':'vghn', 'n':'bhjm', 'm':'njk'
    }
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(0, len(dom)):
        if dom[i] in keys:
            for c in range(0, len(keys[dom[i]])):
                out.append(dom[:i] + keys[dom[i]][c] + dom[i+1:] + '.' + tld)

    return out

def omission(domain):
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(0, len(dom)):
        out.append(dom[:i] + dom[i+1:] + '.' + tld)

    return list(set(out))

def hyphenation(domain):
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(1, len(dom)):
        if dom[i] not in ['-', '.'] and dom[i-1] not in ['-', '.']:
            out.append(dom[:i] + '-' + dom[i:] + '.' + tld)

    return out

def subdomain(domain):
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(1, len(dom)):
        if dom[i] not in ['-', '.'] and dom[i-1] not in ['-', '.']:
            out.append(dom[:i] + '.' + dom[i:] + '.' + tld)

    return out

def insertion(domain):
    keys = {
    '1':'2q', '2':'3wq1', '3':'4ew2', '4':'5re3', '5':'6tr4', '6':'7yt5', '7':'8uy6', '8':'9iu7', '9':'0oi8', '0':'po9',
    'q':'12wa', 'w':'3esaq2', 'e':'4rdsw3', 'r':'5tfde4', 't':'6ygfr5', 'y':'7uhgt6', 'u':'8ijhy7', 'i':'9okju8', 'o':'0plki9', 'p':'lo0',
    'a':'qwsz', 's':'edxzaw', 'd':'rfcxse', 'f':'tgvcdr', 'g':'yhbvft', 'h':'ujnbgy', 'j':'ikmnhu', 'k':'olmji', 'l':'kop',
    'z':'asx', 'x':'zsdc', 'c':'xdfv', 'v':'cfgb', 'b':'vghn', 'n':'bhjm', 'm':'njk'
    }
    out = []
    dom = domain.rsplit('.', 1)[0]
    tld = domain.rsplit('.', 1)[1]

    for i in range(1, len(dom)-1):
        if dom[i] in keys:
            for c in range(0, len(keys[dom[i]])):
                out.append(dom[:i] + keys[dom[i]][c] + dom[i] + dom[i+1:] + '.' + tld)
                out.append(dom[:i] + dom[i] + keys[dom[i]][c] + dom[i+1:] + '.' + tld)

    return out

def fuzz_domain(domain):
    domains = []

    for i in bitsquatting(domain):
        domains.append(domain)
    for i in homoglyph(domain):
        domains.append(domain) 
    for i in repetition(domain):
        domains.append(domain) 
    for i in transposition(domain):
        domains.append(domain) 
    for i in replacement(domain):
        domains.append(domain) 
    for i in omission(domain):
        domains.append(domain) 
    for i in hyphenation(domain):
        domains.append(domain) 
    for i in insertion(domain):
        domains.append(domain) 
    for i in subdomain(domain):
        domains.append(domain) 

    return  domains


#@superuser
@configure(
    label='To PhishWatcher permutation',
    description='Returns domains that have been permuted using DNSTwist fuzzing logic',
    uuids=[ 'PhishWatcher.v2.PermuteDomain' ],
    inputs=[ ( 'Phishwatcher', Domain ) ],
    remote=False,
    debug=True
)
def dotransform(request, response, config):

    # Send a debugging message to the Maltego UI console
    debug('Fuzing Domains...')
    progress(10)

    # Create MyPhishwatcherEntity entity with value set to 'Hello <request.value>!'
    domains = fuzz_domain(request.value)
   
    progress(50)

    #Create simple domain entity for each generated domain
    for d in domains:
        de = Domain(d)
        response += de


    progress(100)

    # Return response for visualization
    return response


"""
Called if transform interrupted. It's presence is optional; you can remove this function if you don't need to do any
resource clean up.
"""
def onterminate():
    debug('Caught signal... exiting.')
    exit(0)

