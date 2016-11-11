import MySQLdb

class DBO:
    def connect(self, **kwargs):
        self._connection = MySQLdb.connect(**kwargs)

    def get_records(self, table=None, filters=None):
        sql = 'SELECT * FROM `{0}`'.format(table)

        if filters is not None:
            wheres = []
            for (key, value) in filters.items():
                wheres.append('{0} IN ("{1}")'.format(key, '","'.join([ str(item) for item in value])))

            where = ' AND '.join(wheres)
            sql += ' WHERE {0}'.format(where)

        with self._connection as cursor:
            print sql
            cursor.execute(sql)
            field_names = [i[0] for i in cursor.description]
            records = []

            for row in cursor.fetchall():
                record = {}
                for i in range(len(field_names)):
                    key = field_names[i]
                    record[key] = row[i]
                records.append(record)

        return records
