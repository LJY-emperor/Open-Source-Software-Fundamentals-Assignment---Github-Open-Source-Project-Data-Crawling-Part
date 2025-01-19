import unittest
from unittest.mock import MagicMock, patch
from app import HelloWorld
from toga import MainWindow

class DummyMainWindow(MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._info_dialog_calls = []

    def info_dialog(self, title, message):
        self._info_dialog_calls.append((title, message))

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        # Mock the app config to provide a formal name and other necessary properties
        with patch('toga.platform.current_platform', 'dummy'):
            self.app = HelloWorld(
                formal_name='My First Application',
                app_id='org.example.myfirstapp'
            )
            self.dummy_main_window = DummyMainWindow(title=self.app.formal_name)
            self.app.main_window = self.dummy_main_window

    def test_say_hello_with_name(self):
        self.app.name_input = MagicMock()
        self.app.name_input.value = "Alice"
        self.app.say_hello(None)
        self.assertEqual(self.dummy_main_window._info_dialog_calls[-1], ('Hello, Alice', 'Hi there!'))

    def test_say_hello_without_name(self):
        self.app.name_input = MagicMock()
        self.app.name_input.value = ""
        self.app.say_hello(None)
        self.assertEqual(self.dummy_main_window._info_dialog_calls[-1], ('Hello, stranger', 'Hi there!'))

if __name__ == '__main__':
    unittest.main()