
class ViewGroup:
    def __init__(self, name, exclude=None):
        self.name=name
        self.exclude=exclude

    def encode(self):
        obj = {self.name: {}}
        if obj != None:
            obj[self.name]["excludeProperties"] = self.exclude
        return obj

class EntitySeed:
    def __init__(self, vertex):
        self.vertex = vertex

    def encode(self):
        obj = {
            "class": "uk.gov.gchq.gaffer.operation.data.EntitySeed",
            "vertex": self.vertex
        }
        return obj

class EdgeSeed:
    def __init__(self, source=None, destination=None, directedType=None,
                 matchedVertex=None):
        self.source = source
        self.destination = destination
        self.directedType = directedType
        self.matchedVertex = matchedVertex

    def encode(self):
        obj = {
            "class": "uk.gov.gchq.gaffer.operation.data.EdgeSeed",
        }
        if self.source != None:
            obj["source"] = self.source
        if self.destination != None:
            obj["destination"] = self.destination
        if self.matchedVertex != None:
            obj["matchedVertex"] = self.matchedVertex
        if self.directedType != None:
            obj["directedType"] = self.directedType
        return obj
                        
class GetAllElements:

    ALL=[]
    NONE=None
    
    def __init__(self, entities=ALL, edges=ALL):
        self.entities = entities
        self.edges = edges

    def encode_group(self, g):
        if type(g) == str:
            return {g: {}}
        if isinstance(g, ViewGroup):
            return g.encode()
        raise TypeError("Needs to be string, unicode or GroupView")
        
    def encode(self):
        op = {
            "class" : "uk.gov.gchq.gaffer.operation.impl.get.GetAllElements",
            "view": {
            }
        }
        if self.entities != None:
            op["view"]["entities"] = {}
            for group in self.entities:
                op["view"]["entities"] = dict(op["view"]["entities"], **self.encode_group(group))
        if self.edges != None:
            op["view"]["edges"] = {}
            for group in self.edges:
                op["view"]["edges"] = dict(op["view"]["edges"], **self.encode_group(group))
        return op
    
    def set_entities(self, entities=ALL):
        self.entities=entities
    
    def set_edges(self, edges=ALL):
        self.edges=edges

class GetElements:

    ALL=[]
    NONE=None
    
    def __init__(self, entities=ALL, edges=ALL, include="EITHER"):
        self.entities = entities
        self.edges = edges
        self.include = include
        self.input = None

    def set_input(self, input):
        self.input = input

    def encode_group(self, g):
        if type(g) == str:
            return {g: {}}
        if isinstance(g, ViewGroup):
            return g.encode()
        raise TypeError("Needs to be string, unicode or GroupView")
    
    def encode(self):
        op = {
            "class" : "uk.gov.gchq.gaffer.operation.impl.get.GetElements",
            "view": {
            },
            "includeIncomingOutGoing": self.include
        }
        if self.input != None:
            op["input"] = [v.encode() for v in self.input]
        if self.entities != None:
            op["view"]["entities"] = {}
            for group in self.entities:
                op["view"]["entities"] = dict(op["view"]["entities"], **self.encode_group(group))
        if self.edges != None:
            op["view"]["edges"] = {}
            for group in self.edges:
                op["view"]["edges"] = dict(op["view"]["edges"], **self.encode_group(group))
        return op
    
    def set_entities(self, entities=ALL):
        self.entities=entities
    
    def set_edges(self, edges=ALL):
        self.edges=edges

class OperationChain:

    def __init__(self, operations=[]):
        self.operations = operations

    def encode(self):
        return {
            "class": "uk.gov.gchq.gaffer.operation.OperationChain",
            "operations": [ op.encode() for op in self.operations ]
        }
    
    def add(self, op):
        self.operations.append(op)

class Limit:

    def __init__(self, limit):
        self.limit = limit

    def encode(self):
        return {
            "class": "uk.gov.gchq.gaffer.operation.impl.Limit",
            "resultLimit": self.limit
        }

class GetWalks:

    def __init__(self, operations=[], limit=None):
        self.operations = operations
        self.limit = limit

    def encode(self):
        op = {
            "class": "uk.gov.gchq.gaffer.operation.impl.GetWalks",
            "operations": [v.encode() for v in self.operations]
        }
        if self.limit != None:
            op["resultsLimit"] = self.limit
        return op
    
    def add(self, op):
        self.operations.append(op)

    def set_limit(self, limit):
        self.limit = limit
