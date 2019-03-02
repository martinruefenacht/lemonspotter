import os

class MPI_Element:


	def __init__(self, name, text):
		self.name = name
		self.text = text
		self.dependencies = []



	def add_dependency(self, to_add):
		self.dependencies = to_add


	def save():
		
