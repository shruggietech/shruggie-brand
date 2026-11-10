"""Reconcile and verify the owner-approved canonical brand alias (Python 3.8+)."""
import argparse
import copy
import datetime
import http.client
import json
import os
from pathlib import Path
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

ZONE = "shruggie.tech"
ALIAS = "brands.shruggie.tech"
CANONICAL = "brand.shruggie.tech"
PHASE = "http_request_dynamic_redirect"
REF = "s075_brands_canonical_redirect"
EXPRESSION = '(http.host eq "brands.shruggie.tech")'
VOLATILE = {"version", "last_updated", "modified_on", "created_on", "comment_modified_on", "tags_modified_on"}


def require(value, message):
    if not value:
        raise ValueError(message)


class APIError(RuntimeError):
    def __init__(self, status, codes):
        super().__init__("Cloudflare HTTP %s, error codes %s" % (status, codes))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Cloudflare:
    def __init__(self, token):
        self.token = token

    def request(self, method, path, body=None, missing=False):
        require(not path.startswith("/") and "://" not in path and ".." not in path, "Invalid API path")
        request = urllib.request.Request("https://api.cloudflare.com/client/v4/" + path, method=method,
                                         data=None if body is None else json.dumps(body).encode("utf-8"),
                                         headers={"Authorization": "Bearer " + self.token,
                                                  "Content-Type": "application/json"})
        try:
            with urllib.request.build_opener(NoRedirect()).open(request, timeout=30) as response:
                data = json.load(response)
        except urllib.error.HTTPError as error:
            try:
                codes = [item.get("code") for item in json.load(error).get("errors", [])]
            except (ValueError, TypeError):
                codes = []
            if missing and error.code == 404:
                return None
            raise APIError(error.code, codes) from None
        except (urllib.error.URLError, OSError):
            raise RuntimeError("Cloudflare transport failed; inspect current state before retrying a write") from None
        if not data.get("success"):
            raise APIError(200, [item.get("code") for item in data.get("errors", [])])
        return data.get("result")


def token():
    value = os.environ.get("CF_DNS_API_TOKEN")
    if not value and os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                value = winreg.QueryValueEx(key, "CF_DNS_API_TOKEN")[0]
        except FileNotFoundError:
            pass
    require(value and value.strip(), "CF_DNS_API_TOKEN is missing from process or Windows User environment")
    return value.strip()


def clean(value):
    return {key: copy.deepcopy(item) for key, item in value.items() if key not in VOLATILE}


def desired_rule():
    return {"ref": REF, "description": "S075 canonical brand alias", "enabled": True,
            "action": "redirect", "expression": EXPRESSION,
            "action_parameters": {"from_value": {"status_code": 301, "preserve_query_string": True,
                "target_url": {"expression": 'concat("https://brand.shruggie.tech", http.request.uri.path)'}}}}


def dns_payload(record):
    return {key: copy.deepcopy(record[key]) for key in
            ("type", "name", "content", "ttl", "proxied", "comment", "tags", "settings") if key in record}


def rule_payload(rule):
    return {key: copy.deepcopy(value) for key, value in clean(rule).items() if key != "id"}


def snapshot(api):
    zones = api.request("GET", "zones?name=%s&per_page=50" % ZONE)
    zones = [zone for zone in zones if zone["name"] == ZONE and zone["status"] == "active"]
    require(len(zones) == 1, "Expected exactly one active authorized zone")
    zone_id = zones[0]["id"]
    records, page = [], 1
    while True:
        batch = api.request("GET", "zones/%s/dns_records?per_page=100&page=%d" % (zone_id, page))
        records.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    entry = api.request("GET", "zones/%s/rulesets/phases/%s/entrypoint" % (zone_id, PHASE), missing=True)
    require(entry is None or (entry.get("phase") == PHASE and entry.get("kind") == "zone"),
            "Unexpected redirect entrypoint")
    return {"zone": zone_id, "records": records, "entry": entry}


def managed(state):
    records = [record for record in state["records"] if record["name"] == ALIAS]
    rules = [(index, rule) for index, rule in enumerate((state["entry"] or {}).get("rules", []))
             if rule.get("ref") == REF or rule.get("expression") == EXPRESSION]
    require(len(records) <= 1 and len(rules) <= 1, "Ambiguous duplicate alias DNS or redirect rules")
    require(not records or records[0]["type"] in ("A", "AAAA", "CNAME"), "Conflicting alias DNS record type")
    return (records[0] if records else None), (rules[0] if rules else None)


