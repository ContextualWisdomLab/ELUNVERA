"""Apply the final reviewed ELUNVERA contract corrections and remove this repair path.

This file is intentionally one-shot.  The workflow that invokes it removes both
this script and every temporary repair workflow before the resulting commit is
created, so the durable branch contains only product documentation, contracts,
and their permanent exact-head validation workflow.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(".")
OPENAPI_PATH = ROOT / "schemas/openapi.yaml"
VALIDATION_PATH = ROOT / "docs/VALIDATION_REPORT.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
PERMANENT_WORKFLOW_PATH = ROOT / ".github/workflows/document-contracts.yml"
MANIFEST_PATH = ROOT / "manifest.json"

PERMANENT_WORKFLOW = r"""name: document and contract checks

on:
  pull_request:
    branches:
      - develop
  push:
    branches:
      - develop
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: elunvera-document-contracts-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  validate:
    name: validate documentation and contracts
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Check out exact revision
        uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # actions/checkout@v7
        with:
          fetch-depth: 0

      - name: Reject temporary repair artifacts
        shell: bash
        run: |
          set -euo pipefail
          test ! -e .github/workflows/repair-review-round-3.yml
          test ! -e .github/workflows/repair-review-round-4.yml
          test ! -e .github/workflows/repair-review-round-5.yml
          test ! -e tools/repair_contract_review_round5.py

      - name: Parse and validate YAML contracts
        shell: bash
        run: |
          set -euo pipefail
          ruby -ryaml - <<'RUBY'
          openapi = YAML.safe_load(File.read('schemas/openapi.yaml'), aliases: false)
          raise 'OpenAPI version mismatch' unless openapi.fetch('openapi') == '3.2.0'

          operations = []
          openapi.fetch('paths').each do |path, item|
            item.each do |method, operation|
              next unless %w[get post put patch delete head options trace].include?(method)
              operations << [path, operation.fetch('operationId')]
            end
          end
          raise 'duplicate operationId' unless operations.map(&:last).uniq.length == operations.length

          parameters = openapi.fetch('components').fetch('parameters')
          %w[ValidAt RecordedAt KnowledgeCutoff].each do |name|
            raise "missing temporal parameter #{name}" unless parameters.key?(name)
          end

          relationship = openapi.fetch('components').fetch('schemas').fetch('RecordRelationshipRequest')
          truth_statuses = relationship.fetch('properties').fetch('truth_status').fetch('enum')
          raise 'P0 manual relationship command must not accept inferred truth' if truth_statuses.include?('inferred')
          evidence = relationship.fetch('properties').fetch('evidence_reference_ids')
          raise 'evidence_reference_ids must reject empty arrays' unless evidence.fetch('minItems').to_i >= 1

          asyncapi = YAML.safe_load(File.read('schemas/asyncapi.yaml'), aliases: false)
          raise 'AsyncAPI version mismatch' unless asyncapi.fetch('asyncapi') == '3.1.0'
          asyncapi.fetch('operations').each do |name, operation|
            raise "#{name} must describe ELUNVERA as producer" unless operation.fetch('action') == 'send'
          end
          envelope = asyncapi.fetch('components').fetch('schemas').fetch('CloudEventEnvelope')
          required = envelope.fetch('required')
          raise 'provenance extension must be required' unless required.include?('provenanceref')
          raise 'classification extension must be required' unless required.any? { |field| %w[dataclassification data_classification].include?(field) }
          raise 'schema revision extension must be required' unless required.any? { |field| %w[schemarevision schema_revision].include?(field) }
          RUBY

      - name: Validate manifest, JSON schemas, and durable evidence
        shell: bash
        run: |
          set -euo pipefail
          python3 <<'PY'
          import hashlib
          import json
          import re
          import subprocess
          from pathlib import Path

          manifest_path = Path('manifest.json')
          manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
          entries = {entry['path']: entry for entry in manifest['files']}
          tracked = set(subprocess.check_output(['git', 'ls-files'], text=True).splitlines())
          tracked_without_manifest = tracked - {'manifest.json'}

          assert len(tracked) == 56, len(tracked)
          assert manifest['file_count'] == len(entries) == 55
          assert set(entries) == tracked_without_manifest
          for path_text, entry in entries.items():
              payload = Path(path_text).read_bytes()
              assert hashlib.sha256(payload).hexdigest() == entry['sha256'], path_text
              assert len(payload) == entry['size_bytes'], path_text
              assert len(payload.decode('utf-8').splitlines()) == entry['line_count'], path_text

          for event_path in sorted(Path('schemas/events').glob('*.json')):
              schema = json.loads(event_path.read_text(encoding='utf-8'))
              assert schema['$schema'] == 'https://json-schema.org/draft/2020-12/schema'
              assert schema['additionalProperties'] is False
          relationship_event = json.loads(Path('schemas/events/relationship-changed-v1.schema.json').read_text(encoding='utf-8'))
          assert 'recorded_at' in relationship_event['required']

          report = Path('docs/VALIDATION_REPORT.md').read_text(encoding='utf-8')
          assert '- Tracked repository files including `manifest.json`: **56**' in report
          assert '- Manifest entries excluding `manifest.json`: **55**' in report
          assert 'Draft 2020-12 declaration and structural invariant validation' in report
          assert 'metaschema validation' not in report.lower()

          placeholder = re.compile(r'\b(?:TBD|TODO|FIXME)\b')
          for path in tracked_without_manifest:
              if path.endswith(('.md', '.yaml', '.yml', '.json')):
                  text = Path(path).read_text(encoding='utf-8')
                  assert not placeholder.search(text), path
          PY

      - name: Validate Markdown links and fences
        shell: bash
        run: |
          set -euo pipefail
          python3 <<'PY'
          import re
          from pathlib import Path

          link_pattern = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
          for path in Path('.').rglob('*.md'):
              if '.git' in path.parts:
                  continue
              text = path.read_text(encoding='utf-8')
              assert text.count('```') % 2 == 0, f'unbalanced code fence: {path}'
              for target in link_pattern.findall(text):
                  target = target.strip().split()[0].strip('<>')
                  if not target or target.startswith(('#', 'http://', 'https://', 'mailto:')):
                      continue
                  local = target.split('#', 1)[0]
                  if local:
                      assert (path.parent / local).resolve().exists(), f'broken link: {path} -> {target}'
          PY

      - name: Reject whitespace errors
        shell: bash
        run: git diff --check HEAD^
