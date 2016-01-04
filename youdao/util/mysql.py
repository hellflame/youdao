

class Mysql:
    def __init__(self, user='root', password='', host='127.0.0.1', db_name='youdao'):
        import MySQLdb
        self.connect = MySQLdb.connect(host=host,
                                       user=user,
                                       passwd=password,
                                       db=db_name,
                                       charset='utf8')
        self.cursor = self.connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        self.db_name = db_name

    def insert(self, phrase, translation, web, basic):
        self.cursor.execute("INSERT INTO youdao (phrase, translation, web, basic) "
                            "VALUE ('{}', '{}', '{}', '{}')".format(phrase,
                                                                    translation,
                                                                    web,
                                                                    basic))

    def phrase_get(self, phrase):
        self.cursor.execute("SELECT * FROM youdao WHERE phrase = '{}'".format(phrase))
        result = self.cursor.fetchone()
        return result

    def create_table(self):
        self.cursor.execute("CREATE TABLE youdao ("
                            "phrase text,"
                            "translation text,"
                            "web text,"
                            "basic text)"
                            )

    def clear_all(self):
        self.cursor.execute("DROP TABLE youdao")
        self.create_table()

    def update_phrase(self, phrase, data):
        sql = "UPDATE youdao SET "
        for i in data:
            sql += " {} = '{}' ,".format(i, data[i])
        sql = sql[:-1] + " where phrase = '{}' ".format(phrase)
        self.cursor.execute(sql)

    def __del__(self):
        self.connect.commit()
        self.connect.close()
