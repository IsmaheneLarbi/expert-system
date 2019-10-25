#!/usr/local/bin/python3

import sys
import re
from check_syntax import *

def load_file(f):
    lines = ""
    try:
        f = open(sys.argv[1], "r+")
        lines = f.readlines()     
    except FileNotFoundError as fnf:
        print(fnf)
    return(lines)
    
def is_valid_rule(line):
    i = 0
    brackets = 0

    words = line.strip().split()
    line = "".join(words)
    implication = line.count("<=>") if line.count("<=>") else line.count("=>")
    if (implication != 1):
        print("Error: invalid rule ", line, "You must use one and only one implication !")
        return (0)
    while (i < len(line)):
        if (line[i] == '('):
            brackets += 1
        elif (line[i] == '!'):
            if (not is_proposition(line, i + 1)):
                print("Syntax error in line [", line, "] near '", line[i], "'at character ", i + 1, " : expected proposition")
                return (0)
        elif (is_proposition(line, i) and (i + 1) < len(line) and not is_op(line, i + 1) and line[i + 1 ] != ')'):
            print("Syntax error in line [", line, "] near '", line[i], "'at character ", i + 1, " : expected operator")
            return (0)
        elif (line[i] == ')'):
            if (brackets and (i - 1) >= 0 and (line[i - 1] != '(')):
                brackets -= 1
            else:
                print("Syntax error in line [", line, "] near '", line[i], "' at character ", i + 1, "expected proposition")
                return (0)
        elif (line[i] == '<' and is_op(line, i)): # or line[i] == '=' ???
            if (brackets):
                print("Syntax error in line [", line, "] near '", line[i], "' expected ')'")
                return (0)
            i += 1
        elif (line[i] == '>' or is_binary_op(line, i)):
            if (((i + 1) >= len(line)) or ((line[i + 1] != '!') and (line[i + 1] != '(') and not is_proposition(line, i + 1))):
                print("Syntax error in line [", line, "] near '", line[i], "' at character ", i + 1, "expected proposition")                
                return (0)
        i += 1
    if (brackets != 0):
        print("tu fais de la merde /_|_/")
        return (0)
    else:
        return (1)

def parse_file(lines, rules, facts, query):
    '''This function checks if the syntax is correct, 
    RETURN VALUES : 1 if it is, 0 if not'''
    i = 0

    while (i < len(lines) and ("<=>" in lines[i] or "=>" in lines[i]) and is_valid_rule(lines[i])):
        rules.append(lines[i].strip())
        i += 1
    if (i < len(lines) and '=' in lines[i]):
        facts += list(filter(None, re.split(r"\s|\=|", lines[i])))
        i += 1
    if (i < len(lines) and '?' in lines[i]):
        query += list(filter(None, re.split(r"\s|\?|", lines[i])))
        i += 1
    if (lines[-1] == lines[i - 1] and rules and facts and query):
        return (1)
    else:
        print("Your file should list: rules, then facts and queries -in one line each- in that order !")
    return (0)

def is_valid_file(lines, rules, alphabet, facts, query):
    '''This function checks wether the facts and queries given belong to our known propositions
    RETURN VALUES: 1 if they do, if not 0'''
    props = []

    if not parse_file(lines, rules, facts, query):
        return (0)
    for rule in rules:
        props += [prop for prop in rule if prop.isupper() and prop not in props]
        alphabet.update(dict(zip(props, len(props) * [0])))
    if not (all_facts_in_rules(facts, alphabet) and all_queries_in_rules(query, alphabet)):
        return (0)
    alphabet.update({key:1 for key in facts})
    rules = [rule.replace(' ', '') for rule in rules]
    # check if all rules are consistent
    forward_chaining(facts, rules, alphabet)
    return (1)

def ignore_comments(lines):
    new_lines = []
    for i, line in enumerate(lines):
        if (lines[i].strip()):
            line = line.strip()
            if (line.find("#") != -1):
                line = line[:line.find("#")]
            if (line):
                new_lines.append(line)
    return new_lines

def remove_dbl_impl(rules):
    new_rules = {}

    for rule in rules:
        rule = "".join(re.split(r"\s", rule))
        if "<=>" in rule:
            split = rule.rpartition("<=>")
            new_rules[split[0]] = split[2]
        else:
            split = rule.rpartition("=>")
        new_rules[split[2]] = split[0]
    return new_rules

