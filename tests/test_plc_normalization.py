import unittest

from func import plc


class TestPlcNormalization(unittest.TestCase):
    def test_normalize_bytes(self):
        self.assertEqual(plc._normalize_field_value(b"\x01\x00"), 1)
        self.assertEqual(plc._normalize_field_value(bytearray([2, 0])), 2)

    def test_normalize_binary_sequence(self):
        self.assertEqual(plc._normalize_field_value([True, False, True]), 0b101)
        self.assertEqual(plc._normalize_field_value([1, 0, 1, 1]), 0b1101)

    def test_non_binary_sequence_stringified(self):
        self.assertEqual(plc._normalize_field_value([2, 0, 3]), "[2, 0, 3]")


if __name__ == "__main__":
    unittest.main()
