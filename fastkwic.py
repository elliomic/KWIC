#!/usr/bin/python
import re

debugMode = False

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


def purgeLineBreaks(text):
        return re.sub("\n", " ", text)

def convertPeriodsToBreaks(text):
        return re.sub("([a-z]\.) ", "\g<1>\n", purgeLineBreaks(text))

def cycleLine(line):
        return line.append(line.pop(0))

def kwicIndex(lines, ignoreWords):
        result = list()
        for i in xrange(0, len(lines)):
                line = lines[i].split()
		for word in line:
			if stripAndLower(line[0]) not in ignoreWords:
				result.append((list(line), i))
			line.append(line.pop(0))
        return result

			
def kwic(text, ignoreWords=[], listPairs=False, periodsToBreaks=False, debug=False):
        global debugMode
        debugMode = debug

	if periodsToBreaks:
		text = convertPeriodsToBreaks(text);
				             
	result = sorted(kwicIndex(text.split("\n"), ignoreWords), key=kwicOrderBy)

        return (result, getPairs(lines)) if listPairs else result
