import tempfile
import unittest
from pathlib import Path
import config
import database
from database import init_db
from affiliate_manager import add_product, validate_https
from campaign_matcher import match_campaign

class LucrarTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        config.DB_PATH = Path(self.tmp.name) / "test.sqlite3"
        database.DB_PATH = config.DB_PATH
        init_db()

    def tearDown(self):
        self.tmp.cleanup()

    def test_https_validation(self):
        with self.assertRaises(ValueError):
            validate_https("http://example.com/item")

    def test_match_and_mismatch(self):
        add_product("Fone Bluetooth JBL Tune", "Áudio",
                    "https://loja.example/produto",
                    "https://afiliado.example/link?tag=meutag",
                    "LojaTeste", "fone bluetooth jbl headphone", "camp-1")
        self.assertTrue(match_campaign("Fone Bluetooth JBL Tune original"))
        self.assertFalse(match_campaign("Geladeira duplex inox"))

if __name__ == "__main__":
    unittest.main()
