import jwt
from datetime import datetime


current_time = datetime.utcnow()

data=jwt.encode({
    "name":"yk",
    "id":1,
    "exp":current_time
},"abc").decode('utf8')


import time

time.sleep(2)

send_data = jwt.decode(data,"abc",leeway=1,options={"verify_exp":True})

print(send_data)