from parse import *

def choose_rule(query, rules_base):
    for concl, cond in rules_base:
        if query in concl:
            concl = cond 

def deduce(alphabet, facts, queries, rules_base):
    for query in queries:
        if query not in facts:
            rule = choose_rule(query, rules_base)