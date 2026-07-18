---
name: wayback-link-fallback
description: Use when a task depends on a dead, redirected, incomplete, version-specific, or historically changed web page and archived evidence from the Wayback Machine may recover the required source.
---

# Wayback Link Fallback

Recover the smallest reliable archived source needed for the task and label it as
historical evidence.

## Workflow

1. Try the original URL and determine whether the live content still answers the question.
2. If historical or unavailable content is needed, query captures for the exact original
   URL. Prefer one narrow CDX query over manually opening many snapshots.
3. Select a successful capture that matches the relevant date, product version, and MIME
   type; avoid login pages, soft 404s, consent screens, and unrelated redirects.
4. Fetch raw archived content with the `id_` form when possible to avoid archive UI and URL
   rewriting.
5. Record the original URL, snapshot URL, capture timestamp, and any version or completeness
   uncertainty.
6. Verify current claims against a live primary source. Never present an archive snapshot
   as current truth merely because it was retrievable.

For CDX parameters, capture selection details, and relative-link resolution, read
[capture and link handling](references/captures-and-links.md).

## Request discipline

- Make the fewest requests that can answer the task.
- Collapse duplicate digests in capture-heavy results.
- Back off on slow, empty, `429`, or `503` responses.
- Cache useful timestamps and URLs in task-local notes instead of repeating requests.
- Avoid broad wildcard crawls or asset enumeration unless explicitly required.

## Failure handling

If no reliable capture exists, try one narrower primary alternative: versioned official
docs, a tagged source file, package registry, release page, official mirror, or repository
history. Keep fallback provenance explicit.

Report failure rather than relying on captures that are blocked, partial, mismatched to the
target version, or missing required scripts, assets, schemas, or linked pages.

For legal, medical, financial, security-sensitive, or other high-stakes current claims,
use archived content only as historical evidence and verify the present state with live
authoritative sources.

## Expected output

Include the original URL, archive URL, capture timestamp (`YYYYMMDDhhmmss`), relevant human
date, why that capture was chosen, and all material uncertainty.