def unrelated(state):
    return {"records": sorted([clean(record) for record in state["records"] if record["name"] != ALIAS],
                               key=lambda record: record["id"]),
            "rules": [clean(rule) for rule in (state["entry"] or {}).get("rules", [])
                      if rule.get("ref") != REF and rule.get("expression") != EXPRESSION]}


def save(path, data):
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8", newline="\n") as output:
        if os.name != "nt":
            os.chmod(temporary, 0o600)
        json.dump(data, output, indent=2)
        output.write("\n")
    os.replace(str(temporary), str(path))


def apply(api, directory):
    before = snapshot(api)
    record, indexed_rule = managed(before)
    directory.mkdir(parents=True, exist_ok=True)
    receipt = directory / (datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex + ".json")
    data = {"schema": 1, "before": before, "operations": []}
    save(receipt, data)
    prefix = "zones/%s/" % before["zone"]

    def remember(kind, old, new, **extra):
        data["operations"].append(dict(kind=kind, before=old, after=new, **extra))
        save(receipt, data)

    desired = desired_rule()
    if before["entry"] is None:
        entry = api.request("POST", prefix + "rulesets", {"name": "Canonical brand alias", "kind": "zone",
                            "phase": PHASE, "rules": [desired]})
        rule = next(item for item in entry["rules"] if item.get("ref") == REF)
        remember("ruleset-create", None, rule, ruleset=entry["id"])
    else:
        entry = before["entry"]
        if indexed_rule is None:
            result = api.request("POST", prefix + "rulesets/%s/rules" % entry["id"],
                                 dict(desired, position={"index": 1}))
            rule = next(item for item in result["rules"] if item.get("ref") == REF)
            remember("rule-create", None, rule, ruleset=entry["id"])
        else:
            index, old = indexed_rule
            if index != 0 or any(old.get(key) != value for key, value in desired.items()):
                result = api.request("PATCH", prefix + "rulesets/%s/rules/%s" % (entry["id"], old["id"]),
                                     dict(rule_payload(old), **desired, position={"index": 1}))
                rule = next(item for item in result["rules"] if item.get("ref") == REF)
                remember("rule-update", old, rule, ruleset=entry["id"], position=index + 1)
    wanted = dict(dns_payload(record) if record else {}, type="A", name=ALIAS,
                  content="192.0.2.1", ttl=1, proxied=True)
    if record is None:
        result = api.request("POST", prefix + "dns_records", wanted)
        remember("dns-create", None, result)
    elif any(record.get(key) != value for key, value in wanted.items()):
        result = api.request("PATCH", prefix + "dns_records/%s" % record["id"], wanted)
        remember("dns-update", record, result)
    after = snapshot(api)
    require(unrelated(before) == unrelated(after), "Unrelated DNS or redirect configuration changed")
    final_record, final_rule = managed(after)
    require(final_record is not None and all(final_record.get(key) == wanted[key]
                                           for key in ("name", "type", "content", "ttl", "proxied")),
            "Alias DNS readback differs")
    require(final_rule is not None and final_rule[0] == 0 and
            all(final_rule[1].get(key) == value for key, value in desired.items()), "Alias redirect readback differs")
    data["after"] = after
    save(receipt, data)
    return {"host": ALIAS, "changes": len(data["operations"]), "unrelated_unchanged": True, "receipt": str(receipt)}


