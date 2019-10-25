def get_highest_opeator_index(rule, operators):
    op = 0
    index = 0

    for i, val in enumerate(rule):
        if val in operators and operators[val] > op:
            op = operators[val]
            print(val)
            index = i    
    left = rule[0:index]
    right = rule[index + 1:]
    print("=======LEFT==========")
    print(left)
    print("=======RIGHT==========")
    print
    return (index)

operators = {'^':2, '|':3, '+':4, '!': 5}
rule = "A+B"
rule = list(rule)
print(rule)
print(get_highest_opeator_index(rule, operators))