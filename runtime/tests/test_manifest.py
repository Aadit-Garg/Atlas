import os
from atlas.core.manifest import ManifestLoader
from atlas.core.diagnostics import ParseError, ValidationError

def test_valid_manifest():
    loader = ManifestLoader()
    path = os.path.join(os.path.dirname(__file__), "dummy_workers", "valid", "atlas.yaml")
    
    res = loader.load_file(path)
    assert res.is_ok()
    manifest = res.unwrap()
    
    assert manifest.id == "atlas.test.dummy"
    assert manifest.language == "python"
    assert "test" in manifest.roles
    assert manifest.execution.policy == "pool"
    assert len(manifest.imports) == 1
    assert manifest.imports[0].capability_name == "capability.logger"
    assert len(manifest.exports) == 1

def test_invalid_manifest():
    loader = ManifestLoader()
    path = os.path.join(os.path.dirname(__file__), "dummy_workers", "invalid_schema", "atlas.yaml")
    
    res = loader.load_file(path)
    assert res.is_err()
    assert isinstance(res.error, ValidationError)

def test_missing_file():
    loader = ManifestLoader()
    res = loader.load_file("/this/path/does/not/exist.yaml")
    assert res.is_err()
    assert isinstance(res.error, ParseError)