def rollback(api, receipt):
    data = json.loads(receipt.read_text(encoding="utf-8"))
    require(data.get("schema") == 1 and not data.get("rolled_back"), "Invalid or already rolled-back receipt")
    current = snapshot(api)
    require(current["zone"] == data["before"]["zone"], "Receipt zone differs")
    expected_state = copy.deepcopy(data["before"])
    for operation in data["operations"]:
        kind, new = operation["kind"], operation["after"]
        require(kind in ("dns-create", "dns-update", "rule-create", "rule-update", "ruleset-create"),
                "Unknown receipt operation")
        if kind.startswith("dns-"):
            expected_state["records"] = [item for item in expected_state["records"] if item["id"] != new["id"]] + [new]
        else:
            if expected_state["entry"] is None:
                expected_state["entry"] = {"id": operation["ruleset"], "phase": PHASE, "kind": "zone", "rules": []}
            expected_state["entry"]["rules"] = [new] + [item for item in expected_state["entry"]["rules"]
                                                        if item["id"] != new["id"]]

    def signature(state):
        record, rule = managed(state)
        return (clean(record) if record else None, (rule[0], clean(rule[1])) if rule else None)

    require(signature(current) == signature(data.get("after", expected_state)),
            "Managed object or rule-position drift prevents rollback")
    # Validate every managed object before reversing any write, including tampered receipts.
    for operation in data["operations"]:
        expected = operation["after"]
        if operation["kind"].startswith("dns-"):
            require(expected.get("name") == ALIAS, "Receipt DNS is outside the alias")
            require(operation["before"] is None or operation["before"].get("name") == ALIAS,
                    "Receipt DNS baseline is outside the alias")
            actual = next((item for item in current["records"] if item["id"] == expected["id"]), None)
        else:
            require(operation["kind"] in ("rule-create", "rule-update", "ruleset-create") and
                    expected.get("ref") == REF and expected.get("expression") == EXPRESSION,
                    "Receipt rule is outside the alias")
            require(current["entry"] and current["entry"]["id"] == operation["ruleset"], "Ruleset identity changed")
            actual = next((item for item in current["entry"]["rules"] if item["id"] == expected["id"]), None)
        require(actual is not None and clean(actual) == clean(expected), "Managed object drift prevents rollback")
    prefix = "zones/%s/" % current["zone"]
    for operation in reversed(data["operations"]):
        kind, old, new = operation["kind"], operation["before"], operation["after"]
        if kind.startswith("dns-"):
            path = prefix + "dns_records/%s" % new["id"]
            api.request("DELETE" if old is None else "PATCH", path, None if old is None else dns_payload(old))
        else:
            path = prefix + "rulesets/%s" % operation["ruleset"]
            if kind == "ruleset-create" and len(snapshot(api)["entry"]["rules"]) == 1:
                api.request("DELETE", path)
            else:
                path += "/rules/%s" % new["id"]
                api.request("DELETE" if old is None else "PATCH", path,
                            None if old is None else dict(rule_payload(old), position={"index": operation["position"]}))
    after = snapshot(api)
    require(unrelated(current) == unrelated(after), "Rollback changed unrelated configuration")
    require(signature(after) == signature(data["before"]), "Rollback alias readback differs from baseline")
    data["rolled_back"] = after
    save(receipt, data)
    return {"host": ALIAS, "changes": len(data["operations"]), "unrelated_unchanged": True, "rolled_back": True}


def probe(url):
    parsed = urllib.parse.urlsplit(url)
    require(parsed.hostname in (ALIAS, CANONICAL) and parsed.scheme in ("http", "https"), "Unexpected verification host")
    connection = (http.client.HTTPSConnection(parsed.hostname, timeout=30, context=ssl.create_default_context())
                  if parsed.scheme == "https" else http.client.HTTPConnection(parsed.hostname, timeout=30))
    try:
        connection.request("GET", parsed.path + ("?" + parsed.query if parsed.query else ""),
                           headers={"User-Agent": "S075-alias-verification"})
        response = connection.getresponse()
        return response.status, response.getheader("Location")
    finally:
        connection.close()


def verify(request=probe):
    paths = ("/", "/?source=s075&empty=&value=a%2Bb", "/docs/references/",
             "/docs/references/?source=s075&value=a%2Bb&repeat=1&repeat=2")
    results = []
    for scheme in ("http", "https"):
        for path in paths:
            source, expected = scheme + "://" + ALIAS + path, "https://" + CANONICAL + path
            status, destination = request(source)
            require(status == 301 and destination == expected, "Alias must preserve raw path/query in one canonical 301")
            target_status, target_location = request(destination)
            require(target_status == 200 and target_location is None, "Canonical destination must return 200 without another hop")
            results.append({"source": source, "status": status, "location": destination, "destination_status": target_status})
    return {"host": ALIAS, "cases": len(results), "tls_validation": "default certificate and hostname validation",
            "results": results}


def private_path(value):
    resolved = value.resolve()
    root = Path(__file__).resolve().parents[1]
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        return resolved
    require(relative.parts[:2] == ("dist", "private"), "Operational receipts inside the repository must stay under dist/private")
    return resolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    apply_parser = commands.add_parser("apply")
    apply_parser.add_argument("--state-dir", type=Path, required=True)
    rollback_parser = commands.add_parser("rollback")
    rollback_parser.add_argument("--receipt", type=Path, required=True)
    commands.add_parser("verify")
    args = parser.parse_args()
    if args.command == "verify":
        result = verify()
    elif args.command == "apply":
        result = apply(Cloudflare(token()), private_path(args.state_dir))
    else:
        result = rollback(Cloudflare(token()), private_path(args.receipt))
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (APIError, ValueError, RuntimeError, OSError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        sys.exit(1)
