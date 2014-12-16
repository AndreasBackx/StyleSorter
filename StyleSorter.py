import sublime
import sublime_plugin
from StyleSorter.Parser import Parser


class StyleSorterSortCommand(sublime_plugin.TextCommand):

	NAME = 'StyleSorter'

	def run(self, edit):
		settings = sublime.load_settings(self.NAME + '.sublime-settings')
		ordering = settings.get('ordering')

		self.view.set_status(self.NAME, 'Parsing stylesheet')
		self.region = sublime.Region(0, self.view.size())
		text = self.view.substr(self.region)
		thread = Parser(text, ordering, self.updateFile)
		thread.start()

	def updateFile(self, formatted):
		self.view.set_status(self.NAME, 'Updating stylesheet')
		sel = self.view.sel()
		sel.clear()
		sel.add(self.region)
		self.save(formatted)

		self.view.erase_status(self.NAME)
		sublime.status_message(self.NAME + ' successfully sorted your stylesheet.')

	def save(self, text):
		auto_indent = self.view.settings().get('auto_indent')
		if auto_indent:
			self.view.settings().set('auto_indent', False)
		self.view.run_command('insert', {'characters': text})
		if auto_indent:
			self.view.settings().set('auto_indent', True)
