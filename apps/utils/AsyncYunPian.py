from urllib.parse import urlencode
from tornado import httpclient
from tornado.httpclient import HTTPRequest
import json

class AsyncYunPian:

    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self, code, mobile):
        # 发送单条短信

        http_client = httpclient.AsyncHTTPClient()

        url = "https://sms.yunpian.com/v2/sms/single_send.json"

        text = "【树圈网】您的验证码是{}".format(code)
        post_request = HTTPRequest(url=url, method='POST', body=urlencode({
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text}))

        print("pisss",post_request)
        res = await  http_client.fetch(post_request)
        print("ressssssssssssssssss",res)
        print(res.body.decode('utf8'))
        return json.loads(res.body.decode('utf8'))

if __name__ == '__main__':
    import tornado.ioloop

    io_loop = tornado.ioloop.IOLoop.current()

    yun_pian = AsyncYunPian("fbdaa372a39ac1c459c27cf4cebf139f")
    from functools import partial

    new_func = partial(yun_pian.send_single_sms, "1234", "18089389137")
    io_loop.run_sync(new_func)
