import MySQLdb

class DBO:
    def connect(self, **kwargs):
        self._connection = MySQLdb.connect(**kwargs)

    def get_records(self, table, filters=None):
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

    def update_record(self, table, record):
        updates = []
        for key, value in record.items():
            if isinstance(value, basestring):
                value = self._connection.escape_string(value)
            updates.append('`{0}`="{1}"'.format(key, value))
        update = ','.join(updates)
        sql = 'UPDATE `{0}` SET {1} WHERE id={2}'.format(table, update, record['id'])

        with self._connection as cursor:
            cursor.execute(sql)
        return {}