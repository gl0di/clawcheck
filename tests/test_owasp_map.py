"""OWASP Top 10 for LLM Apps 2025 coverage mapping (additive metadata, no verdict impact)."""
import json

from clawseccheck import audit, render_json
from clawseccheck.catalog import BY_ID, OWASP_LLM_2025, OWASP_MAP, owasp_for


# ---- mapping integrity ----
def test_every_mapped_id_is_a_real_check():
    for cid in OWASP_MAP:
        assert cid in BY_ID, f"OWASP_MAP references unknown check id {cid!r}"


def test_every_code_is_a_valid_owasp_llm_2025_code():
    for cid, codes in OWASP_MAP.items():
        assert isinstance(codes, tuple)
        for code in codes:
            assert code in OWASP_LLM_2025, f"{cid} maps to unknown OWASP code {code!r}"


def test_owasp_for_unmapped_returns_empty():
    assert owasp_for("B50") == ()      # host-watch: intentionally unmapped
    assert owasp_for("ZZ99") == ()     # unknown id


def test_owasp_llm_2025_has_ten_canonical_codes():
    assert len(OWASP_LLM_2025) == 10
    assert set(OWASP_LLM_2025) == {f"LLM{n:02d}" for n in range(1, 11)}


# ---- the positioning claim: the multi-agent / agency arc maps to Excessive Agency ----
def test_multiagent_checks_map_to_excessive_agency():
    for cid in ("A1", "B45", "B46", "B47"):
        assert "LLM06" in owasp_for(cid), f"{cid} should map to LLM06 Excessive Agency"


def test_supply_chain_checks_map_to_llm03():
    for cid in ("B5", "B13", "B25", "B42"):
        assert "LLM03" in owasp_for(cid)


# ---- JSON surfacing ----
def test_render_json_includes_owasp_per_finding(tmp_path):
    _, findings, score = audit("fixtures/home_vuln", include_native=False, include_host=False)
    data = json.loads(render_json(findings, score))
    by_id = {f["id"]: f for f in data["findings"]}
    # every serialized finding carries an owasp list of valid codes
    for f in data["findings"]:
        assert "owasp" in f and isinstance(f["owasp"], list)
        for code in f["owasp"]:
            assert code in OWASP_LLM_2025
    # a mapped check exposes its codes; an unmapped one is an empty list (not absent)
    assert by_id["A1"]["owasp"] == ["LLM01", "LLM06"]
    assert by_id["B50"]["owasp"] == []
