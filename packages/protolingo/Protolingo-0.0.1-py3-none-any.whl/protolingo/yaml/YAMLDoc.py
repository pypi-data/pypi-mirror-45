from .Parser import Parser
from functools import reduce
from protolingo.utils import gettype


class YAMLDoc:

    def __init__(self, path, params):
        self.context = {**params, "yaml":{}}
        with open(path, 'r') as file:
            self.doc = Parser.load(file)
        self.config = reduce(lambda default,item:item, [tag["config"] for tag in self.doc if type(tag) is dict and list(tag)[0] == "config"],dict())
        self.context["config"] = self.config
       
    def __iter__(self):
       for expression in Parser.parse(self.doc):
            output =  Parser.comprehend(expression, **self.context) 
            yield output
            exception = gettype(output[3])
            if(((exception is SystemExit and int(output[4]) != 0) or (exception is not SystemExit)) and self.config.get("exit_on_error",True)):
                break

    def save(self, path):
        self.close()
        Parser.save(path, self.doc)

    def close(self):
        Parser.clear(self.doc)
          
    @staticmethod
    def open(path, params):
        doc = Parser.load(path)
        return YAMLDoc(doc, params)

      
        