import os

class element:


	def __init__(self, name, text, params, dependencies=[], before=[], after=[]):
		self.name = name
		self.text = text
		self.parameters = params
		self.dependencies = dependencies
		self.before = before
		self.after = after


	def get_parameters():
		return self.parameters

	def get_dependency_list(self):
		return self.dependencies

	def get_before(self):
		return self.before

	def get_after(self):
		return self.after

	def get_name(self):
		return self.name