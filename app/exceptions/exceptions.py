class JSONException(Exception):
    def __init__(self, code, data):
        self.code = code
        self.data = data