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

def all_queries_in_rules(queries, alphabet):
    return False if [query for query in queries if query not in alphabet] else True

def all_facts_in_rules(facts, alphabet):
    return False if [fact for fact in facts if fact not in alphabet] else True