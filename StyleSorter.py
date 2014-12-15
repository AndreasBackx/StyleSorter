import sublime
import sublime_plugin


class SortCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		lines = self.view.substr(sublime.Region(0, self.view.size()))
		parsed = self.scssToDict(lines)

	def scssToDict(self, scss):
		isKey = True
		reset = False
		depth = 0
		part = ''
		previousPart = ''
		result = {}
		for index, char in enumerate(scss):
			if depth == 0:
				if char == ':' and index > 0 and scss[index-1] != '&':
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
