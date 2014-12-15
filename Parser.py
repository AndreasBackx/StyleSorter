class Parser:
	def __init__(self, lines):
		self.lines = lines

	def addResult(self, result, lineLengths, lastLine, end, key, value=None, originalValue=None):
		'''
		Format the result with the line and content.
		'''
		valueLength = 0 if value is None else len(value)
		originalValueLength = 0 if originalValue is None else len(originalValue)

		start = end - len(key) - valueLength - originalValueLength + 1

		lastIndex = len(lineLengths) - 1
		lineNumber = lastLine

		# Get the original lineNumber (index starting from 0)
		while lastIndex > lineNumber and lineLengths[lineNumber] <= start:
			lineNumber += 1

		result[key] = [lineNumber, value]
		return (result, lineNumber,)

	def parse(self, style=None):
		'''
		Convert an SCSS string to a dict.
		'''
		if style is None:
			style = self.lines

		result = {}
		part = ''
		previousPart = ''

		# Keep track whether the current string in the loop is considered a value or a key in the dict
		isKey = True
		# Whether to reset the current part/string
		reset = False
		# A depth is set when opening braces occurred, it will then get the string between those braces and parse recursively parse those
		depth = 0
		# The line the previous part was originally
		lastLine = 0

		# A single line comment is being parsed
		lineComment = False
		# A multi line comment line is being parsed
		multilineComment = False
		# This indicates the end of a multi line comment
		endlineComment = False

		lineLengths = []
		lines = style.split('\n')

		for key, line in enumerate(lines):
			lineLengths.append(len(line) + 1 if key == 0 else len(line) + lineLengths[key - 1] + 1)

		lineLengths[len(lineLengths) - 1] -= 1
		length = lineLengths[len(lineLengths) - 1]

		for index, char in enumerate(style):
			if depth == 0:
				# Some kind of comment is being parsed
				if lineComment or multilineComment or endlineComment:
					# It's the end of a single line comment
					if lineComment and char == '\n':
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
						lineComment = False
						reset = True
					elif endlineComment:
						endlineComment = False
						part += char
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
						reset = True
					# A multi line comment is being parsed and the current char might indicate it'll end
					elif multilineComment and char == '*' and style[index + 1] == '/':
						endlineComment = True
						multilineComment = False
				elif char == '/':
					if length > index + 1:
						nextChar = style[index + 1]
						# If the next char is '/' it means a single line comment is starting (//)
						if nextChar == '/':
							lineComment = True
						# If the next char is '*' it means a multi line comment is starting (/*)
						elif nextChar == '*':
							multilineComment = True
				# If an attribute is being set (e.g: "height:") it must be considered as so
				# if in SCSS &:hover is being used, it must be considered as one key
				elif char == ':' and index > 0 and style[index-1] != '&':
					if isKey:
						isKey = False
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
					reset = True
				elif char == ';':
					# @imports, @extends, etc. are keys while attribute values are dict values
					if isKey:
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part)
					else:
						(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, previousPart, part)
						isKey = True
					reset = True
				elif char == '{':
					depth += 1
					part = part.strip()
					(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, part, {})
					reset = True
			# It's already adding the string for a recursive result, but we need to keep track where the current nesting ends
			elif char == '{':
				depth += 1
			elif char == '}':
				depth -= 1
				# If the depth reaches 0 again, then it means that this closing brace ends this nesting and we want to parse the string between the braces
				if depth == 0:
					nestedStyle = self.parse(part)
					(result, lastLine,) = self.addResult(result, lineLengths, lastLine, index, previousPart, nestedStyle, part)
					reset = True

			if reset:
				reset = False
				previousPart = part
				part = ''
			# Strip whitespace if it should not be preserved (comments and nestings need to be preserved)
			elif (multilineComment or (depth > 0 and style[index - 1] != '{') or char != '\n')\
				and (part != '' or char != ' ')\
				and (part != '' or char != '\t'):
				part += char

		return result
