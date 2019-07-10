#!/usr/bin/python
import re

def stripAndLower(string):
	return string.lower().translate(None, ".?,!:")


def kwicOrderBy(kwicEntry):
	(lst, n) = kwicEntry
	return tuple([element.lower() for element in lst])


def getPairs(lines):
	pairs = []
	wordMatches = dict()
	for line in lines:
		line = line.split()
		for word in set(line):
			word = stripAndLower(word)
			if word:
				if word not in wordMatches:
					wordMatches[word] = []

				for match in set(line):
					match = stripAndLower(match)
					if match and match != word:
						wordMatches[word].append(match)
				
	for key in wordMatches:
		for match in wordMatches[key]:
			count = wordMatches[key].count(match)
			if count > 1:
				pairs.append((tuple(sorted([key, match])), count))

	return sorted(set(pairs))

			
def kwic(text, ignoreWords=[], listPairs=False, periodsToBreaks=False):
	result = list()
				             
	if periodsToBreaks:
		text = re.sub("\n", " ", text)
		text = re.sub("([a-z]\.) ", "\g<1>\n", text)

	lines = text.split("\n")
	
	for i in range(0, len(ignoreWords)):
		ignoreWords[i] = stripAndLower(ignoreWords[i])
				             
	for i in range(0, len(lines)):
		line = lines[i].split()
		
		for word in line:
			if stripAndLower(line[0]) not in ignoreWords:
				result.append((list(line), i))
			line.append(line.pop(0))

	if not listPairs:
		return sorted(result, key=kwicOrderBy)
	else:
		return (sorted(result, key=kwicOrderBy), getPairs(lines))
