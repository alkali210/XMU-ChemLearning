from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ROOT / "docker-compose.yml"
CLIENT = ROOT / "webui" / "src" / "api" / "client.js"
APP = ROOT / "webui" / "src" / "App.jsx"
MODEL_CARD = ROOT / "webui" / "src" / "components" / "ModelCard.jsx"
MOLSCRIBE = ROOT / "services" / "molscribe-api" / "main.py"
DECIMER = ROOT / "services" / "decimer-api" / "main.py"
README = ROOT / "README.md"
README_ZH = ROOT / "README-zh.md"


class DefaultTwoModelStackTests(unittest.TestCase):
    def test_compose_defaults_to_molscribe_decimer_and_webui_only(self):
        compose = COMPOSE.read_text(encoding="utf-8")
        self.assertIn("molscribe-api:", compose)
        self.assertIn("decimer-api:", compose)
        self.assertIn("webui:", compose)
        self.assertNotIn("markushgrapher-api:", compose)
        self.assertNotIn("localhost:8003", compose)

    def test_webui_calls_only_default_two_models(self):
        client = CLIENT.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertIn("molscribe", client)
        self.assertIn("decimer", client)
        self.assertNotIn("markushgrapher", client)
        self.assertNotIn("http://localhost:8003", client)
        self.assertIn("MolScribe", app)
        self.assertIn("DECIMER", app)
        self.assertNotIn("MarkushGrapher-2", app)

    def test_services_return_simple_runtime_telemetry(self):
        for path in (MOLSCRIBE, DECIMER):
            source = path.read_text(encoding="utf-8")
            self.assertIn("duration_ms", source)
            self.assertIn("runtime", source)
            self.assertIn("socket.gethostname()", source)
            self.assertIn("platform.platform()", source)
            self.assertIn("time.perf_counter()", source)

    def test_model_card_renders_runtime_telemetry(self):
        source = MODEL_CARD.read_text(encoding="utf-8")
        self.assertIn("duration_ms", source)
        self.assertIn("runtime", source)
        self.assertIn("Host:", source)
        self.assertIn("Platform:", source)
        self.assertIn("Time:", source)

    def test_docs_describe_chinese_and_english_two_model_default(self):
        readme = README.read_text(encoding="utf-8")
        readme_zh = README_ZH.read_text(encoding="utf-8")
        self.assertIn("MolScribe", readme)
        self.assertIn("DECIMER", readme)
        self.assertIn("MarkushGrapher-2", readme)
        self.assertIn("experimental optional", readme)
        self.assertIn("默认", readme_zh)
        self.assertIn("MolScribe", readme_zh)
        self.assertIn("DECIMER", readme_zh)
        self.assertIn("MarkushGrapher-2", readme_zh)
        self.assertIn("实验性可选", readme_zh)


if __name__ == "__main__":
    unittest.main()
