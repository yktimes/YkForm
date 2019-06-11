from functools import partial
import json
import jwt
from tornado.web import RequestHandler
import redis
import random
from datetime import datetime
from apps.users.forms import SmsCodeForm,RegisterForm,LoginForm
from apps.utils.AsyncYunPian import AsyncYunPian
from YkForm.handler import RedisHandler
from apps.users.models import User

class SmsHandler(RedisHandler):

    def generate_code(self):
        """
        生成随机验证码
        :return:
        """
        # 生成短信验证码
        code = "%06d" % random.randint(0, 999999)

        return code

    async def post(self, *args, **kwargs):

        param = self.request.body.decode('utf8')

        re_data = {}

        param = json.loads(param)
        # 注意这里
        sms_form = SmsCodeForm.from_json(param)

        if sms_form.validate():

            code = self.generate_code()
            mobile = sms_form.mobile.data
            print(mobile)
            yun_pian = AsyncYunPian("fbdaa372a39ac1c459c27cf4cebf139f")
            print(yun_pian, "*" * 100)
            print(code)
            re_json = await yun_pian.send_single_sms(code, mobile)

            if re_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = re_json["msg"]
            else:
                print(self.redis_conn)
                # 将验证码写入redis中
                self.redis_conn.set("{}_{}".format(mobile, code), 1, 10 * 60)

        else:

            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]

        self.finish(re_data)

class RegesterHandler(RedisHandler):

    async def post(self,*args,**kwargs):
        param = self.request.body.decode('utf8')

        re_data = {}

        param = json.loads(param)
        # 注意这里
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password=register_form.password.data

            # 验证码是否正确
            redis_key ="{}_{}".format(mobile,code)
            if not self.redis_conn.get(redis_key):
                self.set_status(400)
                re_data['code']="验证码错误"

            else:
                try:
                    # 验证用户是否存在
                    existed_users = await self.application.objects.get(User,mobile=mobile)
                    self.set_status(400)
                    re_data['mobile']='用户已存在'
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User,mobile=mobile,password=password)
                    re_data['id']=user.id
        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field]=register_form[field][0]

        self.finish(re_data)


class LoginHandler(RedisHandler):


    async def post(self,*args,**kwargs):
        param = self.request.body.decode('utf8')

        re_data = {}

        param = json.loads(param)

        form = LoginForm.from_json(param)

        if form.validate():
            mobile = form.mobile.data
            password = form.password.data

            try:
                user = await self.application.objects.get(User,mobile=mobile)
                if not user.password.check_password(password):
                    self.set_status(400)
                    re_data['non_fields']="用户名或密码错误"
                else:
                    # 登陆成功

                    ployed={
                        'id':user.id,
                        'nick_name':user.nick_name,
                        # 固定参数
                        'exp':datetime.utcnow()
                    }
                    # 生成jwt

                    token = jwt.encode(ployed,self.settings['secret_key'],algorithm='HS256')

                    re_data['id']=user.id

                    if user.nick_name:
                        re_data['nick_name']=user.nick_name
                    else:
                        re_data['nick_name']=user.mobile

                    # TypeError: Object of type 'bytes' is not JSON serializable
                    # 不加decode会报错
                    re_data['token']=token.decode('utf8')


            except User.DoesNotExist as e:
                self.set_status(400)
                re_data['mobile']='用户不存在'


            self.finish(re_data)

