import os

class element:


	def __init__(self, name="ELEMENT_NOT_FOUND", return_type="", arguments=[], requires=[]):
		self.function_name = name
		self.arguments = arguments
		self.return_type = return_type
		self.requires = requires


	def get_function_name(self):
		return self.function_name

	def get_arguments_list(self):
		return self.arguments

	def get_return_type(self):
		return self.return_type

	def get_dependency_list(self):
		return self.requires

	