from dbo import DBO
from flask import jsonify

build_tree = {}

def fix_data_case(string):
	return string[0].lower() + string[1:]

def get_record_from_tree(tree, rtype, id):
	if rtype not in build_tree:
		build_tree[rtype] = {}
	if id not in build_tree[rtype]:
		build_tree[rtype][id] = Record(rtype)

	return build_tree[rtype][id]

class Record:
	def __init__(self, type):
		self.__type = type

	def dictionary(self):
		dictionary = {}

		for key, value in self.__dict__.items():
			if isinstance(value, Record):
				print value.__dict__
				value = { 'type': self.__type, 'id': 4 }
			dictionary[key] = value

		return dictionary
	def load(self, data, tree):
		for key, value in data.items():
			if key.endswith('Id') and not key == 'Id':
				key = key[:-2]
				value = get_record_from_tree(tree, key, value)

			key = fix_data_case(key)
			self.__dict__[key] = value

def objectify(data, table, tree):
	record = get_record_from_tree(tree, table, data['Id'])
	record.load(data, tree)
	return record

class Anvil:
	structure = [
		'Attendance',
		'AttendanceType',
		'AssignmentCategory',
		'AssignmentGrade',
		'Assignment',
		'Course',
		'School',
		'Image',
		'Teacher',
		'Gradingscale'
	]

	def __init__(self):
		self.__dependencies = {}
		self.__tree = {}
		self.dbo = DBO()

	def __getitem__(self, key):
		return self.__tree[key]

	def __setitem__(self, key, value):
		self.__tree[key] = value

	def connect_to_db(self, **kwargs):
		self.dbo.connect(**kwargs)

	def load(self, table, filters):
		records = self.dbo.get_records(table=table, filters=filters)

		self.__tree[table] = {record['Id']: objectify(record, table, self.__tree) for record in records}

		for record in records:
			self.find_dependencies(record)

		self.resolve_dependencies()

	def update(self, table, record):
		return self.dbo.update_record(table=table, record=record)

	def find_dependencies(self, record):
		for key, value in record.items():
			if key.endswith('Id'):
				type = key[:-2]

				if not type in Anvil.structure:
					continue

				if type in ['Teacher']: type = 'User'

				if value is not None:
					del record[key]
					found = get_record_from_tree(self.__tree, type, value)
					record[key[:-2]] = found

					if not type in self.__dependencies:
						self.__dependencies[type] = set()

					self.__dependencies[type].add(value)

	def resolve_dependencies(self):
		dependencies = self.__dependencies
		self.__dependencies = {}

		for type, idlist in dependencies.items():
			records = self.dbo.get_records(table=type, filters={ 'Id': idlist })

			if type not in self.__tree:
				self.__tree[type] = {}

			for record in records:
				id = record['Id']
				found = get_record_from_tree(self.__tree, type, id)
				found.load(record, self.__tree)
				self.__tree[type][id] = found
				self.find_dependencies(record)

		if dependencies:
			self.resolve_dependencies()

	def jsonify(self):
		tree = self.__tree
		for key, records in tree.items():
			for id, record in records.items():
				if isinstance(record, Record):
					tree[key][id] = record.dictionary()
		return jsonify(**tree)
