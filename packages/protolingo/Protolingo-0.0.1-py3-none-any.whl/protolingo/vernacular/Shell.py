import os
import sys
import subprocess
from protolingo.utils import escape
from protolingo.yaml.YAMLExpression import YAMLExpression


class Shell(YAMLExpression):
    yaml_tag = u'!shell'

    def __init__(self, id, depends_on, commands, output=None, exit=None, exitCode=None):
        super(YAMLExpression, self).__init__(id, depends_on, output, exit, exitCode)
        self.commands = commands

    def exec(self,**kwargs):
        try:
            for command in self.commands:
                print(command)
                proc = subprocess.Popen(command,
                env = {**os.environ},
                shell  = True,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                )
                stdout, stderr = proc.communicate()
                print(escape(stdout.decode("utf-8")), file=sys.stdout, end = '')
                print(escape(stderr.decode("utf-8")), file=sys.stderr, end = '')
                if proc.returncode != 0 :
                    break
            sys.exit(proc.returncode)
        except Exception as e:
            print(e.__str__(), file=sys.stderr)
            raise

    def __repr__(self):
        return "%s(id=%r, commands=%r)" % (
            self.__class__.__name__, self.id, self.commands)

