import unittest
from datetime import datetime

from app import app
from helpers import check_data_from_str, random_analyzes_result, random_analyzes_description, random_receipt_description


class AnalyzesTest(unittest.TestCase):

    def test_check_data_from_str(self):
        data = "abc"
        self.assertEqual(check_data_from_str(data), data)

        data = "2021-01-29"
        expected_result = datetime(2021, 1, 29)
        self.assertEqual(check_data_from_str(data, "date"), expected_result)

        data = "111-222-111 22"
        expected_result = "11122211122"
        self.assertEqual(check_data_from_str(data, "snils"), expected_result)

        data = "111-aaa-111 22"
        expected_result = False
        self.assertEqual(check_data_from_str(data, "snils"), expected_result)

        data = "1234 1234 1234 1234"
        expected_result = "1234123412341234"
        self.assertEqual(check_data_from_str(data, "polis"), expected_result)

        data = "1234 1234 aaaa 1234"
        expected_result = False
        self.assertEqual(check_data_from_str(data, "polis"), expected_result)

        data = "(927)-000-11-22"
        expected_result = "9270001122"
        self.assertEqual(check_data_from_str(data, "phone"), expected_result)

        data = "(927)-aaa-11-22"
        expected_result = False
        self.assertEqual(check_data_from_str(data, "phone"), expected_result)

        data = ""
        expected_result = False
        self.assertEqual(check_data_from_str(data), expected_result)

        data = "123abc"
        expected_result = "123abc"
        self.assertEqual(check_data_from_str(data), expected_result)

    def test_analyzes_res(self):
        analyzes_list = ["POSITIVE", "NEGATIVE"]
        self.assertTrue(random_analyzes_result() in analyzes_list)

    def test_analyzes_desc(self):
        analyzes_list = ["анализ 0", "анализ 1", "анализ 2", "анализ 3"]
        self.assertTrue(random_analyzes_description() in analyzes_list)

    def test_receipt_desc(self):
        analyzes_list = ["рецепт 0", "рецепт 1", "рецепт 2", "рецепт 3"]
        self.assertTrue(random_receipt_description() in analyzes_list)

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
