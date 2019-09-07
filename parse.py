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


# def is_valid_side(side):
#     side = " ".join(side.split())
#     print(side)

def is_proposition(letter):
    return 1 if (letter.isalpha() and letter.isupper()) else 0

def is_valid_rule(line):
    brackets = 0
    i = 0

    line = line.strip()
    line = "".join(line.split())
    print(line)
    while (i < len(line)):
        if (line[i] == '('):
            brackets += 1
        else if (line[i] == ')'):
            if ((i - 1) >= 0 and (line[i - 1].isalpha())):
                brackets -= 1
            else:
                print("Syntax error near ", line[i], "at column ", i)
                exit(1)
        else if (line[i] == '!'):
            if (i + 1 >= len(line) or (i + 1 < len(line) and not is_proposition(line[i + 1]))
                print("Syntax error near ", line[i], "at column ", i, ": expected proposition")

        i += 1
    print(line)
    if (brackets != 0):
        print("tu fais de la merde /_|_/")
        # print("Syntax error near ", line[i], "at column ", i)

def ignore_comments(lines):
    new_lines = []
    for i, line in enumerate(lines):
        if (lines[i][0] != "#" and lines[i].strip()):
            new_lines.append(line[0:line.find("#")])
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
    is_valid_rule("(A+B)B)")