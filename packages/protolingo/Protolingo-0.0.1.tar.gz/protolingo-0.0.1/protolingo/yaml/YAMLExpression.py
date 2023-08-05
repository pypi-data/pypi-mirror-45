import yaml
from protolingo.semantics.Expression import Expression

class YAMLExpression(Expression, yaml.YAMLObject):

    def __init__(self, id, depends_on=[], output=None, exit=None, exitCode = None):
        super(YAMLExpression, self).__init__(id, depends_on, output, exit, exitCode)