#!/usr/bin/env python
import unittest

from talospider import Request


class TestRequest(unittest.TestCase):
    def setUp(self):
        super(TestRequest, self).setUp()
        self.headers = {
            "User-Agent": 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
        }
        self.payload = {'key1': 'value1', 'key2': 'value2'}

    def test_post_req(self):
        post_req = Request("http://httpbin.org/post",
                           method='POST',
                           headers=self.headers,
                           data=self.payload,
                           file_type='json')()
        self.assertEqual(post_req.html['form']['key1'], 'value1')

    def test_get_req(self):
        get_req = Request("http://httpbin.org/get",
                          headers=self.headers,
                          params=self.payload,
                          file_type='json')()
        self.assertEqual(get_req.html['args']['key1'], 'value1')

    def test_headers_req(self):
        headers_req = Request("http://httpbin.org/get",
                              headers=self.headers,
                              file_type='json')()
        self.assertEqual(headers_req.html['headers']['User-Agent'], self.headers['User-Agent'])


if __name__ == '__main__':
    unittest.main()
