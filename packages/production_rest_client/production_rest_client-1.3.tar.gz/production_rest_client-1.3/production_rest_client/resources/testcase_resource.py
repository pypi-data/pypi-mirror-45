# coding=utf-8
# pylint: disable=import-error, broad-except
import json
from resources.models.helper import rest_get_call
from resources.models.helper import rest_post_json_call
from resources.models.helper import rest_delete_call


class TestCaseResource(object):

    def __init__(self, host, port, session, time_out):
        self.host = host
        self.port = port
        self.session = session
        self.time_out = time_out

    def list(self, filter_):
        """
        :param filter_: list filter
        :return: type: list, return test case list meet the filter
        """
        url_ = "http://{0}:{1}/tc/{2}".format(self.host, self.port, filter_)
        try:
            result = rest_get_call(url_, self.session, self.time_out)
            response_ = result.json()
        except Exception as get_except:
            response_ = {"resource":{"msg": get_except, "result": False, "key": None, "state": None, "data": None}}
        return response_["resource"]['data']

    def run(self, test_case, mode="sync", **kwargs):
        """
        :param test_case: type string, test case name
        :param  mode: sync or async, run test case
        :return: type bool, return test case run result
        """
        data = {"tc": test_case, "mode":mode}
        for key in kwargs:
            data[key] = kwargs[key]
        try:
            url_ = "http://{0}:{1}/tc".format(self.host, self.port)
            result = rest_post_json_call(url_, self.session, json.dumps(data), self.time_out)
            response_ = result.json()
        except Exception as get_except:
            response_ = {"resource":{"msg": get_except, "result": False, "key": None, "state": None}}
        return response_["resource"]

    def get_async_result(self, key):
        url_ = "http://{0}:{1}/tc/results/{2}".format(self.host, self.port, key)
        try:
            result = rest_get_call(url_, self.session, self.time_out)
            response_ = result.json()
        except Exception as get_except:
            response_ = {"resource":{"msg": get_except, "result": False, "key": None, "state": None}}
        return response_["resource"]

    def stop_tests(self):
        url_ = "http://{0}:{1}/tc".format(self.host, self.port)
        try:
            result = rest_delete_call(url_, self.session, self.time_out)
            response_ = result.json()
        except Exception as get_except:
            print(get_except)
            response_ = {"resource":{"msg": get_except, "result": False, "key": None, "state": None}}
        return response_["resource"]["result"]
