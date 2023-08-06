# `zope.testrunner` test suite

from unittest import TestCase

from DateTime.DateTime import DateTime
from ZTUtils import make_query
from ZPublisher.HTTPRequest import HTTPRequest, record

from . import register_json_extension, unregister_extension

class Tests(TestCase):
  def test_general(self):
    rd = self._check(
      dict(i=1, b=True, f=float(1), s='abc', u=u'\u0100', d=DateTime(),
           le=[], l=[1,2,3],
           )
      )
    self.assertIsInstance(rd['f'], float)
    self.assertIsInstance(rd['u'], unicode)

  def test_dict(self):
    self._check(dict(di=dict(i=1, b=False, le=[], l=[1,2,3],),),
                transformer=lambda d: d.update(dict(di=dict(d['di'].items()))) or d,
                )

  def test_tuple(self):
    self._check(dict(te=(), t=(1,2,3)),
                dict(te=[], t=[1,2,3]),
                )

  def test_none(self):
    self._check(dict(x=None))

  def _check(self, data, result=None, transformer=None):
    if result is None: result = data
    if transformer is None: transformer = lambda x: x
    r = HTTPRequest(
      None,
      dict(REQUEST_METHOD='GET', QUERY_STRING=make_query(data),
           SERVER_NAME='localhost', SERVER_PORT='80', SCRIPT_NAME='',
           ),
      None,
      )
    r.processInputs()
    self.assertEqual(transformer(r.form), result)
    return r.form

class JsonLayer(object):
  @staticmethod
  def setUp(): register_json_extension()

  @staticmethod
  def tearDown(): unregister_extension("json")


class TestJsonExtension(Tests):
  layer = JsonLayer

  def test_nested_list(self):
    self._check(dict(x = [[1]]))

  def test_record(self):
    d = dict(x=1); r = record(); r.__dict__.update(d)
    self._check(dict(x=[[r]]), dict(x=[[d]]))


# Python 2/3 compatibility
try: unicode
except NameError: unicode=str
