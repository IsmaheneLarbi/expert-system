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

# def dict_add_elt(props, letter):
#     props[letter] = enum(True, False, Undetermined)


def is_valid_side(side):
    # side = " ".join(side.split())
    print(side)

def is_proposition(rule, i):
    if (i >= len(rule) or i < 0):
        return (0)
    letter = rule[i]
    if (i + 1 < len(rule) and rule[i + 1].isalpha()):
        return 0
    if (not letter.isalpha() or not letter.isupper()):
        return (0)
    return (1)

def is_binary_op(line, i):
    if (line[i] == '|' or line[i] == '+' or line[i] == '^'):
        return (1)
    elif (line[i] == '='):
        return (1) if ((i + 1) < len(line) and line[i + 1] == '>') else (0)
    elif (line[i] == '<'):
        return (1) if ((i + 2) < len(line) and line[i:i+3] == "<=>") else (0)
        
def is_valid_rule(line):
    i = 0
    brackets = 0

    words = line.strip().split()
    line = "".join(words)
    implication = line.count("<=>") + line.count("=>")
    if (not (implication) or implication > 2):
        print("shit how do you exect me to deduce anything, genius ?")
        exit(1)
    while (i < len(line)):
        if (line[i] == '('):
            brackets += 1
        elif (line[i] == '!'):
            if (not is_proposition(line, i + 1)):
                print("Syntax error near '", line[i], "'at column ", i + 1, " : expected proposition")
                exit(1)
        elif (is_proposition(line, i) and (i + 1) < len(line) and not is_binary_op(line, i + 1) and line[i + 1 ] != ')'):
            print("Syntax error near '", line[i], "'at column ", i + 1, " : expected operator")
            exit(1)
        elif (line[i] == ')'):
            if (brackets and (i - 1) >= 0 and (line[i - 1] != '(')):
                brackets -= 1
            else:
                print("Syntax error near '", line[i], "' at column ", i, "expected proposition")
                exit(1)
        elif (line[i] == '<' and is_binary_op(line, i)):
            if (brackets):
                print("Syntax error near '", line[i], "' expected ')'")
                exit(1)
            i += 1
        elif (line[i] == '>' or is_binary_op(line, i)):
            if ((i + 1) >= len(line)) or (line[i + 1] != '!' and not is_proposition(line, i + 1) and line[i + 1] != '('):
                print("Syntax error near '", line[i], "' at column ", i, "expected proposition")                
                exit(1)
        i += 1
    if (brackets != 0):
        print("tu fais de la merde /_|_/")
        exit(1)
    else:
        print("this rule is valid")

def ignore_comments(lines):
    new_lines = []
    for i, line in enumerate(lines):
        if (lines[i][0] != "#" and lines[i].strip()):
            if (line.find("#") != -1):
                line = line[:line.find("#")]
            new_lines.append(line)
    return new_lines

def parse(lines):
    new_lines = ignore_comments(lines)
    return (new_lines)

def expert_system():
    if (len(sys.argv) != 2):
        return (1)
    lines = load_file(sys.argv[1])
    if (lines):
        new_lines = parse(lines)
        for i, line in enumerate(new_lines):
            print("[", i, "]",  line)

if (__name__ == "__main__"):
    # expert_system()
    rule = "((A)|!B)<=>(!C|G)"
    # print(rule[6:8] == "=>")
    is_valid_rule(rule)
    # print(len("a"))