"""


def repair_openapi() -> None:
    text = OPENAPI_PATH.read_text(encoding="utf-8")
    start = text.index("    RecordRelationshipRequest:\n")
    end = text.index("    StageTransitionRequest:\n", start)
    block = text[start:end]

    block = re.sub(r"(?m)^          - inferred\n", "", block)
    evidence_header = "        evidence_reference_ids:\n          type: array\n"
    if "        evidence_reference_ids:\n          type: array\n          minItems:" not in block:
        if evidence_header not in block:
            raise RuntimeError("RecordRelationshipRequest evidence array not found")
        block = block.replace(evidence_header, evidence_header + "          minItems: 1\n", 1)

    if "          - inferred\n" in block:
        raise RuntimeError("inferred truth remains in the P0 manual relationship command")
    if "          minItems: 1\n" not in block:
        raise RuntimeError("relationship evidence arrays still accept empty input")

    OPENAPI_PATH.write_text(text[:start] + block + text[end:], encoding="utf-8")


def repair_validation_report() -> None:
    text = VALIDATION_PATH.read_text(encoding="utf-8")
    text = re.sub(r"- \*\*Validation date:\*\* \d{4}-\d{2}-\d{2}", "- **Validation date:** 2026-08-29", text, count=1)
    text = text.replace(
        "JSON Schema Draft 2020-12 metaschema validation",
        "JSON Schema Draft 2020-12 declaration and structural invariant validation",
    )
    text = text.replace(
        "Python JSON and JSON Schema validation",
        "Python JSON parsing and Draft 2020-12 declaration/invariant validation",
    )
    text = re.sub(
        r"- Repository files excluding `\.git`: \*\*\d+\*\*",
        "- Tracked repository files including `manifest.json`: **56**",
        text,
    )
    text = re.sub(
        r"- Manifest entries excluding `manifest\.json`: \*\*\d+\*\*",
        "- Manifest entries excluding `manifest.json`: **55**",
        text,
    )
    if "metaschema validation" in text.lower():
        raise RuntimeError("validation report still overstates metaschema validation")
    required = (
        "- Tracked repository files including `manifest.json`: **56**",
        "- Manifest entries excluding `manifest.json`: **55**",
        "Draft 2020-12 declaration and structural invariant validation",
    )
    for value in required:
        if value not in text:
            raise RuntimeError(f"validation report repair missing: {value}")
    VALIDATION_PATH.write_text(text, encoding="utf-8")


def repair_changelog() -> None:
    text = CHANGELOG_PATH.read_text(encoding="utf-8")
    bullets = (
        "- Restricted the P0 manual relationship command from accepting `inferred` truth without inference provenance and confidence.",
        "- Required at least one evidence reference when a relationship command chooses the evidence-backed assertion path.",
        "- Corrected documentation inventory counts and aligned validation claims with the permanent exact-head workflow.",
    )
    missing = [bullet for bullet in bullets if bullet not in text]
    if missing:
        marker = "## [Unreleased]"
        if marker not in text:
            marker = "## Unreleased"
        if marker in text:
            insertion = text.index("\n", text.index(marker)) + 1
            text = text[:insertion] + "\n### Fixed\n\n" + "\n".join(missing) + "\n" + text[insertion:]
        else:
            text += "\n## Unreleased\n\n### Fixed\n\n" + "\n".join(missing) + "\n"
    CHANGELOG_PATH.write_text(text, encoding="utf-8")


def remove_temporary_artifacts() -> None:
    for path_text in (
        ".github/workflows/repair-review-round-3.yml",
        ".github/workflows/repair-review-round-4.yml",
        ".github/workflows/repair-review-round-5.yml",
        "tools/repair_contract_review_round5.py",
    ):
        path = ROOT / path_text
        if path.exists():
            path.unlink()


def refresh_manifest() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries: list[dict[str, object]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path == MANIFEST_PATH:
            continue
        payload = path.read_bytes()
        entries.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
                "line_count": len(payload.decode("utf-8").splitlines()),
            }
        )
    if len(entries) != 55:
        raise RuntimeError(f"expected 55 manifest entries after cleanup, found {len(entries)}")
    manifest["generated_at"] = "2026-08-29T00:00:00Z"
    manifest["file_count"] = len(entries)
    manifest["files"] = entries
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate_final_tree() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    if len(files) != 56:
        raise RuntimeError(f"expected 56 final files including manifest, found {len(files)}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    entries = {entry["path"]: entry for entry in manifest["files"]}
    if manifest["file_count"] != len(entries) or len(entries) != 55:
        raise RuntimeError("manifest inventory count mismatch")
    for path_text, entry in entries.items():
        payload = Path(path_text).read_bytes()
        if hashlib.sha256(payload).hexdigest() != entry["sha256"]:
            raise RuntimeError(f"manifest hash mismatch: {path_text}")
        if len(payload) != entry["size_bytes"]:
            raise RuntimeError(f"manifest size mismatch: {path_text}")
        if len(payload.decode("utf-8").splitlines()) != entry["line_count"]:
            raise RuntimeError(f"manifest line-count mismatch: {path_text}")

    for path in sorted((ROOT / "schemas/events").glob("*.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise RuntimeError(f"schema declaration mismatch: {path}")
        if schema.get("additionalProperties") is not False:
            raise RuntimeError(f"schema must close unknown fields: {path}")


def main() -> None:
    repair_openapi()
    repair_validation_report()
    repair_changelog()
    PERMANENT_WORKFLOW_PATH.write_text(PERMANENT_WORKFLOW, encoding="utf-8")
    remove_temporary_artifacts()
    refresh_manifest()
    validate_final_tree()


if __name__ == "__main__":
    main()
