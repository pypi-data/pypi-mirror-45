import yaml
import pykka
import inspect
import traceback
from abc import ABC, abstractmethod
 
class Node():

    def __init__(self, id, depends_on, output, exit, exitCode):
        super(Node, self).__init__()
        self.id = id
        if(output):
            self.output = output
        else:
            self.output = [id]
        self.exit = exit
        self.exitCode = exitCode
        self.depends_on = depends_on
          
    @abstractmethod
    def exec(self, **kwargs):
        pass

    def isrunnable(self):
        return len(self.output) == 1

