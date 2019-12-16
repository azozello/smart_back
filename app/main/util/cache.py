from pymemcache.client import base


class Cache:
    def __init__(self):
        self.client = base.Client(('localhost', 11211))

    def add(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key=key)


if __name__ == '__main__':
    cache = Cache()
    print(cache.get('some_key'))
    cache.add('some_key', {'some': 'value'})
    print(type(cache.get('some_key')))
