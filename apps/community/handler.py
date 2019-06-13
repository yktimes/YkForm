from tornado.web import authenticated
from YkForm.handler import RedisHandler
from apps.users.models import User
from apps.utils.form_decorators import authenticated_async
import json
from playhouse.shortcuts import model_to_dict
from apps.community.forms import CommunityGroupForm
from apps.community.models import CommunityGroupMember,CommunityGroup
import uuid
import aiofiles
import os


from apps.utils.util_func import json_serial






class GroupHandler(RedisHandler):


    async def get(self,*args,**kwargs):
        re_data = []

        # community_query = CommunityGroup.select()
        community_query = CommunityGroup.extend()

        # 根据类别进行过滤
        c = self.get_argument("c",None)
        if c:
            community_query.filter(CommunityGroup.category==c)

        # 根据参数进行排序
        order = self.get_argument("o",None)
        if order:
            if order=="new":
                community_query=community_query.order_by(CommunityGroup.add_time)
            elif order=="hot":
                community_query=community_query.order_by(CommunityGroup.member_nums)

        limit = self.get_argument("limit",None)
        if limit:
            community_query = community_query.limit(int(limit))

        groups = await self.application.objects.execute(community_query)

        for group in groups:
            group_dict=model_to_dict(group)
            group_dict["front_image"]="{}/media/{}".format(self.settings["SITE_URL"],group_dict["front_image"])

            re_data.append(group_dict)


        self.finish(json.dumps(re_data,default=json_serial))

    @authenticated_async
    async def post(self,*args,**kwargs):


        re_data = {}


        # 注意这里就不能使用 from_json
        group_form = CommunityGroupForm(self.request.body_arguments)

        if group_form.validate():
            # 自己完成图片字段验证
            files_meta = self.request.files.get("front_image",  None)
            if not files_meta:
                self.set_status(400)
                re_data["front_image"]="请上传图片"

            else:
                # 完成图片保存并设置
                # 通过aiofiles写
                new_filename=""
                # 1 文件名
                for meta in files_meta:
                    filename = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(),filename=filename)
                    file_path = os.path.join(self.settings['MEDIA_ROOT'],new_filename)
                    async with aiofiles.open(file_path,'wb') as f:
                        await f.write(meta['body'])

                group = await self.application.objects.create(CommunityGroup,
                                                              add_user =self.current_user,
                                                              name = group_form.name.data,
                                                              category = group_form.category.data,
                                                              desc=group_form.desc.data,
                                                              notice=group_form.notice.data,
                                                              front_image = new_filename
                                                              )
                re_data["id"]=group.id

        else:
            self.set_status(400)
            for field in group_form.errors:
                re_data[field]=group_form.errors[field][0]


        self.finish(re_data)

