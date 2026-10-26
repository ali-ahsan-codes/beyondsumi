"""Current style identifiers; earlier movement methods are compatibility data only."""

VERSION = "1.0.0"
PLAN_COMPATIBILITY_VERSION = "5.1.2"  # Existing plan validation contracts, separate from public release tags.
CATALOG_ID = "three-styles-v4"
STYLES = {
    "sumi-original": {
        "name": "Sumi Original",
        "short_description": "Painted Japanese stories with richer character acting and emotional depth.",
        "recommended_for": "richer animated stories and expressive character acting",
        "drawing_budget_mode": "action-driven",
        "character_update_fps": 20,
        "state_source_policy": "whole-drawings-or-supported-derived-acting",
        "motion_direction": "integrated Sumi-e scenes, matching cinematic views and purposeful acting",
        "profile": "original-preservation-v1",
        "mechanism": "preserved-original-sumi",
        "default_output_fps": 30,
        "presentation": {
            "treatment": "Sumi Anime within Sumi Original",
            "default_aspect": "16:9",
            "fill": "edge-to-edge painted scene",
            "caption_reference_baseline_y": 0.95,
            "caption_lift_frame_height": 0.10,
            "caption_baseline_y": 0.85,
            "caption_backing": "compact readable paper or translucent tone",
            "opening": "distinct anime-inspired Sumi hook/title; clean type motion, no animated brush or splash reveal",
        },
    },
    "sumi-light": {
        "name": "Sumi Light",
        "short_description": "Colourful brush-and-ink romance, children’s/general stories and documentaries.",
        "recommended_for": "romance, children’s and general stories, and documentaries",
        "motion_direction": "approved brush acting, story-selected colours and explanatory camera",
        "profile": "brush-ink-on-twos-v2",
        "mechanism": "layered-brush-ink",
        "default_output_fps": 24,
    },
    "sumi-dark": {
        "name": "Sumi Dark",
        "short_description": "Dramatic ink, selective red and cinematic reveals for horror and mystery.",
        "recommended_for": "horror, mystery and dark stories",
        "motion_direction": "large splash-built forms, camera-led depth/reveals and purposeful dark red",
        "profile": "brush-ink-on-twos-v2",
        "mechanism": "layered-brush-ink",
        "default_output_fps": 24,
    },
}

# Explicit historical compatibility. These are not current style choices and
# must never be silently translated into one of the three current styles.
LEGACY_METHODS = {
    "sumi-brush": "ordered-stroke-redraw",
    "living-ink": "evolving-ink-mass",
    "drawn-acting": "whole-pose-replacement",
    "sumi-graphic": "painted-shape-transformation",
}


def style_for_shot(shot):
    return shot.get("style") if isinstance(shot, dict) else None


def uses_current_catalog(plan):
    return isinstance(plan, dict) and (
        plan.get("catalog") == CATALOG_ID
        or any(style_for_shot(s) is not None for s in plan.get("shots", [])
               if isinstance(s, dict))
    )
