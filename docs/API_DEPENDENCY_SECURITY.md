# FastAPI dependency security audit

Audited 2026-10-04 on Python 3.12.14, starting from main
`675e27c8fe226bb4c82784060f270bb45e38c27b`. This change is separate
from the Flask work in draft PR #36. Both Flask manifests and application
implementations are unchanged.

## Resolution and selected versions

| Package | Original resolution | Selected resolution | Reason |
| --- | --- | --- | --- |
| FastAPI | 0.104.1 | 0.142.2 | Removes old Starlette/AnyIO restrictions and the reported FastAPI advisory |
| Starlette | 0.27.0 | 1.7.0 | Includes current URL, dispatch, static-file and form-parser fixes |
| AnyIO | 3.7.1 | 4.15.1 | Includes fixes released in 4.14.2 |
| Uvicorn | 0.24.0.post1 | 0.54.0 | Current compatible ASGI server; not reported vulnerable in this audit |
| HTTPX | 0.25.2 | 0.28.1 | Compatible maintained client; not reported vulnerable in this audit |
| HTTPcore | 1.0.9 | 1.0.9 | Resolves from HTTPX's 1.x constraint and requires h11 >=0.16 |
| h11 | 0.16.0 | 0.16.0 | Explicitly retain the patched HTTP parser rather than Uvicorn's permissive minimum |
| Pydantic | 2.13.5 | 2.13.5 | Existing models work with the new FastAPI Pydantic 2 requirement |

FastAPI 0.142.2 accepts Starlette >=0.46.0 and Pydantic >=2.9.0;
Starlette 1.7.0 requires AnyIO >=4,<5. HTTPX 0.28.1 works with the
upgraded TestClient. Starlette and AnyIO are explicitly pinned so an
older vulnerable version cannot satisfy a fresh install. These versions
require Python 3.10+, now documented in the installation instructions.
Only Python 3.12.14 was exercised here.

The two adjacent JSON audit snapshots record the complete resolved root
manifest closure, including console dependencies: 22 packages before,
23 after. They retain advisory identifiers and fixed versions, deduplicated
by GHSA, rather than repeating upstream advisory descriptions. Other
transitive versions remain resolver-selected; these snapshots are audit
evidence, not complete lock files.

## Advisories and applicability

The original closure reports ten distinct package advisories:

| Package | Advisory | First fixed version |
| --- | --- | --- |
| FastAPI | GHSA-qf9m-vfgh-m389 | 0.109.1 |
| AnyIO | GHSA-82r6-8w77-94w6 | 4.14.2 |
| AnyIO | GHSA-5p39-cfhj-2xmp | 4.14.2 |
| Starlette | GHSA-f96h-pmfr-66vw | 0.40.0 |
| Starlette | GHSA-2c2j-9gv5-cj73 | 0.47.2 |
| Starlette | GHSA-86qp-5c8j-p5mr | 1.0.1 |
| Starlette | GHSA-wqp7-x3pw-xc5r | 1.1.0 |
| Starlette | GHSA-x746-7m8f-x49c | 1.1.0 |
| Starlette | GHSA-jp82-jpqv-5vv3 | 1.3.0 |
| Starlette | GHSA-82w8-qh3p-5jfq | 1.3.1 |

The current `service.py` and `api.py` endpoints use JSON models and
synchronous handlers. They do not register multipart/form routes,
StaticFiles, HTTPEndpoint subclasses, AnyIO process workers, or outbound
TLS calls. Thus these package findings are not proof that each exploit is
reachable through the present endpoints. The upgrades remove vulnerable
components and protect future uses. No authentication, input-validation,
or game-business-rule changes are included.

h11's GHSA-vqfr-h8mv-ghfj is fixed by 0.16.0. A fresh original resolution
already selects that version through HTTPcore 1.0.9, so it is not a finding
against this baseline. An older installed environment could differ.

## Verification

- Updated `requirements.txt` installs; `pip check` passes.
- `pip-audit -r requirements.txt`: 23 resolved packages, no known
  vulnerabilities reported. This result applies to this manifest only.
- Eight new regression cases pass on both original and upgraded stacks.
  They exercise service travel/trade state, typed validation without state
  mutation, malformed JSON, 404/405 routing, session-header authentication,
  session isolation, and OpenAPI/docs for both entry points.
- The three existing `tests/test_api_service.py` cases also pass.
- Real local Uvicorn HTTP smoke passes for `service:app` status and
  `api:app` session creation followed by authenticated status.
- With the new tests present in both environments,
  `pytest --continue-on-collection-errors -q` produces the same
  **171 passed, 3 skipped, 8 failed, 12 errors**. This is 163 passes plus
  the eight new cases. Failure/error node lists match.
- `git diff --check` passes.

Baseline failures remain outside scope: six API tests expect 400/422 where
the current service returns 200 with a failure flag or accepts zero/negative
quantities; one combat assertion and one placeholder web UI assertion fail.
Collection of world-generation tests fails on the missing `SectorDB`
import; eleven combat setup errors involve existing missing/invalid fixtures.
Normal full-suite execution stops at the collection error.

The upgraded Starlette TestClient emits a deprecation warning recommending
HTTPX2. HTTPX 0.28.1 remains supported by this version; adopting HTTPX2 is
deferred to avoid an additional client migration. The pre-existing test
using `data=` for raw JSON also emits an HTTPX deprecation warning.

Reproduce in an isolated environment:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt pytest==9.0.3 pip-audit==2.10.1
.venv/bin/pip check
.venv/bin/pip-audit -r requirements.txt
.venv/bin/python -m pytest tests/test_api_stack_regression.py tests/test_api_service.py -q
.venv/bin/python -m pytest --continue-on-collection-errors -q
```

## Primary references

- https://github.com/fastapi/fastapi/releases/tag/0.142.2
- https://github.com/fastapi/fastapi/security/advisories/GHSA-qf9m-vfgh-m389
- https://github.com/Kludex/starlette/releases/tag/1.7.0
- https://github.com/Kludex/starlette/security/advisories
- https://github.com/agronholm/anyio/security/advisories/GHSA-82r6-8w77-94w6
- https://github.com/agronholm/anyio/security/advisories/GHSA-5p39-cfhj-2xmp
- https://github.com/encode/httpx/releases/tag/0.28.1
- https://github.com/python-hyper/h11/security/advisories/GHSA-vqfr-h8mv-ghfj
