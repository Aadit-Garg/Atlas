"""
Atlas Translation Layer Demonstration
Demonstrates the Translation Resolver computing the shortest valid translation path.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from atlas.core.manifest import WorkerManifest, ExecutionPolicy, CommunicationPolicy, TranslationDefinition
from atlas.core.registry import GlobalRegistry
from atlas.core.loader import WorkerInstance
from atlas.core.translation import TranslationResolver

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

def run_demo():
    print("Initializing Atlas Translation Resolver...")
    registry = GlobalRegistry()
    resolver = TranslationResolver(registry)
    
    # We want to translate: Python -> C++
    print("\n[Scenario] We need to translate 'python' to 'cpp'")
    
    print("\n[Registry] Installing Translators:")
    translators = [
        create_translator("trans.py_to_json", "python", "json", cost=1),
        create_translator("trans.json_to_rust", "json", "rust", cost=1),
        create_translator("trans.rust_to_cpp", "rust", "cpp", cost=1),
        create_translator("trans.json_to_cpp", "json", "cpp", cost=5), # Expensive direct route
    ]
    
    for t in translators:
        print(f"  - Installed {t.id} (Cost {t.translations[0].cost})")
        registry.register_worker(WorkerInstance(id=t.id, manifest=t, _executable_handle=None))
        
    print("\n[Resolver] Computing optimal Translation Chain...")
    res = resolver.resolve_translation("python", "cpp")
    
    if res.is_ok():
        chain = res.unwrap()
        print(f"\nSuccess! Total Cost: {chain.total_cost}")
        print("Required Translators:")
        for w_id in chain.translators:
            print(f"  -> {w_id}")
            
        print("\nNote how Atlas ignored the expensive 'trans.json_to_cpp' and instead built a cheaper 3-step chain!")
    else:
        print(f"Failed: {res.error}")

if __name__ == "__main__":
    run_demo()
