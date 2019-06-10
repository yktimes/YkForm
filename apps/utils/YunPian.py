import requests


class YunPian:

    def __init__(self,api_key):
        self.api_key = api_key

    def send_single_sms(self,code,mobile):
        # 发送单条短信
        url = "https://sms.yunpian.com/v2/sms/single_send.json"

        text="【树圈网】您的验证码是{}".format(code)
        res = requests.post(url,data={
            "apikey":self.api_key,
            "mobile":mobile,
            "text":text
        })

        return res

if __name__ == "__main__":
    # TODO api_key
    yun_pian = YunPian("fbdaa372a39ac1c459c27cf4cebf139f")
    res = yun_pian.send_single_sms("1234", "18089389137")
    print(res.text)
