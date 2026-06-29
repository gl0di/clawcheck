"""B12 — local-first model preference (check_local_first).

Verdicts:
  UNKNOWN : no model config found (no agents.defaults.model and no models key)
  PASS    : model names present; none contain a cloud-provider substring
  WARN    : at least one model name contains a cloud-provider name
            (CLOUD_PROVIDERS: openai, anthropic, gpt, claude, google, gemini, grok, mistral, cohere)
  (no FAIL)

Note: {} produces UNKNOWN (not PASS) because _model_names({}) returns [],
verified against checks.py:check_local_first.
"""
from pathlib import Path

from clawseccheck.catalog import FAIL, PASS, UNKNOWN, WARN
from clawseccheck.checks import check_local_first
from clawseccheck.collector import Context


def _ctx(cfg: dict) -> Context:
    c = Context(home=Path("/nonexistent"))
    c.config = cfg
    return c


# ---- UNKNOWN: no model config ----

def test_b12_empty_config_unknown():
    # {} has no agents.defaults.model and no models key -> _model_names returns []
    assert check_local_first(_ctx({})).status == UNKNOWN


def test_b12_unrelated_config_unknown():
    # config with keys that contain no model information
    assert check_local_first(_ctx({"gateway": {"port": 19001}})).status == UNKNOWN


# ---- PASS: local model(s) only ----

def test_b12_local_model_primary_passes():
    cfg = {"agents": {"defaults": {"model": {"primary": "llama"}}}}
    assert check_local_first(_ctx(cfg)).status == PASS


def test_b12_local_model_phi_passes():
    cfg = {"agents": {"defaults": {"model": {"primary": "phi-3"}}}}
    assert check_local_first(_ctx(cfg)).status == PASS


def test_b12_models_dict_local_provider_passes():
    cfg = {"models": {"local-llm": {"provider": "ollama"}}}
    assert check_local_first(_ctx(cfg)).status == PASS


def test_b12_models_list_all_local_passes():
    cfg = {"models": ["llama", "phi"]}
    assert check_local_first(_ctx(cfg)).status == PASS


def test_b12_local_primary_and_local_fallbacks_passes():
    cfg = {"agents": {"defaults": {"model": {"primary": "llama", "fallbacks": ["mistral-local"]}}}}
    # "mistral-local" contains "mistral" which IS in CLOUD_PROVIDERS -> WARN, not PASS
    # Use a safe fallback name instead
    cfg = {"agents": {"defaults": {"model": {"primary": "llama", "fallbacks": ["phi-3"]}}}}
    assert check_local_first(_ctx(cfg)).status == PASS


# ---- WARN: at least one cloud-provider name found ----

def test_b12_gpt_model_warns():
    cfg = {"agents": {"defaults": {"model": {"primary": "gpt-4"}}}}
    f = check_local_first(_ctx(cfg))
    assert f.status == WARN


def test_b12_openai_model_warns():
    cfg = {"agents": {"defaults": {"model": {"primary": "openai/gpt-4o"}}}}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_anthropic_model_warns():
    cfg = {"models": {"main": {"provider": "anthropic"}}}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_claude_in_name_warns():
    cfg = {"agents": {"defaults": {"model": {"primary": "claude-3-haiku"}}}}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_gemini_model_warns():
    cfg = {"agents": {"defaults": {"model": {"primary": "gemini-pro"}}}}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_google_provider_warns():
    cfg = {"models": {"vision": {"provider": "google"}}}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_models_list_mixed_cloud_warns():
    # list with one cloud entry -> WARN
    cfg = {"models": ["llama", "gpt-4"]}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_cloud_fallback_warns():
    # local primary but cloud fallback -> WARN
    cfg = {"agents": {"defaults": {"model": {"primary": "llama", "fallbacks": ["gpt-4"]}}}}
    assert check_local_first(_ctx(cfg)).status == WARN


def test_b12_warn_detail_names_provider():
    cfg = {"agents": {"defaults": {"model": {"primary": "gpt-4o"}}}}
    f = check_local_first(_ctx(cfg))
    assert f.status == WARN
    assert "gpt" in f.detail.lower() or "cloud" in f.detail.lower()


# ---- never FAIL ----

def test_b12_never_fail():
    for cfg in (
        {},
        {"agents": {"defaults": {"model": {"primary": "llama"}}}},
        {"agents": {"defaults": {"model": {"primary": "gpt-4"}}}},
        {"models": ["openai"]},
        {"models": {"x": {"provider": "anthropic"}}},
    ):
        assert check_local_first(_ctx(cfg)).status != FAIL, (
            f"B12 must never return FAIL; got FAIL for {cfg}"
        )
