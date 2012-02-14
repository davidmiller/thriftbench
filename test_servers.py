"""
test_servers.py

FunkLoad test script for benchmarking Python Thrift server implementations
"""
import os
import sys
import time
from xml.sax.saxutils import quoteattr

sys.path.append(os.path.join(os.path.dirname(__file__), 'gen-py'))

from funkload import FunkLoadTestCase
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from bench import Bencher

class ServerTest(FunkLoadTestCase.FunkLoadTestCase):


    def _log_thrifty(self, method, args, response,
                     time_start, time_stop, code):
        """
        Log the call the FunkLoad way
        """
        self.total_responses += 1
        self.page_responses += 1
        info = {}
        info['cycle'] = self.cycle
        info['cvus'] = self.cvus
        info['thread_id'] = self.thread_id
        info['suite_name'] = self.suite_name
        info['test_name'] = self.test_name
        info['step'] = self.steps
        info['number'] = self.page_responses
        info['type'] = 'jsonrpc'
        info['url'] = quoteattr(str(method) + '#' + str(args))
        info['code'] = code
        info['description'] = quoteattr("Thrift service call %s" % str(method))
        info['time_start'] = time_start
        info['duration'] = time_stop - time_start
        info['result'] = self.step_success and 'Successful' or 'Failure'
        message = '''<response cycle="%(cycle).3i" cvus="%(cvus).3i" thread="%(thread_id).3i" suite="%(suite_name)s" name="%(test_name)s" step="%(step).3i" number="%(number).3i" type="%(type)s" result="%(result)s" url=%(url)s code="%(code)s" description=%(description)s time="%(time_start)s" duration="%(duration)s" />"''' % info
        self._logr(message)


    def thrift_call(self, method, *args):
        """
        Make a Thrift call, performing the appropriate FunkLoad logging

        Arguments:
        - `method`: callable
        - `*args`: arguments to pass to the method
        """
        self.steps += 1
        self.page_responses = 0
        self.logd("THRIFT %s:%s" % (str(method), str(args)))

        response = None
        t_start = time.time()
        try:
            response = method(*args)
        except:
            etype, value, tback = sys.exc_info()
            t_stop = time.time()
            t_delta = t_stop - t_start
            self.total_time += t_delta
            self.step_success = False
            self.test_status = 'Error'
            self.logd(' Failed in %.3fs' % t_delta)
            self._log_thrifty(method, args, response,
                                       t_start, t_stop,- 1)
            raise
        t_stop = time.time()
        t_delta = t_stop - t_start
        self.total_time += t_delta

        self.total_pages += 1
        self.logd(' Done in %.3fs' % t_delta)
        self._log_thrifty(method, args, response,
                                   t_start, t_stop, 200)
        self.sleep()
        return response

    def setUp(self):
        """
        Prepare the client
        """
        self.transport = TSocket.TSocket('localhost', 30303)
        self.transport = TTransport.TBufferedTransport(self.transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = Bencher.Client(protocol)
        self.transport.open()

    def tearDown(self):
        self.transport.close()

    def test_sortset(self):
        """ Simple test sorting a list of integers """
        numbers = [1, 4, 7665, 23, 78, 435,4, 32534, 234, 2345, 256,
                   2454, 264, 89, 2, 4, 8, 4, 23, 4532, 574, 1, 23452,
                   5635, 4757, 74, 47, 90, 36, 2, 6, 47, 457, 5, 76, 6,
                   2, 43, 56, 7, 89, 2, 534234, 45, 78, 4, 45, 23]
        self.thrift_call(self.client.ping)
        self.thrift_call(self.client.sortset, numbers)


