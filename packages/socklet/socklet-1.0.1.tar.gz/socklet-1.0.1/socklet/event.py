import json


class Event:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        s = (self.name, self.data)
        s = json.dumps(s)
        return s
