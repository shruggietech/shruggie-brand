#!/usr/bin/env python3
"""Validate and resolve BrandBuilder's bounded component recipe contract."""

import copy
import json
import re
from pathlib import Path

from schema_validation import SchemaValidationError, validate_json_schema


HERE = Path(__file__).resolve().parent
REFERENCES = HERE.parent / "references"

COMPONENT_IDS = (
    "AppFrame", "Button", "IconButton", "Toolbar", "Tabs", "Menu", "Dialog",
    "Field", "FormControls", "ListRow", "SplitPane", "Toast", "StatusBadge",
    "Card", "EmptyState",
)
RESPONSIBILITIES = (
    "safe_area", "dynamic_viewport", "root_scrolling", "fixed_chrome",
    "ime_obstruction", "titlebar_regions", "global_focus",
)
REQUIRED_DIMENSIONS = (
    "purpose", "element", "variants", "densities", "states", "roles", "keyboard",
    "target", "icons", "accessibility", "motion", "responsive", "overrides",
    "owner", "verification",
)
REQUIRED_FORBIDS = {
    "application-screens", "product-navigation", "route-trees",
    "renderer-property-bags", "raw-visual-values", "free-form-nesting",
}
INVARIANT_OVERRIDE_ROOTS = {
    "keyboard", "target", "icons.accessible_name", "accessibility", "motion.reduced",
    "responsive.inputs", "owner", "verification",
}
MINIMUM_STATES = {
    "AppFrame": {"default", "focus-visible"},
    "Button": {"default", "hover", "pressed", "focus-visible", "disabled", "loading"},
    "IconButton": {"default", "hover", "pressed", "focus-visible", "disabled", "loading"},
    "Toolbar": {"default", "hover", "pressed", "focus-visible", "disabled", "selected"},
    "Tabs": {"default", "hover", "pressed", "focus-visible", "disabled", "selected"},
    "Menu": {"default", "hover", "pressed", "focus-visible", "disabled", "selected"},
    "Dialog": {"default", "focus-visible", "loading", "invalid", "warning", "success"},
    "Field": {"default", "focus-visible", "disabled", "invalid", "warning", "success"},
    "FormControls": {"default", "hover", "pressed", "focus-visible", "disabled", "invalid", "warning", "success"},
    "ListRow": {"default", "hover", "pressed", "focus-visible", "disabled", "selected"},
    "SplitPane": {"default", "hover", "pressed", "focus-visible", "disabled"},
    "Toast": {"default", "hover", "focus-visible", "warning", "success"},
    "StatusBadge": {"default", "warning", "success"},
    "Card": {"default", "hover", "focus-visible", "selected"},
    "EmptyState": {"default", "focus-visible", "loading"},
}
EXPECTED_VARIANTS = {
    "AppFrame": {"default"},
    "Button": {"primary", "secondary", "ghost", "destructive"},
    "IconButton": {"primary", "secondary", "ghost", "destructive"},
    "Toolbar": {"horizontal", "vertical"},
    "Tabs": {"automatic", "manual"},
    "Menu": {"dropdown"},
    "Dialog": {"modal", "alert"},
    "Field": {"stacked", "inline"},
    "FormControls": {"input", "textarea", "select", "checkbox", "radio"},
    "ListRow": {"static", "action", "selection"},
    "SplitPane": {"horizontal", "vertical"},
    "Toast": {"status", "warning", "error"},
    "StatusBadge": {"neutral", "success", "warning", "error"},
    "Card": {"plain", "outlined", "elevated"},
    "EmptyState": {"informational", "actionable"},
}
REQUIRED_KEYBOARD_TERMS = {
    "AppFrame": {"tab", "skip link"},
    "Button": {"enter", "space"},
    "IconButton": {"enter", "space"},
    "Toolbar": {"arrow", "home", "end"},
    "Tabs": {"arrow", "home", "end", "enter", "space"},
    "Menu": {"arrow", "home", "end", "typeahead", "escape"},
    "Dialog": {"tab", "escape", "focus"},
    "Field": {"label", "focus"},
    "FormControls": {"native", "space"},
    "ListRow": {"native", "selection", "activation"},
    "SplitPane": {"arrow", "home", "end"},
    "Toast": {"tab", "escape", "focus"},
    "StatusBadge": {"no special keyboard interaction"},
    "Card": {"native controls"},
    "EmptyState": {"native button or link"},
}
ICON_POLICIES = {"optional", "prohibited", "required"}
ICON_NAME_POLICIES = {
    "close-control-required", "content-owned", "decorative-unless-informative",
    "inherited-from-control", "item-label", "not-name-source", "per-control",
    "required-on-control", "row-label", "separator-label-required",
    "status-text-required", "visible-label", "visible-status-text",
}
ACCESSIBILITY_ROLES = {
    "application-landmarks", "article-or-section", "button", "dialog", "group",
    "listitem", "menu", "native", "section", "separator", "status-or-alert",
    "status-text", "tabs", "toolbar",
}
ACCESSIBILITY_NAMES = {
    "field-label-required", "heading-required", "heading-when-needed", "landmarks",
    "message-required", "required", "required-visible-or-aria", "row-label-required",
    "tablist-required", "title-required", "trigger-required", "visible-label-required",
    "visible-text-required",
}
ACCESSIBILITY_FOCUS = {
    "action-only", "contained-roving", "delegated-to-control", "global-boundary",
    "nested-controls", "none", "roving", "self", "single-action-only",
    "trapped-and-returned",
}
ACCESSIBILITY_RELATIONSHIPS = {
    "control-describedby-message", "dialog-describedby-description",
    "dialog-labelledby-title", "field-owned", "header-main-overlay",
    "label-for-control", "panel-labelledby-tab", "section-labelledby-heading",
    "separator-controls-primary-pane", "tab-controls-panel", "trigger-controls-menu",
    "viewport-owned-by-app-frame",
}
RESPONSIVE_INPUTS = {
    "forced_colors", "hover", "ime_obstruction", "pointer_precision",
    "reduced_motion", "safe_area", "text_scale", "titlebar_regions", "touch",
    "viewport", "window_class",
}
RESPONSIVE_COMPACT = {
    "edge-contained", "full-width", "horizontal-scroll", "minimum-target",
    "overflow-scroll", "single-column", "stacked", "stacked-or-clamped",
    "viewport-contained", "wrap", "wrap-label", "wrap-metadata",
}
RESPONSIVE_EXPANDED = {
    "anchor-contained", "bounded", "bounded-content", "centered", "columns",
    "configured", "corner-contained", "intrinsic", "minimum-target", "resizable",
}
OVERRIDE_ROLE_COMPATIBILITY = {
    ("AppFrame", "background"): {"surface.background"},
    ("Button", "fill"): {"action.primary"},
    ("IconButton", "fill"): {"action.primary"},
    ("Toolbar", "surface"): {"surface.card"},
    ("Tabs", "selected"): {"action.primary"},
    ("Menu", "surface"): {"surface.overlay"},
    ("Dialog", "surface"): {"surface.overlay"},
    ("FormControls", "surface"): {"surface.background"},
    ("ListRow", "surface"): {"surface.card"},
    ("SplitPane", "divider"): {"border.default", "border.strong"},
    ("Toast", "surface"): {"surface.overlay"},
    ("Card", "surface"): {"surface.card"},
}
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


