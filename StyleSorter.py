import sublime
import sublime_plugin
import json


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		parsed = self.scssToDict(lines)
		print(json.dumps(parsed, indent=4))

	def addResult(self, result, lineLengths, lastLine, end, key, value='', originalValue=''):
		start = end - len(key) - len(value) - len(originalValue) + 1
		lastIndex = len(lineLengths) - 1
		lineNumber = lastLine
		while lastIndex > lineNumber and lineLengths[lineNumber] <= start:
			lineNumber += 1
		result[key] = [lineNumber, value]
		return (result, lineNumber,)

	def scssToDict(self, style):
		result = {}
		part = ''
		previousPart = ''

		isKey = True
		reset = False
		depth = 0
		lastLine = 0

		lineComment = False
		multilineComment = False
		endlineComment = False

		lineLengths = []
		lines = style.split('\n')

		for key, line in enumerate(lines):
			lineLengths.append(len(line) + 1 if key == 0 else len(line) + lineLengths[key - 1] + 1)

		lineLengths[len(lineLengths) - 1] -= 1
		length = lineLengths[len(lineLengths) - 1]

		for index, char in enumerate(style):
			if depth == 0:
				if lineComment or multilineComment or endlineComment:
					if lineComment and char == '\n':
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part, char)
						lineComment = False
						reset = True
					elif endlineComment:
						endlineComment = False
						part += char
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
						reset = True
					elif multilineComment and length > index + 1 and char == '*' and style[index + 1] == '/':
						endlineComment = True
						multilineComment = False
				elif char == '/' and length > index + 1:
					nextChar = style[index + 1]
					if nextChar == '/':
						lineComment = True
					elif nextChar == '*':
						multilineComment = True
					else:
						# We want to remove this invalid /
						continue
				elif char == ':' and index > 0 and style[index-1] != '&':
					if isKey:
						isKey = False
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
					reset = True
				elif char == ';':
					if isKey:
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
					else:
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, previousPart, part)
					reset = True
				elif char == '{':
					depth += 1
					part = part.strip()
					(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part, {})
					reset = True
			elif char == '{':
				depth += 1
			elif char == '}':
				depth -= 1
				if depth == 0:
					nestedScss = self.scssToDict(part)
					(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, previousPart, nestedScss, part)
					reset = True

			if reset:
				reset = False
				previousPart = part
				part = ''
			elif (multilineComment or (depth > 0 and style[index - 1] != '{') or char != '\n') and (part != '' or char != ' ') and (part != '' or char != '\t'):
				part += char

		return result

	def description(self):
		return 'Super CSS sorter.'
