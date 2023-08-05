# Copyright(C) 2019 by Dr. Dieter Maurer, Illtalstr. 25, D-66571 Bubach, Germany
from Testing.ZopeTestCase import ZopeTestCase
from AccessControl import getSecurityManager

from ..proxy import proxy_roles

class Tests(ZopeTestCase):
  def test_proxy(self):
    sm = getSecurityManager()
    self.assertFalse(sm.checkPermission("Change permissions", None))
    with proxy_roles("Manager"):
      self.assertTrue(sm.checkPermission("Change permissions", None))
    self.assertFalse(sm.checkPermission("Change permissions", None))

