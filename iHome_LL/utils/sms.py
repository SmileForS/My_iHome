# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome_LL.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8a216da862764869016285c411d0078a'

# ���ʺ�Token
accountToken = 'f1e57a76cebb4a6d8195a62158ed54ba'

# Ӧ��Id
appId = '8a216da862764869016285c412350791'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

def sendTemplateSMS(to, datas, tempId):
    # ��ʼ��REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)


# ����1:Ŀ���ֻ�
# ����2����һ��Ԫ�أ�������֤�룻�ڶ���������������֤�����Ч��
# ����3�����ŵ�ģ�壬Ĭ���ṩ��ģ���id��1
sendTemplateSMS('18390994494', ['666666', '5'], '1')