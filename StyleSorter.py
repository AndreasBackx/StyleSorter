import sublime
import sublime_plugin
from StyleSorter.Parser import Parser


class StyleSorterSortCommand(sublime_plugin.TextCommand):

	NAME = 'StyleSorter'

	SETTINGS_POPUP = 'extension_popup'
	SETTINGS_RESET = 'extension_reset'

	def run(self, edit):
		self.settings = sublime.load_settings(self.NAME + '.sublime-settings')
		ordering = self.settings.get('ordering')

		syntaxOrExt, syntax = self.getSyntax()
		if syntax not in self.settings.get('extensions'):
			self.notify('The file\'s %s \'%s\' is disabled for sorting.' % (syntaxOrExt, syntax))
			return

		self.view.set_status(self.NAME, 'Parsing stylesheet')
		self.region = sublime.Region(0, self.view.size())
		text = self.view.substr(self.region)
		thread = Parser(text, ordering, self.updateFile)
		thread.start()

	def getSyntax(self):
		syntax = self.view.settings().get('syntax').split('.')[-2].split('/')[-1]
		if syntax != 'Plain text' or self.view.file_name() is None:
			return ('syntax', syntax)
		return ('extension', self.view.file_name().split('.')[-1])

	def notify(self, text):
		popup = self.settings.get(self.SETTINGS_POPUP, False)
		reset = self.settings.get(self.SETTINGS_RESET, False)
		if popup or reset:
			if not popup:
				self.settings.set(self.SETTINGS_RESET, False)
				text += ' This popup is automatically disabled from now on and is displayed in the status bar.'
				text += ' You can enable it again in the settings.'
			sublime.message_dialog(text)
		else:
			sublime.status_message(text)

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
