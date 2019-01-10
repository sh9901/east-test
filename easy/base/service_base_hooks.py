import logging
from requests.models import Response
from easy.utils import jsonUtil


# naming convention: name ends with '_g' will be used globally by default

# TODO 检查http_code=200是否加入默认检查TBD
def check_http_code_g(resp: Response, expected_http_code):
    """检查httpcode"""
    assert resp.status_code == expected_http_code, 'resp.status_code:%s与期望:%s不一致' % (resp.status_code, expected_http_code)


def check_status_code(resp: Response, expected_status_code=0):
    """检查resp.data内的status值"""
    resp_status = None
    try:
        # 此处尽量使用resp.model.status取值，顺便测试下model_hook健壮性
        resp_status = resp.model.status
    except Exception as e_model:
        logging.info("check_status_code: 尝试使用Response.model.status获取status值失败:%s,使用resp.json['status']获取" % e_model)
        try:
            resp_status = resp.json()['status']
        except Exception as e_json:
            logging.info("check_status_code: 尝试使用resp.json()['status']获取status值也失败:%s" % e_json)
    finally:
        if resp_status is None:
            raise
    assert resp_status == expected_status_code, 'check_status_code: resp.status:%s 与期望值:%s 不一致' % (resp_status, expected_status_code)


def check_response_in_time_g(resp: Response, time_threshold=10):
    """检查http请求超时否"""
    assert resp.elapsed.seconds < time_threshold, '请求超时,%s > %s' % (resp.elapsed.seconds, time_threshold)


def print_response_info_g(resp: Response):
    logging.info('Response.status_code: %s' % resp.status_code)
    logging.info('Response.elapsed: %s' % resp.elapsed)
    logging.info('Response.content: \n%s' % jsonUtil.pformat_resp(resp))


def ensure_utf8_g(resp: Response):
    """解决中文乱码问题"""
    resp.encoding = 'utf8'


def check_response_data_is_null(resp: Response):
    """不是所有的http请求都是json返回, 可能是image/png等, 不可滥用"""
    assert resp.json() and resp.json()['data'] is None


class BaseHooks(object):
    @staticmethod
    def hook_http_code_in_class_static(resp: Response, http_code=200):
        assert resp.status_code == http_code

    def hook_http_code_in_class_instance(self, resp: Response, http_code=200):
        assert resp.status_code == http_code
