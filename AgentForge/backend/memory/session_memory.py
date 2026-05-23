class SessionMemory:

    def __init__(self):
        self.memory = {}

    def save(self, image_hash, description, prompt):
        self.memory["image_hash"] = image_hash
        self.memory["description"] = description

        history = self.memory.get("history", [])
        history.append(prompt)

        self.memory["history"] = history[-5:]

    def get_last_description(self):
        return self.memory.get("description")

    def get_hash(self):
        return self.memory.get("image_hash")

    def get_history(self):
        return self.memory.get("history", [])