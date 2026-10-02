# Validation and delivery status

Checked on 2 October 2026. This is an implementation validation, not a new general site audit.

## Passed locally

- `python3 tools/build.py`: seven complete static pages, one confirmed retailer, no published articles or coverage.
- `python3 tools/check.py`: 92 internal links; 22 local/embedded asset references; no missing files or broken internal fragments.
- Explicit balanced HTML tags, one main landmark, one h1 and one title per generated page, image alt text, unique IDs, skip links and semantic navigation.
- Page titles/descriptions, canonical and Open Graph/social fields; valid JSON-LD with Book, both Person authors, WebSite, WebPage and internal-page BreadcrumbList. This is structural validation, not a remote rich-results eligibility test or a guarantee of search display.
- Sitemap XML parses and exactly matches the seven intended canonical pages. Robots file references the sitemap. Host-root robots limitation is documented in README.
- Original archive Git blob hash is **90aa25c42d7f7ec495950992d0afb2103d991c17**, exactly matching GitHub. All three original embedded image strings remain unchanged on the homepage; extracted assets match their decoded original bytes.
- Original homepage CSS and main content preserved. Changes inside its main element are limited to attributes identifying the existing retailer link for future events. Header purchase link remains. Footer now credits both authoritative authors.
- Both original Google Play URLs are identical to the approved route. Buy and Press use that same product URL generated from the retailer configuration.
- No placeholder text in visitor pages. Empty articles/coverage remain unpublished. No invented reviews, biographies, awards, prices, publication details or additional retailers.
- `node --check assets/hub.js`: valid JavaScript syntax.
- `node tools/check-measurement.cjs`: DOM harness verifies project-only UTM propagation, ignored invalid/non-allowlisted queries, exact retailer URLs, untagged downloads, page/click/navigation event fields and no storage or event network calls.
- Repeated build produces identical output.
- Text contrast calculations: forest/cream 11.83:1, rust/cream 5.33:1, caption/cream 5.93:1, white/forest button 12.79:1. Visible focus styles are supplied; these checks do not replace keyboard/browser testing.
- Responsive CSS retains the approved homepage breakpoints and gives new pages stacked layouts, wrapping navigation and at least 48px retailer buttons. No runtime dependencies or third-party scripts are loaded.

## Confirmed through GitHub

The repository originally contains only `index.html` and `A-Taste-of-Brazil-corrected-1.html`, both at the same original blob. There is no AGENTS.md, custom-domain file or custom build workflow in that tree.

The baseline is `abed85900135c5363cbc71560a1a9d774002ece1`. Its [Pages build and deployment](https://github.com/aubreyjonesp-design/a-taste-of-brazil/actions/runs/36853593384) completed successfully from `main`. The deployment log confirms https://aubreyjonesp-design.github.io/a-taste-of-brazil/ as the deployed URL. Root `index.html` is the site's existing entry point.

## Could not verify or publish here

Cloud HTTP access failed at the configured proxy. The GitHub connector can read repository files, but creating a backup branch returned **403 Resource not accessible by integration**. No remote files, branches or deployment settings were changed by this task. The completed expansion is a local commit and upload-ready package; the live site is still the existing version.

Chromium is installed but cannot start under this executor's socket restrictions (`setsockopt`/`shutdown: Operation not permitted`). Mobile/desktop rendering, screenshots, actual keyboard interaction and no-JavaScript browser navigation were therefore not executed. The event tests are a DOM harness, not a full browser test. No remote Google Play response or region-specific availability was verified. Those limits are not recorded as passes.

## After upload

1. Wait for a successful Pages build; open Home, Buy and Press on a phone and desktop.
2. Check 320–390px mobile and wider desktop layouts for readable text, wrapping navigation and no horizontal scrolling. Compare the homepage's approved content and artwork.
3. Use Tab/Enter to try the skip link, every navigation link and a retailer button. Turn JavaScript off and repeat page navigation/purchase access.
4. Open the Google Play link and confirm the correct product, authorship and local availability. Check the cover and facts downloads, sitemap and each page's canonical URL.
5. Follow a campaign-tagged link through the site and verify tags remain on internal page links while the retailer destination remains unchanged.

The preserved PNG artwork is about 2.3 MB; the existing homepage embeds all artwork. No images were recompressed or replaced. Further asset optimisation is a possible future measured improvement only if visual preservation is verified. GitHub Pages cannot itself collect the prepared events or establish purchase attribution. See MEASUREMENT.md.
