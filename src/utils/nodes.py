class Node:
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash(self.id)


class StartNode(Node):
    def __init__(self, id: int):
        super().__init__(id)
        self.type = "start"

    def __repr__(self):
        return "Start"


class MessageNode(Node):
    def __init__(self, id, status, message):
        super().__init__(id)
        self.status = status
        self.message = message
        self.type = "message"

    def __repr__(self):
        return f"Message: {self.id}\n Status: {self.status}\n Message: {self.message}"


class ConditionNode(Node):
    def __init__(self, id, condition):
        super().__init__(id)
        self.condition = condition
        self.yes_node = ""
        self.no_node = ""
        self.type = "condition"

    def __repr__(self):
        return f"Condition {self.id}: {self.condition}"


class EndNode(Node):
    def __init__(self, id):
        super().__init__(id)
        self.type = "end"

    def __repr__(self):
        return f"End"
