from is_valid_rule import is_binary_op
from is_valid_rule import is_op
from is_valid_rule import is_proposition

class Rule:
    def __init__(self, rule):
        self.rule = rule
    
    def is_valid_rule(self):
        i = 0
        brackets = 0

        words = self.rule.strip().split()
        self.rule = "".join(words)
        implication = self.rule.count("<=>") + self.rule.count("=>")
        if (not (implication) or implication > 2):
            print("shit how do you exect me to deduce anything, genius ?")
            return (0)
        while (i < len(self.rule)):
            if (self.rule[i] == '('):
                brackets += 1
            elif (self.rule[i] == '!'):
                if (not is_proposition(self.rule, i + 1)):
                    print("Syntax error in self.rule [", self.rule, "] near '", self.rule[i], "'at character ", i + 1, " : expected proposition")
                    return (0)
            elif (is_proposition(self.rule, i) and (i + 1) < len(self.rule) and not is_op(self.rule, i + 1) and self.rule[i + 1 ] != ')'):
                print("Syntax error in self.rule [", self.rule, "] near '", self.rule[i], "'at character ", i + 1, " : expected operator")
                return (0)
            elif (self.rule[i] == ')'):
                if (brackets and (i - 1) >= 0 and (self.rule[i - 1] != '(')):
                    brackets -= 1
                else:
                    print("Syntax error in self.rule [", self.rule, "] near '", self.rule[i], "' at character ", i + 1, "expected proposition")
                    return (0)
            elif (self.rule[i] == '<' and is_op(self.rule, i)):
                if (brackets):
                    print("Syntax error in self.rule [", self.rule, "] near '", self.rule[i], "' expected ')'")
                    return (0)
                i += 1
            elif (self.rule[i] == '>' or is_binary_op(self.rule, i)):
                if (((i + 1) >= len(self.rule)) or ((self.rule[i + 1] != '!') and (self.rule[i + 1] != '(') and not is_proposition(self.rule, i + 1))):
                    print("Syntax error in self.rule [", self.rule, "] near '", self.rule[i], "' at character ", i + 1, "expected proposition")                
                    return (0)
            i += 1
        if (brackets != 0):
            print("tu fais de la merde /_|_/")
            return (0)
        else:
            return (1)