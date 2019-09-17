import sys
import re

def load_file(f):
    lines = ""
    try:
        f = open(sys.argv[1], "r+")
        lines = f.readlines()     
    except FileNotFoundError as fnf:
        print(fnf)
    return(lines)

# def is_valid_line(line):
#     print(line)
#     alphabet = ["=>", "<=>", '?', '=', '!', '(', ')']
#     for word in line:
#         print(word)
#         if word not in alphabet and not word.isalpha() and not word.isupper():
#             return (0)
#     return (1)

def is_proposition(rule, i):
    if (i >= len(rule) or i < 0):
        return (0)
    letter = rule[i]
    if (i + 1 < len(rule) and rule[i + 1].isalpha()):
        return 0
    if (not letter.isalpha() or not letter.isupper()):
        return (0)
    return (1)

def is_op(line, i):
    if (line[i] == '|' or line[i] == '+' or line[i] == '^'):
        return (1)
    elif (line[i] == '='):
        return (1) if ((i + 1) < len(line) and line[i + 1] == '>') else (0)
    elif (line[i] == '<'):
        return (1) if ((i + 2) < len(line) and line[i:i+3] == "<=>") else (0)

def is_binary_op(line, i):
    if (line[i] == '|' or line[i] == '+' or line[i] == '^'):
        return (1)
    return (0)
    
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

def is_valid_lst_of_facts(line):
    line = line.strip().split('=')
    if (len(line) != 2 or line[1] == "" or line[0] != ""):
        return (0)
    facts = line[1]
    if (facts.isalpha() and facts.isupper()):
        return (1)
    return (0)

def is_valid_query(line):
    line = line.strip().split('?')
    if (len(line) != 2 or line[1] == "" or line[0] != ""):
        return (0)
    queries = line[1]
    if (queries.isalpha() and queries.isupper()):
        return (1)
    return (0)

def is_valid_file(lines, rules, facts, query):
    i = 0
    
    while (i < len(lines) and ("<=>" in lines[i] or "=>" in lines[i]) and is_valid_rule(lines[i])):
        rules.append(lines[i].strip())
        i += 1
    while (i < len(lines) and '=' in lines[i] and is_valid_lst_of_facts(lines[i])):
        lines[i] = lines[i].strip().split('=')[1]
        facts.append(lines[i])
        i += 1
        if (len(facts) == 1):
            break
    while (i < len(lines) and '?' in lines[i] and is_valid_query(lines[i])):
        lines[i] = lines[i].strip().split('?')[1]        
        query.append(lines[i])
        i += 1
        if (len(query) == 1):
            break
    if (lines[-1] == lines[i - 1] and rules and facts and query):
        print("I got new rules I count them")
        return (1)
    else:
        print("Missing bracket")
        print("Your file should list: rules, then facts and queries -in one line each- in that order !")
    # if (lines[-1] != lines or not len(rules) or not len(facts) or not len(query)):
    return (0)

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

if (__name__ == "__main__"):
    # expert_system()
    rule = "(A <=> C + D)"
    # rule = "(A+C=>B+C)=>D"
    # print(rule[6:8] == "=>")
    print(is_valid_rule(rule))
    # # print(len("a"))
    # facts = "?ABC"
    # print(is_valid_query(facts))
    # print(is_lst_of_facts(facts))