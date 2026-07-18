# Capture and link handling

## Locate captures

For quick inspection:

```text
https://web.archive.org/web/*/<original-url>
```

For structured selection:

```text
https://web.archive.org/cdx?url=<original-url>&output=json&fl=timestamp,original,statuscode,mimetype,digest&filter=statuscode:200&collapse=digest
```

Prefer a capture with status 200, the expected MIME type, a relevant timestamp, and a
stable digest. The newest capture is not automatically the correct one.

Fetch raw content when available:

```text
https://web.archive.org/web/<timestamp>id_/<original-url>
```

## Resolve links

Resolve relative links against the original live page first, then find or construct the
archive URL for the resulting absolute URL. Prefer the same capture timestamp for one docs
set and a nearby timestamp only when the matching snapshot is absent or broken.

- Resolve `../path` against the original page directory.
- Resolve `/path` against the original origin.
- Resolve `//host/path` with the original scheme, normally HTTPS.

Do not resolve links against Wayback toolbar URLs or cite archive chrome as source content.

## Reject misleading captures

Reject errors, redirects to unrelated pages, login or consent pages, placeholders, soft
404s, wrong versions, and documents missing the material needed for the claim. A successful
HTTP status alone does not establish relevance or completeness.
