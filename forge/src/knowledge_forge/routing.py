import re
import unicodedata
from typing import cast

_TOKEN_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def _tokens(value: str) -> set[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return set(_TOKEN_PATTERN.findall(normalized))


def _score(query_tokens: set[str], terms: list[str]) -> int:
    term_tokens: set[str] = set()
    for term in terms:
        term_tokens.update(_tokens(term))
    return len(query_tokens & term_tokens)


def _not_covered() -> dict[str, object]:
    return {"status": "not-covered", "area_id": None, "module_ids": []}


def route_query(query: str, indexes: dict[str, object]) -> dict[str, object]:
    query_tokens = _tokens(query)
    if not query_tokens:
        return _not_covered()
    l0 = cast(dict[str, object], indexes["l0"])
    areas = cast(list[dict[str, object]], l0["areas"])
    scores = {
        cast(str, area["id"]): _score(
            query_tokens,
            cast(list[str], area["aliases"]),
        )
        for area in areas
    }
    best_score = max(scores.values(), default=0)
    if best_score == 0:
        return _not_covered()
    top_areas = sorted(
        area_id for area_id, score in scores.items() if score == best_score
    )
    if len(top_areas) > 1:
        return {
            "status": "ambiguous",
            "area_id": None,
            "module_ids": [],
            "alternatives": top_areas,
        }
    area_id = top_areas[0]
    l1 = cast(dict[str, dict[str, object]], indexes["l1"])
    descriptors = cast(list[dict[str, object]], l1[area_id]["modules"])
    module_scores = {
        cast(str, descriptor["id"]): _score(
            query_tokens,
            cast(list[str], descriptor["tags"])
            + cast(list[str], descriptor["aliases"])
            + [cast(str, descriptor["title"])],
        )
        for descriptor in descriptors
    }
    highest_module_score = max(module_scores.values(), default=0)
    module_ids = (
        [
            min(
                module_id
                for module_id, score in module_scores.items()
                if score == highest_module_score
            )
        ]
        if highest_module_score > 0
        else []
    )
    return {"status": "covered", "area_id": area_id, "module_ids": module_ids}
