import unittest

from func import plc


class TestPlcWritePayload(unittest.TestCase):
    def setUp(self):
        self.aliases = {"AWB[0].0": "pulsacion_bms"}

    def test_parse_payload_by_tag(self):
        payload = {"tag": "AWB[0].0", "value": "1"}
        self.assertEqual(plc._parse_write_payload(payload, self.aliases), ("AWB[0].0", 1))

    def test_parse_payload_by_alias(self):
        payload = {"field": "pulsacion_bms", "value": True}
        self.assertEqual(plc._parse_write_payload(payload, self.aliases), ("AWB[0].0", True))

    def test_reject_unknown_tag(self):
        payload = {"tag": "AWB[0].99", "value": 1}
        self.assertIsNone(plc._parse_write_payload(payload, self.aliases))


if __name__ == "__main__":
    unittest.main()
