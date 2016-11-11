from dbo import DBO


class Anvil:
	structure = [
		'Attendance',
		'AttendanceType',
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
		self.dbo = DBO()

	def connect_to_db(self, **kwargs):
		self.dbo.connect(**kwargs)

	def get(self, table, filters, tree={}):
		records = self.dbo.get_records(table=table, filters=filters)

		tree[table] = records

		for record in records:
			self.find_dependencies(record, tree)

		self.resolve_dependencies(tree)

		return tree

	def find_dependencies(self, record, tree):
		def has_record(records, id):
			for record in records:
				if record['Id'] == id:
					return True

			return False


		for key, value in record.items():
			if key.endswith('Id'):
				type = key[:-2]

				if not type in Anvil.structure:
					continue

				if type in ['Teacher']: type = 'User'

				if value is not None:
					record[key[:-2]] = { 'type': type, 'id': value }

					if not type in self.__dependencies:
						self.__dependencies[type] = set()

					self.__dependencies[type].add(value)

	def resolve_dependencies(self, tree):
		dependencies = self.__dependencies
		self.__dependencies = {}

		for type, idlist in dependencies.items():
			records = self.dbo.get_records(table=type, filters={ 'Id': idlist })

			if type not in tree:
				tree[type] = []

			tree[type] += records

			for record in records:
				self.find_dependencies(record, tree)

			self.resolve_dependencies(tree)
