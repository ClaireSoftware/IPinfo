import ipinfo
import rich
import unittest


class TestIP(unittest.TestCase):
    def runTest(self):
        output = ipinfo.trysites()
        rich.print(f"{output=} {output.keys()}")
        ip = output.get("ip")
        self.assertTrue(ip, "IP not present")
        self.assertEqual(ip.replace('.', '').isalnum(),
                         True, "invalid chars in IP")

        octets = ip.split(".")
        print(f"{ip=}, {octets=}")
        self.assertEqual(len(octets), 4, "wrong number of octets in IP")
        for octet in octets:
            self.assertGreater(int(octet), -1, f"octet {octet} smaller than 0")
            self.assertLess(int(octet), 256, f"octet {octet} greater than 255")


unittest.main()
