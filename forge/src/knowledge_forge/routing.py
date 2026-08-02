import re
import unicodedata
from typing import cast

_TOKEN_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


def _ordered_tokens(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return _TOKEN_PATTERN.findall(normalized)


def _tokens(value: str) -> set[str]:
    return set(_ordered_tokens(value))


def _score(query_tokens: set[str], terms: list[str]) -> int:
    term_tokens: set[str] = set()
    for term in terms:
        term_tokens.update(_tokens(term))
    return len(query_tokens & term_tokens)


def _contains_phrase(query: str, phrase: str) -> bool:
    query_tokens = _ordered_tokens(query)
    phrase_tokens = _ordered_tokens(phrase)
    width = len(phrase_tokens)
    return bool(width) and any(
        query_tokens[index : index + width] == phrase_tokens
        for index in range(len(query_tokens) - width + 1)
    )


def _module_score(
    query: str, descriptor: dict[str, object], excluded_tokens: set[str]
) -> int:
    query_tokens = _tokens(query) - excluded_tokens
    title = cast(str, descriptor["title"])
    aliases = cast(list[str], descriptor["aliases"])
    tags = cast(list[str], descriptor["tags"])
    score = _score(query_tokens, tags + aliases + [title])
    if not _tokens(title).issubset(excluded_tokens) and _contains_phrase(
        query, title
    ):
        score += 100
    score += 50 * sum(
        not _tokens(alias).issubset(excluded_tokens)
        and _contains_phrase(query, alias)
        for alias in aliases
    )
    return score


def _not_covered() -> dict[str, object]:
    return {"status": "not-covered", "area_id": None, "module_ids": []}


def route_query(query: str, indexes: dict[str, object]) -> dict[str, object]:
    query_tokens = _tokens(query)
    if not query_tokens:
        return _not_covered()
    l0 = cast(dict[str, object], indexes["l0"])
    areas = cast(list[dict[str, object]], l0["areas"])
    alias_scores = {
        cast(str, area["id"]): _score(
            query_tokens,
            cast(list[str], area["aliases"]),
        )
        for area in areas
    }
    scores = {
        cast(str, area["id"]): alias_scores[cast(str, area["id"])]
        + (100 if _contains_phrase(query, cast(str, area["title"])) else 0)
        for area in areas
    }
    if max(scores.values(), default=0) == 0:
        scores = {
            cast(str, area["id"]): _score(
                query_tokens,
                [cast(str, area["title"])],
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
    selected_area = next(
        area for area in areas if cast(str, area["id"]) == area_id
    )
    excluded_tokens = _tokens(cast(str, selected_area["title"]))
    l1 = cast(dict[str, dict[str, object]], indexes["l1"])
    descriptors = cast(list[dict[str, object]], l1[area_id]["modules"])
    module_scores = {
        cast(str, descriptor["id"]): _module_score(
            query, descriptor, excluded_tokens
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
