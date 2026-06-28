"""
atlas new — Scaffold a new Atlas project.
"""

import os
import textwrap


# ---------------------------------------------------------
# Templates (embedded for zero-dependency operation)
# ---------------------------------------------------------

WORKER_MANIFEST = textwrap.dedent("""\
    id: {namespace}.{name}
    name: {class_name}
    version: 1.0.0
    language: python
    roles: [worker]

    execution:
      policy: singleton

    communication:
      transports: [memory]
      formats: [python]
      default_format: python

    imports: []

    exports:
      - capability: {namespace}.{name}
        version: 1.0.0

    translations: []
""")

WORKER_PY = textwrap.dedent('''\
    """
    {class_name} — An Atlas Worker
    """
    from atlas_sdk import WorkerBase, capability, on_invocation


    class {class_name}(WorkerBase):
        _worker_id = "{namespace}.{name}"
        _worker_name = "{class_name}"
        _worker_version = "1.0.0"
        _worker_roles = ["worker"]

        def on_init(self):
            """Called after construction. Set up your state here."""
            pass

        def on_start(self):
            """Called when the runtime starts this worker."""
            pass

        def on_stop(self):
            """Called on shutdown. Clean up resources here."""
            pass

        @capability("{namespace}.{name}.hello", version="1.0.0")
        @on_invocation("hello")
        def hello(self, name: str = "World") -> str:
            """A simple hello capability. Replace me with real logic!"""
            return f"Hello, {{name}}! From {class_name}."
''')

WORKER_TEST = textwrap.dedent('''\
    """Tests for {class_name}."""
    from atlas_sdk.testing import MockRuntime, assert_capability_exported
    from {module_path} import {class_name}


    def test_{name}_exports_capability():
        worker = {class_name}()
        assert_capability_exported(worker, "{namespace}.{name}.hello")


    def test_{name}_hello():
        runtime = MockRuntime()
        runtime.register({class_name}, "{namespace}.{name}")
        result = runtime.invoke("{namespace}.{name}", "hello", {{"name": "Atlas"}})
        assert "Hello" in result
''')

WORKER_README = textwrap.dedent("""\
    # {class_name}

    An Atlas Worker.

    ## Capabilities

    - `{namespace}.{name}.hello` — Greets you by name.

    ## Usage

    ```python
    from {module_path} import {class_name}

    worker = {class_name}()
    print(worker.hello("Atlas"))
    ```

    ## Testing

    ```bash
    atlas test
    ```
""")

MODEL_PY = textwrap.dedent('''\
    """
    {class_name} — An Atlas Model
    """
    from abc import abstractmethod
    from atlas_sdk import ModelBase, model_version


    @model_version("1.0.0")
    class {class_name}(ModelBase):
        """
        Define the abstract contract for {name}.
        Workers that implement this model must provide all methods below.
        """

        @abstractmethod
        def process(self, data: str) -> str:
            """Process the input data. Replace with your real contract."""
            ...
''')

MODEL_TEST = textwrap.dedent('''\
    """Compliance tests for {class_name}."""
    from atlas_sdk.testing import assert_model_compliant
    from {module_path} import {class_name}


    class Dummy{class_name}Impl({class_name}):
        """A dummy implementation for compliance testing."""
        def process(self, data: str) -> str:
            return data.upper()


    def test_dummy_is_compliant():
        assert_model_compliant({class_name}, Dummy{class_name}Impl)


    def test_contract_introspection():
        contract = {class_name}.get_contract()
        method_names = [m["method"] for m in contract]
        assert "process" in method_names
''')

ADAPTER_MANIFEST = textwrap.dedent("""\
    id: {namespace}.adapter.{name}
    name: {class_name}
    version: 1.0.0
    language: python
    roles: [translator]

    execution:
      policy: singleton

    communication:
      transports: [memory]
      formats: [python]
      default_format: python

    imports: []
    exports: []

    translations:
      - source_format: source
        target_format: target
        cost: 1
""")