class ComponentContractError(ValueError):
    """A recipe catalog or resolved override violates the bounded contract."""


def _require(condition, message):
    if not condition:
        raise ComponentContractError(message)


def _read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _require_closed_object(name, dimension, value, keys):
    _require(isinstance(value, dict) and set(value) == set(keys),
             "%s %s contract is malformed" % (name, dimension))


def _validate_bounded_dimensions(name, recipe, interface_roles):
    icons = recipe["icons"]
    _require_closed_object(name, "icons", icons, {"policy", "accessible_name"})
    _require(icons["policy"] in ICON_POLICIES and icons["accessible_name"] in ICON_NAME_POLICIES,
             "%s icons contract contains an unknown or raw value" % name)

    accessibility = recipe["accessibility"]
    _require_closed_object(
        name, "accessibility", accessibility, {"role", "name", "focus", "relationships"}
    )
    _require(accessibility["role"] in ACCESSIBILITY_ROLES,
             "%s accessibility role is unknown" % name)
    _require(accessibility["name"] in ACCESSIBILITY_NAMES,
             "%s accessibility naming contract is unknown" % name)
    _require(accessibility["focus"] in ACCESSIBILITY_FOCUS,
             "%s accessibility focus contract is unknown" % name)
    relationships = accessibility["relationships"]
    _require(isinstance(relationships, list) and len(relationships) == len(set(relationships)),
             "%s accessibility relationships are malformed" % name)
    _require(set(relationships).issubset(ACCESSIBILITY_RELATIONSHIPS),
             "%s accessibility relationships contain an unknown value" % name)

    motion = recipe["motion"]
    _require_closed_object(name, "motion", motion, {"standard", "reduced"})
    for key, reference in motion.items():
        _require(isinstance(reference, str) and reference.startswith("$role."),
                 "%s motion %s must use an Interface Canon role reference" % (name, key))
        role = reference[len("$role."):]
        _require(role in interface_roles and role.startswith("motion."),
                 "%s motion %s references an incompatible role" % (name, key))

    responsive = recipe["responsive"]
    _require_closed_object(name, "responsive", responsive, {"inputs", "compact", "expanded"})
    inputs = responsive["inputs"]
    _require(isinstance(inputs, list) and inputs and len(inputs) == len(set(inputs)),
             "%s responsive inputs are malformed" % name)
    _require(set(inputs).issubset(RESPONSIVE_INPUTS),
             "%s responsive inputs contain an unknown value" % name)
    _require(responsive["compact"] in RESPONSIVE_COMPACT,
             "%s responsive compact behavior is unknown or raw" % name)
    _require(responsive["expanded"] in RESPONSIVE_EXPANDED,
             "%s responsive expanded behavior is unknown or raw" % name)


