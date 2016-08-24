import random
import re
import unittest

from nose.tools import assert_equal, assert_in, assert_greater_equal

from FlaskTask import app
from FlaskTask import views

import time

ROBOT_TAGS = ['nofollow', 'none', 'noindex']

LINK_ISSUES = ['bad_uri', 'base', 'body_canonical', 'canonical', 'data_uri', 'long_label', 'malformed_hrefs', 'multiple',
               'nofollow', 'relative_base', 'schemes', 'default_ports', 'internal', 'href_encoding']

ENCODING_TYPES = ['gzip', 'zlib', 'deflate']

REDIRECTS = ['missing_location', 'relative']

HEAD_ISSUES = ['bad_entities', 'closing_html', 'description_in_body', 'multiple_descriptions']


class TestFlaskFlaskTask(object):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    @staticmethod
    def _status_ok(result):
        assert_equal(200, result.status_code)

    @staticmethod
    def _status_not_found(result):
        assert_equal(404, result.status_code)

    def test_home_page(self):
        result = self.app.get('/')
        self._status_ok(result)
        assert_in('<table class="table table-hover" id="robots">', result.data)

    def test_status_code_page(self):
        for code in views.EXAMPLE_STATUS_CODES:
            result = self.app.get('/status_codes/' + str(code))
            assert_equal(result.status_code, code)

    def test_charset_encoding(self):
        for charset in views.CHARSETS:
            result = self.app.get('/encoding/' + str(charset))
            self._status_ok(result)
            # assert_in(('text/html; charset=' + str(charset)), result.headers)
            assert_in(('<meta charset=' + str(charset)), result.data)

    def test_meta_robots(self):
        for tag in ROBOT_TAGS:
            result = self.app.get('/robots/' + str(tag))
            self._status_ok(result)
            assert_in(("<meta name='robots' content=" + str(tag)), result.data)

    def test_meta_robots_multiple(self):
        result = self.app.get('/robots/multiple')
        self._status_ok(result)
        metas = str(result.data).count("<meta name='robots' content=")
        assert_equal(3, metas)

    def test_meta_robots_caps(self):
        result = self.app.get('/robots/capitalization')
        self._status_ok(result)
        assert_in('<META NAME="ROBOTS" CONTENT="NOINDEX,NOFOLLOW"', result.data)

    def test_refresh(self):
        result = self.app.get('/headers/refresh')
        self._status_ok(result)
        assert_in('Refresh', str(result.data))

    def test_links(self):
        for issue in LINK_ISSUES:
            result = self.app.get('/links/' + str(issue))
            self._status_ok(result)

    def test_xrobots(self):
        for tag in ROBOT_TAGS:
            result = self.app.get('/xrobots/' + str(tag))
            self._status_ok(result)
            assert_in(tag, str(result.headers))

    def test_timeouts(self):
        issue = 'Content-Length: 1000'
        result = self.app.get('/headers/timeout_truncated')
        assert_in(issue, str(result.headers))

    def test_encoding_compression(self):
        for compression in ENCODING_TYPES:
            result = self.app.get('/encoding_type/' + str(compression))
            self._status_ok(result)
            assert_in(compression, str(result.headers))

    def test_redirects(self):
        for issue in REDIRECTS:
            result = self.app.get('/redirects/' + str(issue))
            assert_equal(result.status_code, 301)

    def test_empty(self):
        result = self.app.get('/empty')
        self._status_ok(result)
        assert_equal(0, len(result.data))

    def test_head(self):
        for issue in HEAD_ISSUES:
            result = self.app.get('/head/' + str(issue))
            self._status_ok(result)

    def test_delay(self):
        start = time.time()
        result = self.app.get('/delay/1')
        duration = time.time() - start
        self._status_ok(result)
        assert_greater_equal(duration, 1)

    def _check_ok(self, path):
        result = self.app.get(path)
        self._status_ok(result)

    def _check_not_found(self, path):
        result = self.app.get(path)
        self._status_not_found(result)

    def test_infinite(self):
        for path in ['/site/infinite',
                     '/site/infinite/0',
                     '/site/infinite/{}'.format(2**128),
                     ]:
            yield self._check_ok, path

        for path in ['/site/infinite/-1',
                     '/site/infinite/not_an_integer',
                    ]:
            yield self._check_not_found, path

    def test_infinite_degree(self):
        for path in ['/site/infinite_degree',
                     '/site/infinite_degree/0',
                     '/site/infinite_degree/1/0',
                     '/site/infinite_degree/1000/0',
                     '/site/infinite_degree/5000/{}'.format(2**128),
                    ]:
            yield self._check_ok, path

        for path in ['/site/infinite_degree/-1',
                     '/site/infinite_degree/-1/0',
                     '/site/infinite_degree/0/1',
                     '/site/infinite_degree/-1/1',
                    ]:
            yield self._check_not_found, path

    def test_infinite_degree_right_degree(self):
        # Check for the right number of links
        degree = random.randint(1, 20)
        result = self.app.get('/site/infinite_degree/{}/0'.format(degree))
        assert_equal(degree,
                     len(re.findall('<li><a', result.data)))
