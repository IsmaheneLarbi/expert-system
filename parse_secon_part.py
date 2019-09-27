import re

rules = ["C => E",
		"A + (B + C) => D",
		"A | B => C",
		"A + B => Y + Z"
		]

facts = ["=ABG"]

queries =["?GVX"]

def node_for_rules(rules):
	rulesNode = []
	for rule in rules:
		rulesNode = list(filter(None, re.split(r"\s|\+|\^|\||!|=|<|>|<=>|=>|\(|\)", rule)))
		print(rulesNode)
	return (rulesNode)

def verif_facts_in_rules(facts, rulesNode):
	factsNode = list(filter(None, re.split(r"\s|=", facts[0])))
	if factsNode:
		factsNode = list(factsNode[0])
	else:
		return False
	for fact in factsNode:
		if fact not in rulesNode:
			return False
	return True

def verif_queries_in_rules(queries, rulesNode):
	queriesNode = list(filter(None, re.split(r"\s|\?", queries[0])))
	if queriesNode:
		queriesNode = list(queriesNode[0])
	else:
		return False
	for querie in queriesNode:
		if querie not in rulesNode:
			return False
	return True


rulesNode = node_for_rules(rules)
if not verif_facts_in_rules(facts, rulesNode):
	print("A fact variable was not defined")
if not verif_queries_in_rules(queries, rulesNode):
	print("A query variable was not defined")
print("END")