def load_component_catalog(path=None):
    return _read_json(path or REFERENCES / "component-recipes.json")


def load_component_schema(path=None):
    return _read_json(path or REFERENCES / "component-recipes.schema.json")


def _validate_recipe(name, recipe, interface_roles, minimum_target):
    _require(set(recipe) == set(REQUIRED_DIMENSIONS),
             "%s recipe dimensions differ from the required contract" % name)
    for field in ("purpose", "element"):
        _require(isinstance(recipe[field], str) and recipe[field].strip(),
                 "%s %s must be a non-empty string" % (name, field))
    for field in ("variants", "densities", "states", "keyboard", "overrides", "verification"):
        _require(isinstance(recipe[field], list), "%s %s must be an array" % (name, field))
        _require(len(recipe[field]) == len(set(recipe[field])), "%s %s repeats values" % (name, field))
    keyboard_contract = " ".join(recipe["keyboard"]).lower()
    _require(recipe["keyboard"], "%s keyboard contract must not be empty" % name)
    missing_keyboard = REQUIRED_KEYBOARD_TERMS[name] - {
        term for term in REQUIRED_KEYBOARD_TERMS[name] if term in keyboard_contract
    }
    if missing_keyboard:
        raise ComponentContractError(
            "%s keyboard contract is missing %s behavior" % (name, sorted(missing_keyboard)[0])
        )
    states = set(recipe["states"])
    missing_states = MINIMUM_STATES[name] - states
    unknown_states = states - MINIMUM_STATES[name]
    if missing_states:
        raise ComponentContractError("%s is missing required state %s" % (name, sorted(missing_states)[0]))
    if unknown_states:
        raise ComponentContractError("%s has unknown state %s" % (name, sorted(unknown_states)[0]))
    _require(set(recipe["variants"]) == EXPECTED_VARIANTS[name],
             "%s has an unknown or missing variant" % name)
    _require(set(recipe["densities"]) == {"comfortable", "compact"},
             "%s must cover comfortable and compact density" % name)
    _require(isinstance(recipe["roles"], dict) and recipe["roles"], "%s roles are missing" % name)
    for assignment, reference in recipe["roles"].items():
        _require(isinstance(reference, str) and reference.startswith("$role."),
                 "%s %s must use an Interface Canon role reference" % (name, assignment))
        role = reference[len("$role."):]
        _require(role in interface_roles, "%s references unknown role %s" % (name, role))
    target = recipe["target"]
    _require(isinstance(target, dict) and set(target) == {"interactive", "minimum"},
             "%s target contract is malformed" % name)
    _require(isinstance(target["interactive"], bool) and isinstance(target["minimum"], int),
             "%s target values are malformed" % name)
    if target["interactive"]:
        _require(target["minimum"] >= minimum_target,
                 "%s minimum target is below the invariant" % name)
    else:
        _require(target["minimum"] == 0, "%s non-interactive target must be zero" % name)
    _require(recipe["owner"] in {"server", "client", "app-frame"},
             "%s owner is unsupported" % name)
    if name == "IconButton":
        _require(recipe["accessibility"]["name"] == "required",
                 "IconButton requires an accessible name")
        _require(recipe["icons"].get("policy") == "required",
                 "IconButton requires an icon")
    _validate_bounded_dimensions(name, recipe, interface_roles)
    for override in recipe["overrides"]:
        _require(not any(override == root or override.startswith(root + ".") for root in INVARIANT_OVERRIDE_ROOTS),
                 "%s declares invariant override %s" % (name, override))
        _require(override.startswith("roles."), "%s override must target an expressive role" % name)
        _require(override[len("roles."):] in recipe["roles"],
                 "%s override targets an unknown assignment" % name)
    _require(recipe["motion"]["reduced"] == "$role.motion.reduced",
             "%s must preserve the reduced-motion invariant" % name)


