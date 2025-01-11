import sys
import unittest

from PyQt5.QtWidgets import QApplication

from main import MonitorApp


class TestMonitorApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.app = QApplication(sys.argv)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.app.quit()

    def setUp(self):
        self.window = MonitorApp()

    def test_init(self):
        """
        Проверить, что в начальном состоянии приложения запись данных не активна.
        """
        self.assertFalse(self.window.is_recording)

    def test_start_recording(self):
        """
        Тесты для метода start_recording
        """
        self.window.start_recording()
        self.assertTrue(self.window.is_recording)
        self.assertTrue(self.window.timer.isActive())

    def test_stop_recording(self):
        """
        Тесты для метода stop_recording
        Проверка остановки таймера
        Проверка изменения состояния записи
        Проверка доступности кнопок
        """
        self.window.start_recording()
        self.window.stop_recording()
        self.assertFalse(self.window.is_recording)
        self.assertTrue(self.window.start_button.isEnabled())
        self.assertFalse(self.window.stop_button.isEnabled())
        self.assertEqual(self.window.timer.isActive(), False)


if __name__ == '__main__':
    unittest.main()
