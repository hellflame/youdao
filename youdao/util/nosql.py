

class Nosql:
    def __init__(self, host='127.0.0.1', port=27017):
        import pymongo
        self.client = pymongo.MongoClient(host=host, port=port)
        self.table = self.client.youdao.youdao

    def insert(self, data):
        self.table.insert(data)

    def get_data(self, phrase):
        return self.table.find_one({'phrase': phrase})

    def update(self, phrase, data):
        self.table.update({'phrase': phrase}, {'$set': data})

    def total_count(self):
        return self.table.find().count()

