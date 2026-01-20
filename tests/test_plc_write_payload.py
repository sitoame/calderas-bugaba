import unittest

from func import plc


class TestPlcWritePayload(unittest.TestCase):
    def setUp(self):
        self.aliases = {
            "AWB[0].0": "pulsacion_bms",
            "AWR[0]": "op_rem_caldera_sp",
        }

    def test_parse_payload_by_tag(self):
        payload = {"tag": "AWB[0].0", "value": "1"}
        self.assertEqual(plc._parse_write_payload(payload, self.aliases), ("AWB[0].0", True))

    def test_parse_payload_by_alias(self):
        payload = {"field": "pulsacion_bms", "value": True}
        self.assertEqual(plc._parse_write_payload(payload, self.aliases), ("AWB[0].0", True))

    def test_parse_payload_awr(self):
        payload = {"tag": "AWR[0]", "value": "12.5"}
        self.assertEqual(plc._parse_write_payload(payload, self.aliases), ("AWR[0]", 12.5))

    def test_reject_unknown_tag(self):
        payload = {"tag": "AWB[0].99", "value": 1}
        self.assertIsNone(plc._parse_write_payload(payload, self.aliases))


if __name__ == "__main__":
    unittest.main()
