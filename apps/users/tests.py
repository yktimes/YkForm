
import requests
import json
web_url="http://127.0.0.1:8888"
def test_sms():
    url="{}/code/".format(web_url)
    data={
        "mobile":"18089389137"
    }
    res = requests.post(url,json=data)

    print(json.loads(res.text))



def test_register():
    url="{}/register/".format(web_url)

if __name__ == '__main__':
    test_sms()