def solve(conclusion, alphabet, data):
    rules = []

    conclusion = conclusion.split('+')
    print("conclusion = ", conclusion)
    for prop in conclusion:
        if '!' in prop:
            prop = prop[1]
            if prop in data.keys() and data[prop] == 1:
                print("Invalid file :", prop, "Cannot be True and False at the same time")
                exit(1)
            else:
                data[prop] = 0
        else:
            data[prop] = 1
    print("data gathered :", data)


def forward_chaining(facts, rules_set, alphabet):
    '''this function checks wether there are inconsistencies in the rules'''
    rules = []
    data = {fact:1 for fact in facts}
    rules = [rule.replace(' ', '').replace('\t', '') for rule in rules_set]
    
    print("rules in fc", rules)
    for rule in rules:
        split = re.split(r"=>", rule)
        condition = split[0]
        conclusion = split[1]
        if (rec(condition, alphabet)):
            print(rule)
            solve(conclusion, alphabet, data)

def backward_chaining(queries, rules_base, alphabet, facts):
    rules = {}

    for query in queries:
        if query not in alphabet:
            print("Query ", query, "not in list of propositions, please add a rule containing your query")
            exit(1)
        rules.update({k:v for (k,v) in rules_base.items() if query in k})
        print("rules containing", query, rules)
        for rule in rules:
            if rec(rules[query], alphabet):
                facts.append(query)
                alphabet[query] = 1
        # for concl, cond in rules_base.items():
        #     if query in concl:
        #         print("yay ! found", query, "in", concl, ":", cond)
        #         rules[concl] = cond
        #         if (rec(cond, alphabet) and concl not in facts):
        #             facts.append(concl)
        print("rules used", rules)
        if query in facts:
            print(query, "is True")
        else:
            print(query, "is False")

def parse(lines, rules, alphabet, facts, query, rules_base):
    new_lines = ignore_comments(lines)
    if (is_valid_file(new_lines, rules, alphabet, facts, query)):
        rules_base.update(remove_dbl_impl(rules))
    return (new_lines)

def expert_system():
    '''This function parses the input file, extracts facts and answers the queries'''
    rules = []
    rules_base = {}
    alphabet = {}   
    facts = []
    query = []

    if (len(sys.argv) != 2):
        return (1)
    lines = load_file(sys.argv[1])
    if (lines):
        new_lines = parse(lines, rules, alphabet, facts, query, rules_base)
        for i, line in enumerate(new_lines):
            print("[", i, "]",  line)
        print("===rules====")
        print(rules)
        print("=====RULES BASE =====")
        print(rules_base)
        print("=====alphabet=====")
        print(alphabet)
        print("====facts=====")
        print(facts)
        print("=====query===")
        print(query)
        # stack_rules(rules)
        # forward_chaining(facts, rules, alphabet)
        # backward_chaining(query, rules_base, alphabet, facts)
        # backward_chaining(['V'], rules_base, alphabet, facts)
        print("====facts=====")
        print(facts)
        # scan_rules(rules, alphabet)

def calc(rules, alphabet):
    rule = "A | (B + C) => D"
    operators = {'^': 0, '|': 1, '+': 2, '!': 3}
    split = re.split(r'=>|<=>', rule)
    split[0] = list(split[0].replace(' ', ''))
    split[1] = list(split[1].replace(' ', ''))

def do(one, op, two):
    one = int(one)
    two = int(two)

    if op == '+':
        return (one & two)
    elif op == '^':
        return (one ^ two)
    elif op == '|':
        return (one | two)
    else:
        return -1

def negate(rule):
    # print("=====NEGATE=====")
    while '!' in rule:
        i = rule.index('!')
        rule[i + 1] = int(rule[i + 1]) ^ 1
        del rule[i]
    return rule

def simplify(rule, op):
    # print("=======", op, "=====")
    while op in rule:
        i = rule.index(op)
        rule[i + 1] = do(rule[i + 1], op, rule[i - 1])
        del rule[i - 1]
        del rule[i - 1]
    return rule

def test(rule, alphabet):
    i = 0
    rule = list(rule)

    for i, r in enumerate(rule):
        if (r.isalpha()):
            rule[i] = alphabet[r]
    negate(rule)
    simplify(rule, '+')
    simplify(rule, '^')
    simplify(rule, '|')
    return rule[0]

def rec(rule, alphabet):
    res = re.search(r"\((\w|!|\+|\^|\|)*\)", rule)
    if (res == None):
        value = test(rule, alphabet)
        return (value)
    else:
        rule = rule.replace(res.group(), str(test(res.group().replace('(', '').replace(')', ''), alphabet)))
        return rec(rule, alphabet)

if (__name__ == "__main__"):
    expert_system()