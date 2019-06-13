
from datetime import datetime,date
def json_serial(obj):
    if isinstance(obj,(date,datetime)):
        return obj.isoformat()
    return TypeError("Type {}s not serializable".format(type(obj)))