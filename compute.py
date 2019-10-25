import re

def tokenize(rule):
    rule = rule.replace(' ', '')
    rule = re.split(r"(<=>|=>|\(|\)|\||\+|\^)", rule)
    rule = [r for r in rule if r !='']
    return (rule)

# def get_highest_op_index(rule, operators):
#     op = 0
#     i = 0

#     for index, val in enumerate(rule):
#         if val in operators and operators[val] > op:
#             op = operators[val]
#             i = index
#     return (i)

def brackets(rule):
    # rule = "A|(B+C)+D"
    props = []
    res = re.search(r"\((\w|!|\+|\^|\|)*\)", rule)
    if (res):
        line = res.group()
        props.append(res[0], )

def compute(rule, operators):
    # index = 0
    stack = []
    ops = []
    rule = "A+B"

    rule = tokenize(rule)
    print(rule)
    stack = [prop for prop in rule if prop.isupper()]
    print(stack)
    ops = [op for op in rule if op in operators.keys()]
    print(ops)
    # brackets(rule)
    # index = get_highest_op_index(rule, operators)
    # print(rule[index])

if (__name__ == "__main__"):
    operators = {'<=>':0 , '=>':1, '^':2, '|':3, '+':4, '!': 5, ')':6, '(': 7}
    rule = "A | ( B +    C ) => D"
    compute(rule, operators)