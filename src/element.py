import os

class element:


	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.dependencies = []


	def add_dependency(self, to_add):
		self.dependencies.append(to_add)


	def get_dependency_list(self):
		return self.dependencies

	def getName(self):
		return self.name
		