ADAPTER_PY = textwrap.dedent('''\
    """
    {class_name} — An Atlas Adapter
    """
    from atlas_sdk import AdapterBase, translation


    class {class_name}(AdapterBase):
        _adapter_id = "{namespace}.adapter.{name}"
        _adapter_name = "{class_name}"
        _adapter_version = "1.0.0"

        @translation(source="source_format", target="target_format", cost=1)
        def convert(self, data: bytes) -> bytes:
            """Convert data from source to target format. Replace me!"""
            return data
''')

ADAPTER_TEST = textwrap.dedent('''\
    """Tests for {class_name}."""
    from {module_path} import {class_name}


    def test_{name}_translates():
        adapter = {class_name}()
        result = adapter.convert(b"hello")
        assert result == b"hello"


    def test_{name}_has_translations():
        adapter = {class_name}()
        translations = adapter.get_translations()
        assert len(translations) >= 1
''')

PRODUCT_YAML = textwrap.dedent("""\
    product:
      name: {name}
      version: 1.0.0
      description: An Atlas Product

    workers:
      - id: atlas.core.logger
      - id: atlas.core.config
      - id: atlas.core.storage

    config:
      LOG_LEVEL: INFO
""")

PRODUCT_MAIN = textwrap.dedent('''\
    """
    {class_name} — An Atlas Product
    """
    from atlas_sdk import ProductBuilder


    def build():
        product = (
            ProductBuilder("{name}", version="1.0.0", description="An Atlas Product")
            .add_worker("atlas.core.logger")
            .add_worker("atlas.core.config")
            .add_worker("atlas.core.storage")
            .configure("LOG_LEVEL", "INFO")
            .build()
        )
        product.write("product.yaml")
        print(f"Product '{{product.name}}' built successfully!")
        return product


    if __name__ == "__main__":
        build()
''')

PRODUCT_README = textwrap.dedent("""\
    # {class_name}

    An Atlas Product.

    ## Workers

    - `atlas.core.logger`
    - `atlas.core.config`
    - `atlas.core.storage`

    ## Running

    ```bash
    atlas run
    ```
""")


# ---------------------------------------------------------
# Handler
# ---------------------------------------------------------

def handle_new(args):
    name = args.name
    project_type = args.type
    namespace = "atlas"
    class_name = "".join(word.capitalize() for word in name.replace("-", "_").split("_"))
    if not class_name.endswith(project_type.capitalize()):
        class_name += project_type.capitalize()

    project_dir = name
    os.makedirs(project_dir, exist_ok=True)

    ctx = {
        "name": name,
        "class_name": class_name,
        "namespace": namespace,
        "module_path": f"{name}.worker" if project_type == "worker" else f"{name}.model" if project_type == "model" else f"{name}.adapter",
    }

    if project_type == "worker":
        _write(project_dir, "manifest.yaml", WORKER_MANIFEST.format(**ctx))
        _write(project_dir, "worker.py", WORKER_PY.format(**ctx))
        _write(project_dir, f"test_{name}.py", WORKER_TEST.format(**ctx))
        _write(project_dir, "README.md", WORKER_README.format(**ctx))

    elif project_type == "model":
        _write(project_dir, "model.py", MODEL_PY.format(**ctx))
        _write(project_dir, f"test_{name}.py", MODEL_TEST.format(**ctx))

    elif project_type == "adapter":
        _write(project_dir, "manifest.yaml", ADAPTER_MANIFEST.format(**ctx))
        _write(project_dir, "adapter.py", ADAPTER_PY.format(**ctx))
        _write(project_dir, f"test_{name}.py", ADAPTER_TEST.format(**ctx))

    elif project_type == "product":
        _write(project_dir, "product.yaml", PRODUCT_YAML.format(**ctx))
        _write(project_dir, "main.py", PRODUCT_MAIN.format(**ctx))
        _write(project_dir, "README.md", PRODUCT_README.format(**ctx))

    print(f"✨ Created {project_type} '{name}' in ./{project_dir}/")
    print(f"   cd {project_dir}")
    if project_type in ("worker", "adapter"):
        print(f"   atlas test")
    elif project_type == "product":
        print(f"   atlas run")


def _write(directory: str, filename: str, content: str):
    path = os.path.join(directory, filename)
    with open(path, "w") as f:
        f.write(content)
