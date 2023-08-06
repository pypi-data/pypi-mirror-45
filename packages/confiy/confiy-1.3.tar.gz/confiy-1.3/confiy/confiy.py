import re

class confiy():
    data = None

    def __init__(self, file=None):
        if file is not None:
            try:
                with open(str(file), 'r') as file:
                    self.data = file.read()
            except:
                pass
        else:
            f = 'conf.cnf'
            try:
                with open(f, 'r') as f:
                    self.data = f.read()
            except:
                pass

    def getValue(self, key):
        result = None
        if self.data is not None:
            if str is not None:
                result = {v for k, v in re.findall(r'(' + key + ')=(".*?"|\S+)', self.data)}
            if len(result) > 0:
                if len(result) == 1:
                    return result.pop()
                else:
                    return list(result)
            else:
                return None
        else:
            return None

# print confiy().getValue(key='AMQP_URI')