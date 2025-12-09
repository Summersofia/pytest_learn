import pytest
import time
import requests
import json

class TestLogin(object):

    @pytest.mark.positive
    def test_login_success(self, zby_user, login_config):
        responses_login = requests.post(url=login_config['url_login'], headers=login_config['headers'], data=zby_user['raw_body'])
        try:
            resp_json = responses_login.json()
            msg = resp_json['msg']
            if '是否强行登录并清除' in msg:
                pytest.fail(f"账号已在其他地方登录，请先推出登录")
            else:
                resp_json = responses_login.json()
                userid = resp_json['userCode']
                token = resp_json['authorization']
                assert userid == zby_user['body']['userId']
                assert 'ngTokenKey' in token
        except json.JSONDecodeError  as e:
            pytest.fail(f'转换json失败，resp:{responses_login.text},Error:{e}')
        except AssertionError as e:
            pytest.fail(f'断言失败，resp:{responses_login.text},Error:{e}')
        except Exception as e:
            pytest.fial(f'其他错误，Error:{e}')

    @pytest.mark.positive
    def test_login_occupied(self, zby_user, login_config, unlogin_config):
        responses_login = requests.post(url=login_config['url_login'], headers=login_config['headers'], data=zby_user['raw_body'])
        try:
            login_json = responses_login.json()
            msg_json = json.loads(login_json['msg'])
            msg = login_json['msg']
            if '是否强行登录并清除' in msg:
                # 获取清除登录接口所用传参
                sessionID = msg_json['sessionID']
                database = zby_user['body']['dataBase']
                userId = msg_json['userId']
                # 调用fixture获取完整请求信息
                data_unlogin = unlogin_config(sessionId=sessionID, dataBase=database, userId=userId)
                # 触发请求
                response = requests.request("POST", data_unlogin['url_unlog'], headers=data_unlogin['headers'], data=data_unlogin['payload'])
                assert response.json()['Status'] == 'success'
            else:
                pytest.fail(f'测试数据准备有误，需准备二次登录的账号')
        except Exception as e:
            pytest.fial(f'其他错误，Error:{e}')
        except AssertionError as e:
            pytest.fail(f'断言失败，resp:{responses_login.text},Error:{e}')
        except AssertionError as e:
            pytest.fail(f'断言失败，resp:{responses_login.text},Error:{e}')

    @pytest.mark.negative
    def test_login_wrong_pwd(self, wrong_pwd, login_config):
        responses_login = requests.post(url=login_config['url_login'], headers=login_config['headers'], data=wrong_pwd['raw_body'])
        try:
            resp_json = responses_login.json()
            msg = resp_json['msg']
            if '是否强行登录并清除' in msg:
                pytest.fail(f"账号已在其他地方登录，请先推出登录")
            else:
                resp_json = responses_login.json()
                success = resp_json['success']
                msg = resp_json['msg']
                assert not success
                assert '登录失败！用户名或密码不正确' in msg
        except json.JSONDecodeError  as e:
            pytest.fail(f'转换json失败，resp:{responses_login.text},Error:{e}')
        except AssertionError as e:
            pytest.fail(f'断言失败，resp:{responses_login.text},Error:{e}')
        except Exception as e:
            pytest.fial(f'其他错误，Error:{e}')

    @pytest.mark.negative
    def test_login_wrong_user(self, wrong_user, login_config):
        responses_login = requests.post(url=login_config['url_login'], headers=login_config['headers'], data=wrong_user['raw_body'])
        try:
            resp_json = responses_login.json()
            msg = resp_json['msg']
            if '是否强行登录并清除' in msg:
                pytest.fail(f"账号已在其他地方登录，请先推出登录")
            else:
                resp_json = responses_login.json()
                success = resp_json['success']
                msg = resp_json['msg']
                assert not success
                assert '登录失败！用户名或密码不正确' in msg
        except json.JSONDecodeError  as e:
            pytest.fail(f'转换json失败，resp:{responses_login.text},Error:{e}')
        except AssertionError as e:
            pytest.fail(f'断言失败，resp:{responses_login.text},Error:{e}')
        except Exception as e:
            pytest.fial(f'其他错误，Error:{e}')

