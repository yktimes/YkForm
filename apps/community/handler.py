import json
import uuid
import aiofiles
import os

from YkForm.handler import RedisHandler
from playhouse.shortcuts import model_to_dict
from apps.utils.form_decorators import authenticated_async

from apps.utils.util_func import json_serial
from apps.community.forms import *
from apps.community.models import *


# 创建小组
class GroupHandler(RedisHandler):

    async def get(self, *args, **kwargs):
        re_data = []

        # community_query = CommunityGroup.select()
        community_query = CommunityGroup.extend()

        # 根据类别进行过滤
        c = self.get_argument("c", None)
        if c:
            community_query.filter(CommunityGroup.category == c)

        # 根据参数进行排序
        order = self.get_argument("o", None)
        if order:
            if order == "new":
                community_query = community_query.order_by(CommunityGroup.add_time)
            elif order == "hot":
                community_query = community_query.order_by(CommunityGroup.member_nums)

        limit = self.get_argument("limit", None)
        if limit:
            community_query = community_query.limit(int(limit))

        groups = await self.application.objects.execute(community_query)

        for group in groups:
            group_dict = model_to_dict(group)
            group_dict["front_image"] = "{}/media/{}".format(self.settings["SITE_URL"], group_dict["front_image"])

            re_data.append(group_dict)

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, *args, **kwargs):

        re_data = {}

        # 注意这里就不能使用 from_json
        group_form = CommunityGroupForm(self.request.body_arguments)

        if group_form.validate():
            # 自己完成图片字段验证
            files_meta = self.request.files.get("front_image", None)
            if not files_meta:
                self.set_status(400)
                re_data["front_image"] = "请上传图片"

            else:
                # 完成图片保存并设置
                # 通过aiofiles写
                new_filename = ""
                # 1 文件名
                for meta in files_meta:
                    filename = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    file_path = os.path.join(self.settings['MEDIA_ROOT'], new_filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta['body'])

                group = await self.application.objects.create(CommunityGroup,
                                                              add_user=self.current_user,
                                                              name=group_form.name.data,
                                                              category=group_form.category.data,
                                                              desc=group_form.desc.data,
                                                              notice=group_form.notice.data,
                                                              front_image=new_filename
                                                              )
                re_data["id"] = group.id

        else:
            self.set_status(400)
            for field in group_form.errors:
                re_data[field] = group_form.errors[field][0]

        self.finish(re_data)


# 申请加入小组
class GroupMemberHandler(RedisHandler):

    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        re_data = {}

        param = self.request.body.decode('utf8')
        param = json.loads(param)

        form = GroupApplyForm.from_json(param)
        if form.validate():
            try:
                # 获取要加入的小组
                group = await self.application.objects.get(CommunityGroup, id=int(group_id))
                # 是否加入过
                existed = await self.application.objects.get(
                    CommunityGroupMember,
                    community=group,
                    user=self.current_user
                )

                if existed:
                    self.set_status(400)
                    re_data["non_field"] = "用户已经加入"



            except CommunityGroup.DoesNotExist as e:
                self.set_status(404)

            except CommunityGroupMember.DoesNotExist as e:
                # 没有加入就创建
                community_member = await self.application.objects.create(
                    CommunityGroupMember,
                    community=group,
                    user=self.current_user,
                    apply_reason=form.apply_reason.data
                )

                re_data["id"] = community_member.id

        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]

        self.finish(re_data)


# 获取小组详情
class GroupDetailHandler(RedisHandler):
    @authenticated_async
    async def get(self, group_id, *args, **kwargs):
        re_data = {}
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))

            item_dict = {}
            item_dict["id"] = group.id
            item_dict["name"] = group.name
            item_dict["desc"] = group.desc
            item_dict["notice"] = group.notice
            item_dict["member_nums"] = group.member_nums
            item_dict["post_nums"] = group.post_nums
            item_dict["front_image"] = "{}/media/{}".format(self.settings["SITE_URL"], group.front_image)

            re_data = item_dict


        except CommunityGroup.DoesNotExist as e:
            self.set_status(400)

        self.finish(re_data)


class PostHandler(RedisHandler):

    @authenticated_async
    async def get(self, group_id, *args, **kwargs):
        # 获取小组内的帖子
        post_list = []
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            # 要判断发帖是否在这个组
            group_member = await self.application.objects.get(
                CommunityGroupMember,
                user=self.current_user,
                community=group,
                status="agree")
        except User.DoesNotExist as e:
            self.set_status(404)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)

        else:
            posts_query = Post.extend()
            c = self.get_argument("c", None)
            if c == "hot":
                posts_query = posts_query.filter(Post.is_hot == True)
            if c == "excellent":
                posts_query = posts_query.filter(Post.is_excellent == True)
            posts = await self.application.objects.execute(posts_query)

            for post in posts:
                item_dict = {
                    "user": {
                        "id": post.user.id,
                        "nick_name": post.user.nick_name
                    },
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "comment_nums": post.comment_nums
                }
                post_list.append(item_dict)

        self.finish(json.dumps(post_list))

    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        re_data = {}

        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            # 要判断发帖是否在这个组
            group_member = await self.application.objects.get(
                CommunityGroupMember,
                user=self.current_user,
                community=group,
                status="agree")
        except User.DoesNotExist as e:
            self.set_status(404)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)

        else:
            param = self.request.body.decode('utf8')
            param = json.loads(param)

            form = PostForm.from_json(param)
            if form.validate():
                post = await self.application.objects.create(
                    Post, user=self.current_user,
                    title=form.title.data,
                    content=form.content.data,
                    group=group
                )

                re_data["id"] = post.id

            else:
                self.set_status(400)
                for field in form.errors:
                    re_data[field] = form.errors[field][0]

        self.finish(re_data)


class PostDetailHandler(RedisHandler):



    @authenticated_async
    async def get(self, post_id, *args, **kwargs):
        # 获取某一个帖子的详情
        re_data = {}
        post_details = await self.application.objects.execute(Post.extend().where(Post.id == int(post_id)))
        re_count = 0
        for data in post_details:

            user = {}
            user["id"]=data.user.id
            user["nick_name"] = data.user.nick_name or data.user.mobile

            item_dict = {}
            # item_dict["user"] = model_to_dict(data.user)
            item_dict["user"] = user
            item_dict["title"] = data.title
            item_dict["content"] = data.content
            item_dict["comment_nums"] = data.comment_nums
            item_dict["add_time"] = data.add_time.strftime("%Y-%m-%d")
            re_data = item_dict

            re_count += 1

        if re_count == 0:
            self.set_status(404)

        self.finish(re_data)
