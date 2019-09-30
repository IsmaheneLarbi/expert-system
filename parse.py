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

def is_valid_file(lines, rules, facts, query):
    '''This function checks wether the facts and queries given belong to our known propositions
    RETURN VALUES: 1 if they do, if not 0'''
    alphabet = []

    if not parse_file(lines, rules, facts, query):
        return (0)
    for rule in rules:
        alphabet += [prop for prop in rule if prop.isupper() and prop not in alphabet]
    if not (all_facts_in_rules(facts, alphabet) and all_queries_in_rules(query, alphabet)):
        return (0)
    # check if all rules are consistent
    return (1)

def ignore_comments(lines):
    new_lines = []
    for i, line in enumerate(lines):
        if (lines[i][0] != "#" and lines[i].strip()):
            if (line.find("#") != -1):
                line = line[:line.find("#")]
            new_lines.append(line)
    return new_lines

def parse(lines, rules, facts, query):
    new_lines = ignore_comments(lines)
    is_valid_file(new_lines, rules, facts, query)
    return (new_lines)

def expert_system():
    '''This function parses the input file, extracts facts and answers the queries'''
    rules = []
    facts = []
    query = []

    if (len(sys.argv) != 2):
        return (1)
    lines = load_file(sys.argv[1])
    if (lines):
        new_lines = parse(lines, rules, facts, query)
        for i, line in enumerate(new_lines):
            print("[", i, "]",  line)
        print("===rules====")
        print(rules)
        print("====facts=====")
        print(facts)
        print("=====query===")
        print(query)

if (__name__ == "__main__"):
    expert_system()