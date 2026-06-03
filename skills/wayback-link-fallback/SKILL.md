---
name: wayback-link-fallback
description: Use when external documentation, API references, or web resources may be dead or unreliable and the agent should recover usable archived content through the Wayback Machine.
---

# Wayback Link Fallback

Use this skill when a task depends on an external web page, documentation URL, API
reference, blog post, release note, or other web resource that is unavailable,
redirecting unexpectedly, incomplete, or likely to have changed.

The goal is to recover enough source material to answer or implement accurately while
being explicit that the material came from an archived snapshot.

## Workflow

1. Try the original URL first.
   - Check whether the live page loads, whether it redirects, and whether the content
     still matches the caller's need.
   - If the live page works but the question depends on old behavior, still check an
     archived capture near the relevant date or version.
2. Look for archived captures.
   - Use the Wayback Machine page view for quick inspection:
     `https://web.archive.org/web/*/<original-url>`.
   - Use the CDX API when you need structured capture choices:
     `https://web.archive.org/cdx?url=<original-url>&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest`.
   - Prefer captures with HTTP 200, relevant MIME type, a stable digest, and a timestamp
     closest to the date or product version the task requires.
3. Fetch raw archived content.
   - Prefer the `id_` form to avoid the Wayback Toolbar and archive rewrite chrome:
     `https://web.archive.org/web/<timestamp>id_/<original-url>`.
   - If raw content is unavailable, use the normal archived page only for inspection and
     avoid copying Wayback UI text into findings, summaries, or code comments.
4. Work from the archived source carefully.
   - Record the original URL, archive URL, and capture timestamp in notes or citations.
   - State clearly when evidence comes from an archived snapshot.
   - Do not present archived content as current truth unless it is verified against a
     current primary source.

## Choosing Captures

Prefer captures that satisfy the task rather than simply the newest snapshot.

Good capture candidates:

- Match the relevant product, API, library, or documentation version.
- Have `statuscode` 200 in CDX metadata.
- Have an expected `mimetype`, such as `text/html`, `application/json`, `text/plain`,
  or a source file MIME type.
- Are near the date mentioned by the user, package release, commit, changelog, or API
  version being investigated.
- Avoid duplicate captures with the same digest unless the timestamp itself matters.

Avoid relying on captures that are login pages, soft 404 pages, consent screens,
unrelated redirects, generated error pages, or partial pages missing the relevant
content.

## Rate Limiting

Use the Wayback Machine politely. It is a shared public service.

- Make the smallest number of requests that can answer the task.
- Prefer one CDX query over manually opening many timestamped captures.
- Use `collapse=digest` for duplicate-heavy pages.
- Back off when responses are slow, empty, `429`, `503`, or otherwise unstable.
- Cache useful archive URLs and metadata in your working notes during the task instead
  of repeating the same lookup.
- Avoid broad crawls, wildcard-heavy queries, and asset enumeration unless the user
  specifically needs them.

If archive access is rate-limited or unstable, report that limitation and retry with a
narrower query, a later attempt, or a single known timestamp.

## Relative Links

Archived HTML and documentation often contains relative links that need careful
resolution.

When following or citing links found inside an archived page:

1. Resolve the link against the original page URL first, as a browser would have done
   when the page was live.
2. Look up or construct the corresponding archived URL for that resolved absolute URL.
3. Prefer the same capture timestamp when the linked page is part of the same docs set.
4. Use a nearby timestamp only if the same timestamp is missing or broken.

Examples:

- Original page: `https://example.com/docs/api/index.html`
- Relative link: `../auth/tokens.html`
- Resolved live URL: `https://example.com/docs/auth/tokens.html`
- Raw archived URL: `https://web.archive.org/web/<timestamp>id_/https://example.com/docs/auth/tokens.html`

For root-relative links such as `/docs/install`, resolve against the original origin:
`https://example.com/docs/install`.

For protocol-relative links such as `//cdn.example.com/file.js`, preserve the intended
scheme from the original page when possible, usually `https:`.

## Failure Modes

If no reliable archived source is available, say so directly.

Common failures:

- No capture exists for the original URL.
- Captures exist but are blocked, excluded, or unavailable.
- The only captures are errors, redirects, placeholders, login pages, or unrelated
  content.
- Required assets, scripts, OpenAPI specs, source files, or images were not archived.
- The archived version does not match the user's target API, docs version, package
  version, or date.
- Relative links resolve to pages without matching captures.

When this happens, try one narrower alternative before giving up: a versioned docs URL,
a source repository file, a package registry page, a release tag, an official mirror, or
a quoted URL from search results. Keep the fallback source clearly labeled.

## Reporting

When using archived material in an answer or implementation note, include:

- The original URL.
- The Wayback snapshot URL.
- The capture timestamp in `YYYYMMDDhhmmss` form, and a human-readable date when useful.
- Any uncertainty, such as missing assets, mismatched versions, or reliance on nearby
  captures.

For high-stakes, current, legal, medical, financial, or security-sensitive claims, use
archived content only as historical evidence and verify current state with live primary
sources.