def validate_app_frame_profiles(profiles):
    names = [p.get("profile") for p in profiles] if isinstance(profiles, list) else []
    _require(len(names) == 3 and len(names) == len(set(names)) and set(names) == {"browser", "tauri", "wails"},
             "AppFrame profiles must contain browser, tauri, and wails")
    for profile in profiles:
        name = profile.get("profile", "unknown")
        responsibilities = profile.get("responsibilities")
        _require(isinstance(responsibilities, dict), "%s AppFrame responsibilities are missing" % name)
        missing = set(RESPONSIBILITIES) - set(responsibilities)
        if missing:
            raise ComponentContractError("%s AppFrame missing owner for %s" % (name, sorted(missing)[0]))
        extra = set(responsibilities) - set(RESPONSIBILITIES)
        if extra:
            raise ComponentContractError("%s AppFrame has unknown responsibility %s" % (name, sorted(extra)[0]))
        handoff = profile.get("handoff")
        _require(isinstance(handoff, dict), "%s AppFrame handoff must be an object" % name)
        for responsibility, owner in responsibilities.items():
            _require(isinstance(owner, str) and owner in {"app-frame", "host"},
                     "%s %s must have exactly one owner" % (name, responsibility))
            if owner == "host":
                _require(isinstance(handoff.get(responsibility), str) and handoff[responsibility],
                         "%s %s requires a host handoff" % (name, responsibility))
            else:
                _require(responsibility not in handoff,
                         "%s %s has a duplicate host handoff" % (name, responsibility))
        capabilities = profile.get("capabilities")
        _require(isinstance(capabilities, list) and capabilities,
                 "%s capability list is missing" % name)
        _require("operating_system" not in capabilities and "os" not in capabilities,
                 "%s profile cannot route from an operating system" % name)
    return profiles


