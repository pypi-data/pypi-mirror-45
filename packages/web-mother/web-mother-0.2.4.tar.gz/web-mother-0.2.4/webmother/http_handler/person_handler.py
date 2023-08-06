# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
import json
from ..service.async_wrap import ctrl_person


class PersonHandler(base_handler.BaseHandler):
    """
    组织成员的增删改查
    """

    @myweb.authenticated
    @gen.coroutine
    def post(self, oid, indicator, **kwargs):
        employment = self.request.headers.get('x-signed-employment')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))

        ret = yield ctrl_person.add(oid, indicator, data, employment, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid, indicator, **kwargs):
        employment = self.request.headers.get('x-signed-employment')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_person.get(oid, indicator, employment, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def put(self, oid, indicator, **kwargs):
        employment = self.request.headers.get('x-signed-employment')
        access_token = self.request.headers.get('x-access-token')

        data = json.loads(self.request.body.decode('utf-8'))

        ret = yield ctrl_person.update(oid, indicator, data, employment, access_token)
        return self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def delete(self, oid, indicator, **kwargs):
        employment = self.request.headers.get('x-signed-employment')
        access_token = self.request.headers.get('x-access-token')

        ret = yield ctrl_person.remove(oid, indicator, employment, access_token)
        return self.write(ret)


class PersonsHandler(base_handler.BaseHandler):
    """
    获取组织下的用户列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self, oid, **kwargs):
        employment = self.request.headers.get('x-signed-employment')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_person.query(oid, employment, access_token)
        return self.write({'list': array})


