from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "services" / "markushgrapher-api" / "main.py"
DOCKERFILE = ROOT / "services" / "markushgrapher-api" / "Dockerfile"
COMPOSE = ROOT / "docker-compose.yml"
CLIENT = ROOT / "webui" / "src" / "api" / "client.js"
APP = ROOT / "webui" / "src" / "App.jsx"


class MarkushGrapherApiSourceTests(unittest.TestCase):
    def test_service_uses_markushgrapher_identity_and_contract(self):
        source = MAIN.read_text(encoding="utf-8")
        self.assertIn('MODEL_NAME = "MarkushGrapher-2"', source)
        self.assertIn('@app.get("/health")', source)
        self.assertIn('@app.post("/predict")', source)
        self.assertIn('"smiles"', source)
        self.assertIn('"confidence"', source)
        self.assertIn('"error"', source)

    def test_service_runs_official_inference_pipeline_best_effort(self):
        source = MAIN.read_text(encoding="utf-8")
        self.assertIn("scripts/inference/inference.sh", source)
        self.assertIn("subprocess.run", source)
        self.assertIn("predictions", source)
        self.assertIn("MarkushGrapher-2 is not available", source)

    def test_health_check_does_not_download_large_assets(self):
        source = MAIN.read_text(encoding="utf-8")
        health_body = source.split('@app.get("/health")', 1)[1].split('@app.post("/predict")', 1)[0]
        self.assertNotIn("ensure_runtime_assets()", health_body)

    def test_availability_checks_required_model_files_not_only_directories(self):
        source = MAIN.read_text(encoding="utf-8")
        self.assertIn("MODEL_REQUIRED_FILES", source)
        self.assertIn("OCR_REQUIRED_FILES", source)
        self.assertIn("WEIGHT_FILES", source)
        self.assertIn("config.json", source)
        self.assertIn("preprocessor_config.json", source)
        self.assertIn("model.safetensors", source)

    def test_predict_does_not_retry_partial_model_downloads(self):
        source = MAIN.read_text(encoding="utf-8")
        self.assertIn("should_download_directory", source)
        self.assertIn("directory_has_files", source)

    def test_missing_weight_placeholder_groups_string_before_path_join(self):
        source = MAIN.read_text(encoding="utf-8")
        self.assertIn('directory / ("{" + ",".join(WEIGHT_FILES) + "}")', source)

    def test_dockerfile_references_official_repo_and_weights(self):
        dockerfile = DOCKERFILE.read_text(encoding="utf-8")
        source = MAIN.read_text(encoding="utf-8")
        self.assertIn("DS4SD/MarkushGrapher", dockerfile)
        self.assertIn("docling-project/MarkushGrapher-2", source)
        self.assertIn("docling-project/ChemicalOCR", source)
        self.assertIn("swin_base_char_aux_1m680k.pth", source)
        self.assertIn("hf", source)
        self.assertIn("uvicorn", dockerfile)

    def test_dockerfile_installs_rdkit_rendering_libraries(self):
        dockerfile = DOCKERFILE.read_text(encoding="utf-8")
        self.assertIn("libxrender1", dockerfile)
        self.assertIn("libxext6", dockerfile)

    def test_default_compose_and_webui_do_not_load_markushgrapher(self):
        compose = COMPOSE.read_text(encoding="utf-8")
        client = CLIENT.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertNotIn("markushgrapher-api", compose)
        self.assertNotIn("8003:8003", compose)
        self.assertNotIn("markushgrapher-molscribe-cache", compose)
        self.assertNotIn("markushgrapher", client)
        self.assertNotIn("http://localhost:8003", client)
        self.assertNotIn("MarkushGrapher-2", app)
        self.assertNotIn("img2mol", client)


if __name__ == "__main__":
    unittest.main()
