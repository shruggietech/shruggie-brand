"""Isolated regressions for the exact-host alias reconciler."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.parse

SPEC = importlib.util.spec_from_file_location("alias", Path(__file__).with_name("cloudflare_alias.py"))
alias = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(alias)


class FakeAPI:
    def __init__(self, missing=False):
        self.records = [{"id": "1" * 32, "name": alias.CANONICAL, "type": "CNAME",
                         "content": "shruggietech.github.io", "proxied": True, "ttl": 1,
                         "comment": "Keep canonical", "tags": []}]
        self.entry = None if missing else {"id": "2" * 32, "phase": alias.PHASE, "kind": "zone",
                                          "rules": [{"id": "3" * 32, "ref": "other", "enabled": True,
                                                     "action": "redirect", "expression": '(http.host eq "graph.shruggie.tech")',
                                                     "action_parameters": {"from_value": {"status_code": 301,
                                                          "target_url": {"value": "https://shruggie.tech"}}}}]}
        self.writes = []
        self.deny = False
        self.counter = 10
        self.bump_metadata = False

    def request(self, method, path, body=None, missing=False):
        parsed = urllib.parse.urlsplit(path)
        bits = parsed.path.split("/")
        if self.deny and "rulesets" in bits:
            raise alias.APIError(403, [10000])
        if method == "GET":
            if bits == ["zones"]:
                return [{"id": "a" * 32, "name": alias.ZONE, "status": "active"}]
            if bits[-1] == "dns_records":
                return copy.deepcopy(self.records)
            if bits[-1] == "entrypoint":
                return copy.deepcopy(self.entry)
            raise AssertionError(path)
        self.writes.append((method, path, copy.deepcopy(body)))
        self.counter += 1
        new_id = format(self.counter, "032x")
        if "dns_records" in bits:
            if method == "POST":
                result = dict(body, id=new_id)
                self.records.append(result)
            elif method == "PATCH":
                result = next(r for r in self.records if r["id"] == bits[-1])
                result.update(body)
                if self.bump_metadata:
                    result["modified_on"] = "change-%d" % self.counter
            else:
                self.records = [r for r in self.records if r["id"] != bits[-1]]
                result = {}
            return copy.deepcopy(result)
        if bits[-1] == "rulesets" and method == "POST":
            self.entry = dict(body, id=new_id)
            self.entry["rules"][0]["id"] = "b" * 32
        elif "rules" in bits:
            if method == "DELETE":
                self.entry["rules"] = [r for r in self.entry["rules"] if r["id"] != bits[-1]]
            else:
                rule = dict(body)
                position = rule.pop("position", None)
                rule["id"] = new_id if method == "POST" else bits[-1]
                if self.bump_metadata:
                    rule.update(version=str(self.counter), last_updated="change-%d" % self.counter)
                self.entry["rules"] = [r for r in self.entry["rules"] if r["id"] != rule["id"]]
                self.entry["rules"].insert((position or {}).get("index", 1) - 1, rule)
        elif method == "DELETE":
            self.entry = None
        return copy.deepcopy(self.entry)


class AliasTests(unittest.TestCase):
    def test_create_noop_and_rollback_preserve_canonical_and_existing_rules(self):
        api = FakeAPI()
        baseline = copy.deepcopy((api.records, api.entry))
        with tempfile.TemporaryDirectory() as temporary:
            applied = alias.apply(api, Path(temporary))
            self.assertEqual(applied["changes"], 2)
            record = next(r for r in api.records if r["name"] == alias.ALIAS)
            self.assertEqual((record["type"], record["content"], record["ttl"], record["proxied"]),
                             ("A", "192.0.2.1", 1, True))
            rule = api.entry["rules"][0]
            self.assertEqual(rule["expression"], '(http.host eq "brands.shruggie.tech")')
            self.assertEqual(rule["action_parameters"]["from_value"], {
                "status_code": 301, "preserve_query_string": True,
                "target_url": {"expression": 'concat("https://brand.shruggie.tech", http.request.uri.path)'}})
            writes = len(api.writes)
            self.assertEqual(alias.apply(api, Path(temporary))["changes"], 0)
            self.assertEqual(len(api.writes), writes)
            self.assertEqual(alias.rollback(api, Path(applied["receipt"]))["changes"], 2)
            self.assertEqual((api.records, api.entry), baseline)
            self.assertEqual(alias.apply(api, Path(temporary))["changes"], 2)

    def test_existing_alias_metadata_and_rule_position_restore(self):
        api = FakeAPI()
        api.records.append({"id": "4" * 32, "name": alias.ALIAS, "type": "CNAME", "content": "old.example",
                            "proxied": False, "ttl": 300, "comment": "Keep me", "tags": ["owner:test"]})
        api.entry["rules"].append(dict(alias.desired_rule(), id="5" * 32, enabled=False))
        baseline = copy.deepcopy((api.records, api.entry))
        with tempfile.TemporaryDirectory() as temporary:
            receipt = alias.apply(api, Path(temporary))["receipt"]
            self.assertEqual(api.records[-1]["comment"], "Keep me")
            self.assertEqual(api.records[-1]["tags"], ["owner:test"])
            alias.rollback(api, Path(receipt))
            self.assertEqual((api.records, api.entry), baseline)

    def test_missing_entrypoint_is_created_and_scoped_rollback_preserves_new_other_rule(self):
        api = FakeAPI(missing=True)
        with tempfile.TemporaryDirectory() as temporary:
            receipt = alias.apply(api, Path(temporary))["receipt"]
            api.entry["rules"].append({"id": "6" * 32, "ref": "later-other", "expression": "true"})
            alias.rollback(api, Path(receipt))
            self.assertEqual(len(api.entry["rules"]), 1)
            self.assertEqual(api.entry["rules"][0]["ref"], "later-other")

    def test_new_empty_entrypoint_is_removed_on_rollback(self):
        api = FakeAPI(missing=True)
        with tempfile.TemporaryDirectory() as temporary:
            receipt = alias.apply(api, Path(temporary))["receipt"]
            alias.rollback(api, Path(receipt))
            self.assertIsNone(api.entry)

    def test_denied_inspection_never_creates_objects(self):
        api = FakeAPI()
        api.deny = True
        with tempfile.TemporaryDirectory() as temporary, self.assertRaises(alias.APIError):
            alias.apply(api, Path(temporary))
        self.assertEqual(api.writes, [])

    def test_ambiguous_dns_or_managed_rules_fail_before_writes(self):
        for duplicate in ("dns", "rule"):
            api = FakeAPI()
            if duplicate == "dns":
                api.records.extend([dict(api.records[0], name=alias.ALIAS), dict(api.records[0], name=alias.ALIAS)])
            else:
                api.entry["rules"].extend([dict(alias.desired_rule(), id="7" * 32), dict(alias.desired_rule(), id="8" * 32)])
            with tempfile.TemporaryDirectory() as temporary, self.assertRaises(ValueError):
                alias.apply(api, Path(temporary))
            self.assertEqual(api.writes, [])

    def test_rollback_checks_all_managed_objects_before_any_write(self):
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as temporary:
            receipt = alias.apply(api, Path(temporary))["receipt"]
            api.entry["rules"][0]["expression"] = "true"
            writes = len(api.writes)
            with self.assertRaises(ValueError):
                alias.rollback(api, Path(receipt))
            self.assertEqual(len(api.writes), writes)

    def test_tampered_receipt_cannot_delete_canonical_record(self):
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(alias.apply(api, Path(temporary))["receipt"])
            data = json.loads(receipt.read_text(encoding="utf-8"))
            data["operations"][-1]["after"] = copy.deepcopy(api.records[0])
            receipt.write_text(json.dumps(data), encoding="utf-8")
            writes = len(api.writes)
            with self.assertRaises(ValueError):
                alias.rollback(api, receipt)
            self.assertEqual(len(api.writes), writes)

    def test_partial_receipt_can_reverse_known_writes(self):
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(alias.apply(api, Path(temporary))["receipt"])
            data = json.loads(receipt.read_text(encoding="utf-8"))
            del data["after"]
            receipt.write_text(json.dumps(data), encoding="utf-8")
            alias.rollback(api, receipt)
            self.assertFalse(any(r["name"] == alias.ALIAS for r in api.records))
            self.assertEqual(len(api.entry["rules"]), 1)

    def test_rollback_detects_rule_position_drift_before_writes(self):
        api = FakeAPI()
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(alias.apply(api, Path(temporary))["receipt"])
            api.entry["rules"].reverse()
            writes = len(api.writes)
            with self.assertRaises(ValueError):
                alias.rollback(api, receipt)
            self.assertEqual(len(api.writes), writes)

    def test_existing_object_restoration_ignores_new_server_timestamps_and_versions(self):
        api = FakeAPI()
        api.bump_metadata = True
        api.records.append({"id": "4" * 32, "name": alias.ALIAS, "type": "CNAME", "content": "old.example",
                            "proxied": False, "ttl": 300, "modified_on": "initial"})
        api.entry["rules"].append(dict(alias.desired_rule(), id="5" * 32, enabled=False,
                                       version="1", last_updated="initial"))
        original_record, original_rule = copy.deepcopy(alias.managed(alias.snapshot(api)))
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(alias.apply(api, Path(temporary))["receipt"])
            alias.rollback(api, receipt)
            restored_record, restored_rule = alias.managed(alias.snapshot(api))
            self.assertEqual(alias.clean(restored_record), alias.clean(original_record))
            self.assertEqual(restored_rule[0], original_rule[0])
            self.assertEqual(alias.clean(restored_rule[1]), alias.clean(original_rule[1]))
            self.assertNotEqual(restored_record["modified_on"], original_record["modified_on"])
            self.assertNotEqual(restored_rule[1]["version"], original_rule[1]["version"])
            self.assertTrue(json.loads(receipt.read_text(encoding="utf-8"))["rolled_back"])

    def test_api_errors_redact_raw_body_and_redirects_are_not_followed(self):
        error = urllib.error.HTTPError("https://api.cloudflare.com/", 403, "Denied", {},
                                       io.BytesIO(b'{"errors":[{"code":10000,"message":"SECRET_SENTINEL"}]}'))
        with mock.patch.object(alias.urllib.request, "build_opener") as factory:
            factory.return_value.open.side_effect = error
            with self.assertRaises(alias.APIError) as caught:
                alias.Cloudflare("SECRET_SENTINEL").request("GET", "zones")
            self.assertNotIn("SECRET_SENTINEL", str(caught.exception))
            self.assertTrue(any(isinstance(v, alias.NoRedirect) for v in factory.call_args.args))
        redirect = alias.NoRedirect().redirect_request(None, None, 302, "Found", {}, "https://other.example/")
        self.assertIsNone(redirect)

    def test_verification_requires_exact_raw_path_query_and_canonical_200(self):
        calls = []
        def probe(url):
            calls.append(url)
            if "brands.shruggie.tech" in url:
                return 301, url.replace("http://brands.shruggie.tech", "https://brand.shruggie.tech").replace(
                    "https://brands.shruggie.tech", "https://brand.shruggie.tech")
            return 200, None
        report = alias.verify(probe)
        self.assertEqual(report["cases"], 8)
        self.assertTrue(any("repeat=1&repeat=2" in url for url in calls))
        with self.assertRaises(ValueError):
            alias.verify(lambda url: (302, "https://brand.shruggie.tech/"))
        with self.assertRaises(ValueError):
            alias.verify(lambda url: (301, url.replace("brands.", "brand.")))


if __name__ == "__main__":
    unittest.main()
