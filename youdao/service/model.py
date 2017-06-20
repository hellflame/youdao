import time
import json

try:
    import redis
    import tornado.web
    import tornado.ioloop
    import pymongo
except ImportError:
    print("""This Service Require Following Dependencies:
    redis
    tornado
    pymongo

and Databases:
    redis
    mongodb
    """)
    exit(1)


class MongoStore:
    def __init__(self, username=None, password=None, mechanism='SCRAM-SHA-1'):
        client = pymongo.MongoClient()
        if username and password:
            self.db = client.Youdao.authenticate(username, password, mechanism=mechanism)
        else:
            self.db = client.Youdao

    def insert(self, key, pronounces, translate, web_translate):
        if self.db.find_one({'key': key}):
            self.db.insert({
                'key': key,
                'pronounces': pronounces,
                'translate': translate,
                'web_translate': web_translate,
                'insert_time': int(time.time())
            })
        else:
            self.db.update({
                'key': key
            }, {
                '$set': {
                    'pronounces': pronounces,
                    'translate': translate,
                    'web_translate': web_translate,
                    'update_time': int(time.time())
                }
            })

    def fetch(self, key):
        self.db.update({
            'key': key
        }, {
            '$inc': {
                'used': 1
            }
        })
        return self.db.find_one({
            'key': key
        })


class RedisStore:
    def __init__(self, *args, **kwargs):
        self.db = redis.StrictRedis(args, kwargs)

    def fetch(self, key):
        real_key = "youdao-{}".format(key)
        if self.db.exists(real_key):
            return json.loads(self.db.get(real_key))
        return None

    def cache(self, key, data):
        real_key = "youdao-{}".format(key)
        self.db.set(real_key, json.dumps(data))


class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.send_error(404)

    def post(self):
        return self.write("hell")


routes = [(r'/', MainHandler)]

if __name__ == '__main__':
    DEBUG = True
    if DEBUG:
        settings = {
            'debug': True,
            'autoreload': True,
            'serve_traceback': True
        }
    else:
        settings = {
            'debug': False,
            'autoreload': True,
            'serve_traceback': False
        }
    app = tornado.web.Application(handlers=routes, **settings)
    app.listen(5000, address='127.0.0.1')
    tornado.ioloop.IOLoop.current().start()
