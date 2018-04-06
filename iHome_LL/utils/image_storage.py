# -*- coding:utf-8 -*-
# 上传和存储图片到七牛云,会返回一个key给服务器,然后服务器将这个key与七牛云网站拼成一个路径发给用户

import qiniu

access_key = "yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW"
secret_key = "bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW"
bucket_name = 'ihome'

def upload_image(image_data):
    """实现上传和存储图片到七牛云"""

    q = qiniu.Auth(access_key, secret_key)
    # key = 'hello'
    # data = 'hello qiniu!'
    token = q.upload_token(bucket_name)
    ret, info = qiniu.put_data(token, None, image_data)
    # 结果{u'hash': u'FobMwS7gPtQ6IqTyw_Kt5DfdbKsY', u'key': u'FobMwS7gPtQ6IqTyw_Kt5DfdbKsY'}
    print ret
    # 结果exception:None, status_code:200, _ResponseInfo__response:<Response [200]>, text_body:{"hash":"FobMwS7gPtQ6IqTyw_Kt5DfdbKsY","key":"FobMwS7gPtQ6IqTyw_Kt5DfdbKsY"}, req_id:th4AAKXzq9DfQiIV, x_log:body:5;s.ph;s.put.tw;s.put.tr:37;s.put.tw;s.put.tr:26;s.ph;PFDS:28;PFDS:45;body;rs37_17.sel:3;rwro.ins:3/same entry;rs37_17.sel:3;rwro.get:3;MQ;RS.not:;RS:8;rs.put:9;rs-upload.putFile:57;UP:81
    print info

    if 200==info.status_code:
        return ret.get('key')
    else:
        raise Exception('上传图片失败')



if __name__ == '__main__':
    path ="/home/python/Desktop/mm02.jpeg"
    with open(path,'rb') as file:
        upload_image(file.read())