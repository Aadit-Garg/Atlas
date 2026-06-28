import heapq
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

from .diagnostics import Result, TranslationFailedError, TranslationCycleError
from .registry import GlobalRegistry
from .resolver import match_version

@dataclass(frozen=True)
class TranslationEdge:
    worker_id: str
    source_format: str
    target_format: str
    cost: int
    version_compat: str

@dataclass(frozen=True)
class TranslationChain:
    source_format: str
    target_format: str
    total_cost: int
    translators: List[str]  # Ordered list of worker_ids

class TranslationResolver:
    """
    Computes the shortest compatible translation path using Dijkstra's algorithm.
    Atlas does NOT perform translations, it simply orchestrates them here.
    """
    def __init__(self, registry: GlobalRegistry):
        self._registry = registry
        
        # Cache of chains
        # Key: (source_format, target_format)
        self._cache: Dict[Tuple[str, str], TranslationChain] = {}
        self._last_generation: int = -1
        
    def resolve_translation(self, source_format: str, target_format: str) -> Result[TranslationChain, Exception]:
        """
        Finds the shortest compatible translation chain.
        """
        # Check cache invalidation
        current_gen = self._registry.translation_generation
        if self._last_generation != current_gen:
            self._cache.clear()
            self._last_generation = current_gen
            
        cache_key = (source_format, target_format)
        if cache_key in self._cache:
            return Result.ok(self._cache[cache_key])
            
        # If formats are exactly the same, no translation is needed
        if source_format == target_format:
            chain = TranslationChain(source_format, target_format, 0, [])
            self._cache[cache_key] = chain
            return Result.ok(chain)

        res = self._find_chain(source_format, target_format)
        if res.is_err():
            return res
            
        chain = res.unwrap()
        self._cache[cache_key] = chain
        return Result.ok(chain)

    def _find_chain(self, start_format: str, end_format: str) -> Result[TranslationChain, Exception]:
        """
        Dijkstra's Shortest Path Algorithm over the Translation Graph.
        """
        # State: (cumulative_cost, current_format, path_of_worker_ids)
        # Priority Queue automatically sorts by cumulative_cost
        queue: List[Tuple[int, str, List[str]]] = [(0, start_format, [])]
        
        # Track the cheapest cost to reach each format to prevent cycles and redundant paths
        visited_costs: Dict[str, int] = {start_format: 0}
        
        while queue:
            cost, current_format, path = heapq.heappop(queue)
            
            # Goal check
            if current_format == end_format:
                return Result.ok(TranslationChain(
                    source_format=start_format,
                    target_format=end_format,
                    total_cost=cost,
                    translators=path
                ))
                
            # If we found a cheaper way to this node earlier, skip
            if cost > visited_costs.get(current_format, float('inf')):
                continue
                
            # Find all workers that translate FROM this format
            # Using the registry's O(1) translation index
            self._registry._lock.acquire_read()
            try:
                candidate_worker_ids = self._registry._translation_index.get(current_format, [])
                
                for w_id in candidate_worker_ids:
                    # In a highly volatile system this worker might have vanished, grab it safely
                    worker_opt = self._registry.get_worker(w_id)
                    if not worker_opt: continue
                    
                    for trans in worker_opt.manifest.translations:
                        if trans.source_format == current_format:
                            next_format = trans.target_format
                            next_cost = cost + trans.cost
                            
                            # If this path is cheaper than any previously found path to `next_format`
                            if next_cost < visited_costs.get(next_format, float('inf')):
                                visited_costs[next_format] = next_cost
                                
                                new_path = list(path)
                                new_path.append(w_id)
                                
                                heapq.heappush(queue, (next_cost, next_format, new_path))
            finally:
                self._registry._lock.release_read()
                
        # If the queue empties without reaching end_format, resolution failed.
        return Result.err(TranslationFailedError(
            f"No valid translation path found from '{start_format}' to '{end_format}'."
        ))

    def explain(self, chain: TranslationChain) -> str:
        """Returns a human-readable explanation of the calculated translation chain."""
        if not chain.translators:
            return f"No translation required between {chain.source_format} and {chain.target_format}."
            
        lines = [f"Translation Chain: {chain.source_format} -> {chain.target_format}"]
        lines.append(f"Total Cost: {chain.total_cost}")
        lines.append("Path:")
        
        for idx, t_id in enumerate(chain.translators):
            lines.append(f"  {idx+1}. {t_id}")
            
        return "\n".join(lines)
