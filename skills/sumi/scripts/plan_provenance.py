"""Shared plan hashing; no validator imports or review side effects."""
import hashlib
import json


def plan_digest(data):
    """Hash authored plan/content records, excluding review containers."""
    def without_review(record):
        core = {key: value for key, value in record.items() if key != "proof"}
        if isinstance(core.get("style_profile"), dict):
            core["style_profile"] = {key: value for key, value in core["style_profile"].items()
                                     if key != "review"}
        return core
    core = without_review(data)
    core["shots"] = [
        without_review(shot)
        for shot in data.get("shots", [])
    ]
    return hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
