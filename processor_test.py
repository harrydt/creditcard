import unittest
from processor import Processor
from unittest.mock import MagicMock


class ProcessorTest(unittest.TestCase):
    def setUp(self):
        self.processor = Processor({})

    def test_process_with_a_valid_add_command(self):
        commands = [
            ["Add", "Tom", "4111111111111111", "$1000"]
        ]
        self.processor._add = MagicMock()
        self.processor.process(commands)
        self.processor._add.assert_called_once_with(
            name="Tom",
            card_number="4111111111111111",
            limit="$1000")

    def test_process_with_a_valid_charge_command(self):
        commands = [
            ["Charge", "Tom", "$1000"]
        ]
        self.processor._charge = MagicMock()
        self.processor.process(commands)
        self.processor._charge.assert_called_once_with(
            name="Tom",
            amount="$1000")

    def test_process_with_a_valid_credit_command(self):
        commands = [
            ["Credit", "Tom", "$1000"]
        ]
        self.processor._credit = MagicMock()
        self.processor.process(commands)
        self.processor._credit.assert_called_once_with(
            name="Tom",
            amount="$1000")

    def test_add_with_invalid_card_number(self):
        commands = [
            ["Add", "Tom", "1231231321", "$1000"]
        ]
        self.processor.process(commands)
        self.assertEqual(
            {"Tom": "error"},
            self.processor.summary
        )

    def test_add_with_existing_card_number(self):
        '''
        This test will fail because I have yet to decide if the summary
        should print error or the current balance
        '''
        self.processor = Processor({
            "Tom": [{
                "card_number": "4111111111111111",
                "balance": 0,
                "limit": 1000
            }]
        })

        commands = [
            ["Add", "Tom", "1231231321", "$1000"]
        ]
        self.processor.process(commands)
        self.assertEqual(
            {"Tom": "error"},
            self.processor.summary
        )

    def test_add_new_card_for_existing_user(self):
        self.processor = Processor({
            "Tom": [{
                "card_number": "4111111111111111",
                "balance": 0,
                "limit": 1000
            }]
        })

        commands = [
            ["Add", "Tom", "5454545454545454", "$1000"]
        ]
        report = self.processor.process(commands)
        self.assertEqual("Tom: $0\n", report)

    def test_add_new_card_for_new_user(self):
        self.processor = Processor({
            "Tom": [{
                "card_number": "4111111111111111",
                "balance": 0,
                "limit": 1000
            }]
        })

        commands = [
            ["Add", "Lisa", "5454545454545454", "$1000"]
        ]
        report = self.processor.process(commands)
        self.assertEqual(
            "Lisa: $0\nTom: $0\n", report)

    def test_charge_for_non_existing_user(self):
        commands = [
            ["Charge", "Ron", "$2"]
        ]
        self.processor.process(commands)
        self.assertEqual({}, self.processor.summary)


if __name__ == '__main__':
    unittest.main()
