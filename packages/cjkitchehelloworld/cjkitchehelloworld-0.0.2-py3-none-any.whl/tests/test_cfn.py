from unittest import TestCase
from unittest.mock import MagicMock, patch
from logging import getLogger, DEBUG

from cfn import say_hello

logger = getLogger(__name__)
logger.setLevel(DEBUG)

class TestCfn(TestCase):

  def setUp(self):
    logger.debug('Inside setup')
  
  def test_say_hello_returns_hello_world(self):
    expected = 'Hello World'
    received = say_hello()
    self.assertEqual(expected, received, f"Expected {expected} Received {received}")