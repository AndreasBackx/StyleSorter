import sublime
import sublime_plugin
import json


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		parsed = self.scssToDict(lines)
		print(json.dumps(parsed, indent=4))

	def scssToDict(self, scss):
		result = {}
		part = ''
		previousPart = ''

		isKey = True
		reset = False
		depth = 0

		lineComment = False
		multilineComment = False
		endlineComment = False

		length = len(scss)

		for index, char in enumerate(scss):
			if depth == 0:
				if lineComment or multilineComment or endlineComment:
					if lineComment:
						if char == '\n':
							result[part] = char
							lineComment = False
							reset = True
						else:
							pass
					elif multilineComment:
						if length > index + 1:
							nextChar = scss[index + 1]
							if char == '*' and nextChar == '/':
								endlineComment = True
								multilineComment = False
					else:
						endlineComment = False
						part += char
						result[part] = None
						print(part)
						reset = True
				elif char == '/' and length > index + 1:
					nextChar = scss[index + 1]
					if nextChar == '/':
						lineComment = True
					elif nextChar == '*':
						multilineComment = True
					else:
						# We want to remove this invalid /
						continue
				elif char == ':' and index > 0 and scss[index-1] != '&':
					if isKey:
						isKey = False
						result[part] = ''
					reset = True
				elif char == ';':
					if isKey:
						result[part] = None
					else:
						result[previousPart] = part
					reset = True
				elif char == '{':
					depth += 1
					part = part.strip()
					result[part] = {}
					reset = True
			elif char == '{':
				depth += 1
			elif char == '}':
				depth -= 1
				if depth == 0:
					nestedScss = self.scssToDict(part)
					result[previousPart] = nestedScss
					reset = True

			if reset:
				reset = False
				previousPart = part
				part = ''
			elif char != '\n' and (part != '' or char != ' ') and (part != '' or char != '\t'):
				part += char

		return result

	def description(self):
		return 'Super CSS sorter.'
