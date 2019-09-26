def populate(rules, facts, queries):
    rules.extend(["A => B", "B => C", "C <=> D", "D=>E", "E => G | !H"])
    facts.extend(["E", "A"])
    queries.extend(["C", "G", "H"])

def main():
    rules = []
    facts = []
    queries = []
    populate(rules, facts, queries)
    print("=========rules=========")
    print(rules)
    print("=========facts=========")
    print(facts)
    print("=========queries=========")
    print(queries)

if __name__ == "__main__":
    main()