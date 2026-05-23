class SessionMemory:
    def __init__(self):
        self.store = {}

    def get(self, session_id):
        if session_id not in self.store:
            self.store[session_id] = {
                "history": [],
                "cache": {},   # image_hash -> result
                "last_hash": None
            }
        return self.store[session_id]