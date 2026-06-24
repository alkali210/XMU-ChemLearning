import json
import subprocess
import sys
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "data" / "metadata.json"


class DatasetGeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(
            [sys.executable, "data/generate_dataset.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        cls.records = json.loads(METADATA.read_text(encoding="utf-8"))

    def test_generates_original_and_complex_markush_records(self):
        self.assertGreaterEqual(len(self.records), 55)
        complex_records = [record for record in self.records if record["category"] == "D"]
        self.assertGreaterEqual(len(complex_records), 30)

    def test_complex_markush_records_cover_key_variation_types(self):
        complex_records = [record for record in self.records if record["category"] == "D"]
        classes = {record.get("markush_class") for record in complex_records}

        self.assertIn("substituent_variation", classes)
        self.assertIn("position_variation", classes)
        self.assertIn("frequency_variation", classes)
        self.assertIn("homology_variation", classes)

    def test_complex_markush_files_exist_and_are_named_descriptively(self):
        for record in self.records:
            if record["category"] != "D":
                continue

            image_path = ROOT / "data" / record["filename"]
            self.assertTrue(image_path.exists(), image_path)
            self.assertIn(record["id"], image_path.name)
            self.assertTrue(record["generic_symbols"])

    def test_all_generated_images_have_white_background_and_visible_ink(self):
        for record in self.records:
            image_path = ROOT / "data" / record["filename"]
            image = Image.open(image_path).convert("RGBA")
            if hasattr(image, "get_flattened_data"):
                pixels = list(image.get_flattened_data())
            else:
                pixels = list(image.getdata())

            transparent_pixels = sum(1 for _, _, _, alpha in pixels if alpha < 255)
            white_pixels = sum(1 for red, green, blue, alpha in pixels if alpha == 255 and red > 245 and green > 245 and blue > 245)
            dark_pixels = sum(1 for red, green, blue, alpha in pixels if alpha == 255 and red < 80 and green < 80 and blue < 80)

            self.assertEqual(transparent_pixels, 0, image_path)
            self.assertGreater(white_pixels, 90000, image_path)
            self.assertGreater(dark_pixels, 100, image_path)


if __name__ == "__main__":
    unittest.main()
