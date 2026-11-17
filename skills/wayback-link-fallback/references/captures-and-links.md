# Capture lookup and replay

Browse `https://web.archive.org/web/*/<original-url>` or query the [Wayback CDX index](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server) for a specific date window:

```bash
curl --get 'https://web.archive.org/cdx/search/cdx' \
  --data-urlencode 'url=https://example.com/page?x=1&y=2' \
  --data 'output=json&from=20240101&to=20241231&fl=timestamp,original,statuscode,mimetype&filter=statuscode:200&limit=20'
```

Use the actual URL and relevant dates. If a redirect may carry the evidence, retry the narrow query without the status filter. Widen dates only when needed. Be aware that `collapse=digest` can hide the occurrence nearest the target date. Honor retry headers and back off on rate limits or service errors.

Read replay at `https://web.archive.org/web/<timestamp>/<original-url>` or use `<timestamp>id_` for unrewritten content. Confirm which capture was actually served. Resolve relative links in raw content against the original page's URL or base URL before selecting captures of those targets.
