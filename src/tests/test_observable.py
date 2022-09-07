import unittest
from mock import patch
from typing import Any

from observable import observable
from layers.model import types as model_types


class MockView(observable.Observable):
    def invoke_hello(self) -> None:
        self._emit(model_types.EventNames.STATE_UPDATED.value)


def test() -> None:
    print('Hello')


mock_view = MockView()
mock_view.on(model_types.EventNames.STATE_UPDATED.value, test)


class TestObservable(unittest.TestCase):
    @patch('builtins.print')
    def test_on(self, mock_print: Any):
        mock_view.invoke_hello()
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()
