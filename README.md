# A TASTE OF BRAZIL

**Authentic Family Recipes from the Heart of Brazil**

**Edneia “Neia” Silveira & Philip Aubrey-Jones**

A small, free, static publishing hub for the family cookbook. The approved homepage remains the landing page. No hosting purchases, paid services, runtime dependencies or analytics accounts are needed.

Official site: https://aubreyjonesp-design.github.io/a-taste-of-brazil/

## What is where

| File | Purpose |
| --- | --- |
| `index.html` | Approved homepage, with supporting navigation and metadata |
| `about-the-book.html` | Book description and subtitle |
| `authors.html` | Confirmed author names; no invented biographies |
| `buy.html` | Central retailer destination |
| `press.html` | Single URL for reviewers and media; downloadable facts and cover |
| `brazilian-food.html` | Existing artwork and entry point for future approved articles |
| `privacy.html` | Plain explanation of campaign links and privacy |
| `data/retailers.json` | **The one place to maintain retailer links** |
| `data/site.json` | Official website address, factual description, authors, optional contact/social links |
| `data/articles.json` | Future articles; currently empty |
| `data/coverage.json` | Future genuine reviews, press, interviews and awards; currently empty |
| `assets/` | Exact copies of existing artwork, styles, small script and factual text download |
| `tools/build.py` | Builds the HTML and sitemap using Python, with no installed packages |
| `tools/check.py` | Checks links, metadata and preservation |
| `templates/` | Examples to copy when real content is available; not published pages |
| `A-Taste-of-Brazil-corrected-1.html` | Untouched original approved file; source for the homepage build |

The factual source is the original homepage at commit `abed85900135c5363cbc71560a1a9d774002ece1`, plus the authoritative title, subtitle and authorship in the execution brief. No additional biographies, ISBN, publisher, publication date, prices, contact address, social accounts, reviews or retailer availability have been assumed.

## Making changes

A helper can edit the JSON files, then run:

```sh
python3 tools/build.py
python3 tools/check.py
```

Upload **both the edited source files and regenerated output files**. Visitors get complete static HTML even with JavaScript switched off. GitHub Pages does not run the Python builder. Avoid editing generated HTML directly: the next build replaces it. Homepage content or visual changes require explicit approval; keep the original archive recoverable.

### Add a verified retailer

1. Open the real product listing and confirm that it is this book, with correct authorship and identity. Availability may vary by country.
2. In `data/retailers.json`, copy an existing object and add a comma between entries. Give it a unique lowercase ID, retailer name, genuine HTTPS product URL, confirmed format and a `verified_in` note recording evidence/date. Do not add prospective retailers or guessed URLs.
3. Run the two commands above. The Buy and Press pages update together. The homepage continues its established Google Play route.
4. Open the regenerated links and verify them before upload.

The builder only checks URL syntax and evidence fields; it cannot establish that a listing is genuine. Human verification is required. Do not edit the preserved Google Play link without explicit authorisation.

### Add genuine reviews or press coverage

Start with `templates/coverage.json.example`. Follow its notes in `templates/README.md`. Use a genuine source URL and identify its kind (editorial review, reader review, interview, article, press mention or award). Link to the original material. Copy a quote only with appropriate permission or a clearly documented lawful basis; the template records that evidence. A source link alone does not grant reproduction rights. Do not include private emails or personal reviewer information in these public files.

Add the object inside the array in `data/coverage.json`. Set `published` to true only when checked and authorised. Rebuild. `reviews.html`, its navigation link and sitemap entry appear only when a published item exists. An empty coverage collection has no visitor-facing reviews page.

### Add an article

Start with `templates/article.json.example`. Add approved, useful author-led material with sources where factual claims need support. Use a short unique slug, descriptive title and description, author, sections of paragraphs, sources and an approval note. Drafts stay unpublished with `published: false`. Never put confidential content in a draft: the repository is public.

Add it to `data/articles.json` and rebuild. An approved article appears at `articles/your-slug.html` and is linked from the Brazilian food page and sitemap. Keep recipe publication rights in mind; do not assume the entire book may be reproduced. Templates support plain text paragraphs, which the builder escapes safely. Extend the builder only if richer content is actually needed.

### Contact and social accounts

`data/site.json` contains `contact_email: null` and `social_links: []` because no contact mechanism or authorised accounts exist in the source. When Phil supplies approved public details, replace null with the public email and add objects like `{"name": "Instagram", "url": "GENUINE_HTTPS_PROFILE_URL"}` to the social array, then rebuild. Never upload private credentials. A media contact will then appear on Press; social links appear in all footers.

## Deployment and recovery

The repository's `index.html` is the entry point. The source has no custom-domain file and no custom build workflow. The existing publishing instructions describe GitHub Pages deployment from **main / root**. Preserve that setup; confirm the current selection in Settings → Pages before uploading. The last successful GitHub Pages workflow deployed `main` at the baseline commit, and its deploy log confirms the official URL above. The current Settings → Pages selection could not be read directly during this task.

To deploy the prepared expansion, upload the package contents at the repository root, preserving folders, or commit them through Git. With the existing main/root Pages setup, GitHub publishes automatically. Wait for the Pages build to succeed, then open the homepage, Buy and Press URLs on a phone and desktop. No custom domain or paid plan is required. The `.nojekyll` file ensures this is served as plain static files.

To preview locally:

```sh
python3 -m http.server 8000 --directory ..
```

Open http://localhost:8000/a-taste-of-brazil/ (assuming this folder is named `a-taste-of-brazil`).

Before uploading, preserve the current main commit. The official baseline is `abed85900135c5363cbc71560a1a9d774002ece1`; the original file's Git blob is `90aa25c42d7f7ec495950992d0afb2103d991c17`. To recover, revert the expansion commit in GitHub, or restore the original archive as `index.html`. Keep extra pages out of navigation if rolling back. This task also saved a local Git baseline.

GitHub Pages project sites live below `/a-taste-of-brazil/`. Relative links deliberately support that path. `robots.txt` here is beneath the project path; crawlers consult robots.txt at the host root. It cannot set host-wide crawl rules. The sitemap is usable directly and may be submitted to a free Search Console property later. The old archive remains byte-for-byte unchanged and accessible at its existing URL; it is excluded from the new sitemap. It has no canonical metadata, which is a preserved legacy limitation.

## Measurement and next information

See [Measurement](docs/MEASUREMENT.md) for campaign examples, event fields and Project 42 limitations, and [Validation](docs/VALIDATION.md) for actual test results and deployment constraints.

Phil can supply an approved media contact, short biographies, verified publication/ISBN information, authorised social links, further verified product URLs and genuine coverage. None is required to use the current site. The next practical step is deployment and live verification, then adding an approved media contact and author biographies.