def validate_component_catalog(catalog, interface_canon):
    try:
        validate_json_schema(catalog, load_component_schema())
    except SchemaValidationError as error:
        raise ComponentContractError("component recipe schema violation: %s" % error) from error
    _require(SEMVER.fullmatch(catalog.get("version", "")) is not None,
             "component recipe version must be semantic")
    _require(interface_canon.get("version") in catalog["interface_canon_compatibility"],
             "component recipes do not support Interface Canon %s" % interface_canon.get("version"))
    grammar = catalog["grammar"]
    _require(grammar.get("expresses") == ["bounded-component-recipes"],
             "component grammar can express an application-screen or unknown grammar")
    _require(REQUIRED_FORBIDS.issubset(set(grammar.get("forbids", []))),
             "component grammar does not forbid arbitrary screens and renderer values")
    _require(tuple(catalog["required_dimensions"]) == REQUIRED_DIMENSIONS,
             "required recipe dimensions differ from the governed order")
    components = catalog["components"]
    _require(set(components) == set(COMPONENT_IDS),
             "component catalog must contain exactly the bounded recipe vocabulary")
    interface_roles = set(interface_canon.get("role_catalog", []))
    minimum_target = int(interface_canon["invariants"]["minimum_target_logical_units"])
    for name in COMPONENT_IDS:
        _validate_recipe(name, components[name], interface_roles, minimum_target)
    validate_app_frame_profiles(catalog["app_frame_profiles"])
    coverage = catalog["coverage"]
    names = [row.get("component") for row in coverage]
    _require(len(names) == len(set(names)) and set(names) == set(COMPONENT_IDS),
             "component coverage must contain exactly one row per recipe")
    for row in coverage:
        name = row["component"]
        _require(set(row.get("states", [])) == set(components[name]["states"]),
                 "%s coverage states disagree with its recipe" % name)
        _require("web-react" in row.get("adapters", []),
                 "%s coverage omits the Web/React adapter" % name)
        _require(set(row.get("verification", [])).issubset(set(components[name]["verification"])),
                 "%s coverage cites an unknown verification" % name)
    return catalog


def resolve_component_catalog(brand, catalog=None, interface_canon=None):
    catalog = copy.deepcopy(catalog or load_component_catalog())
    interface_canon = interface_canon or _read_json(REFERENCES / "interface-canon.json")
    validate_component_catalog(catalog, interface_canon)
    overrides = brand.get("component_overrides") or {}
    _require(isinstance(overrides, dict), "component overrides must be an object")
    for component, values in overrides.items():
        _require(component in catalog["components"], "component override targets unknown recipe %s" % component)
        _require(isinstance(values, dict), "%s component override must be an object" % component)
        allowed = set(catalog["components"][component]["overrides"])
        for key, value in values.items():
            _require(key in allowed, "%s declares invariant override %s" % (component, key))
            _require(isinstance(value, str) and value.startswith("$role."),
                     "%s override %s must use a semantic role" % (component, key))
            role = value[len("$role."):]
            _require(role in set(interface_canon.get("role_catalog", [])),
                     "%s override %s references unknown role %s" % (component, key, role))
            assignment = key[len("roles."):]
            compatible = OVERRIDE_ROLE_COMPATIBILITY.get((component, assignment), set())
            _require(role in compatible,
                     "%s override %s uses assignment-incompatible role %s" %
                     (component, key, role))
    return {
        "id": catalog["id"],
        "kind": "resolved-component-recipes",
        "version": catalog["version"],
        "interface_canon_version": interface_canon["version"],
        "brand": brand["slug"],
        "components": catalog["components"],
        "app_frame_profiles": catalog["app_frame_profiles"],
        "coverage": catalog["coverage"],
        "overrides": overrides,
    }
