from __future__ import annotations

"""Simple settings loader for TapTrust."""

import os
from functools import lru_cache
from pathlib import Path
from typing import Dict, Set

import yaml

# Default AIDs used if none are configured
DEFAULT_KNOWN_AIDS: Dict[str, bytes] = {
    "ISO18013": bytes.fromhex("D276000024010200"),
    "GET": bytes.fromhex("A0000003965400"),
    "Thales": bytes.fromhex("A0000002471001"),
}

DEFAULT_EF_COM_FILE_ID = 0x0015

SETTINGS_ENV = "TAPTRUST_SETTINGS"


def _settings_path() -> Path:
    env = os.getenv(SETTINGS_ENV)
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[2] / "settings.yaml"


@lru_cache(maxsize=1)
def _load() -> dict:
    path = _settings_path()
    if not path.exists():
        return {}
    try:
        with path.open("r") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return {}
    return data


def get_allowed_issuers() -> Set[str]:
    """Return the allowed issuer whitelist as uppercase strings."""
    issuers = _load().get("allowed_issuers", [])
    if not isinstance(issuers, list):
        return set()
    return {str(i).upper() for i in issuers if isinstance(i, str)}


def get_known_aids() -> Dict[str, bytes]:
    """Return mapping of AID names to bytes from configuration."""
    aids = _load().get("known_aids")
    if isinstance(aids, dict):
        parsed: Dict[str, bytes] = {}
        for name, value in aids.items():
            try:
                parsed[str(name)] = bytes.fromhex(str(value))
            except Exception:
                continue
        if parsed:
            return parsed
    return DEFAULT_KNOWN_AIDS


def get_ef_com_file_id() -> int:
    """Return EF.Com file identifier from configuration."""
    fid = _load().get("ef_com_file_id")
    if isinstance(fid, int) and 0 <= fid <= 0xFFFF:
        return fid
    if isinstance(fid, str):
        try:
            val = int(fid, 0)
            if 0 <= val <= 0xFFFF:
                return val
        except ValueError:
            pass
    return DEFAULT_EF_COM_FILE_ID


def reload_settings() -> None:
    """Clear the cached settings so they will be reloaded on next access."""
    _load.cache_clear()
