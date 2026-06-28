import pytest

from atlas.core.manifest import WorkerManifest, ExecutionPolicy, CommunicationPolicy, TranslationDefinition
from atlas.core.registry import GlobalRegistry
from atlas.core.loader import WorkerInstance
from atlas.core.translation import TranslationResolver
from atlas.core.diagnostics import TranslationFailedError

def create_translator(id: str, source: str, target: str, cost: int) -> WorkerManifest:
    return WorkerManifest(
        id=id,
        name=id,
        version="1.0.0",
        language="python",
        roles=["translator"],
        execution=ExecutionPolicy("singleton"),
        communication=CommunicationPolicy([], []),
        imports=[],
        exports=[],
        translations=[TranslationDefinition(source, target, "*", cost)]
    )

def register_mock(registry: GlobalRegistry, manifest: WorkerManifest):
    instance = WorkerInstance(id=manifest.id, manifest=manifest, _executable_handle=None)
    registry.register_worker(instance)

def test_direct_translation():
    registry = GlobalRegistry()
    register_mock(registry, create_translator("t.py2json", "python", "json", 1))
    
    resolver = TranslationResolver(registry)
    chain = resolver.resolve_translation("python", "json").unwrap()
    
    assert chain.total_cost == 1
    assert len(chain.translators) == 1
    assert chain.translators[0] == "t.py2json"

def test_shortest_path_chaining():
    registry = GlobalRegistry()
    # Route 1: A -> B -> D (Cost 20)
    register_mock(registry, create_translator("t.ab", "A", "B", 10))
    register_mock(registry, create_translator("t.bd", "B", "D", 10))
    
    # Route 2: A -> C -> D (Cost 15) <- Should pick this
    register_mock(registry, create_translator("t.ac", "A", "C", 5))
    register_mock(registry, create_translator("t.cd", "C", "D", 10))
    
    # Route 3: A -> D direct but very expensive (Cost 50)
    register_mock(registry, create_translator("t.ad", "A", "D", 50))
    
    resolver = TranslationResolver(registry)
    chain = resolver.resolve_translation("A", "D").unwrap()
    
    assert chain.total_cost == 15
    assert len(chain.translators) == 2
    assert chain.translators == ["t.ac", "t.cd"]

def test_no_path():
    registry = GlobalRegistry()
    register_mock(registry, create_translator("t.ab", "A", "B", 10))
    
    resolver = TranslationResolver(registry)
    res = resolver.resolve_translation("A", "C")
    
    assert res.is_err()
    assert isinstance(res.error, TranslationFailedError)

def test_cache_invalidation():
    registry = GlobalRegistry()
    register_mock(registry, create_translator("t.ab", "A", "B", 10))
    
    resolver = TranslationResolver(registry)
    
    # Resolves to cost 10
    chain1 = resolver.resolve_translation("A", "B").unwrap()
    assert chain1.total_cost == 10
    
    # Now we register a much cheaper direct translator
    register_mock(registry, create_translator("t.ab_cheap", "A", "B", 1))
    
    # Because the registry generation incremented, cache should clear
    chain2 = resolver.resolve_translation("A", "B").unwrap()
    assert chain2.total_cost == 1
    assert chain2.translators == ["t.ab_cheap"]
