# Measurement and Project 42

The site currently has **no visitor analytics collection**. It sends no event requests, sets no cookies, writes no browser storage and generates no visitor identifiers. No backend, paid analytics or cookie banner is included.

## Campaign links

Use the official homepage as the permanent social-profile URL. Use Press for media invitations and Buy for retailer-led campaigns. Add lowercase campaign labels to a website URL:

```
https://aubreyjonesp-design.github.io/a-taste-of-brazil/?utm_source=instagram&utm_medium=social&utm_campaign=book_discovery&utm_content=profile
https://aubreyjonesp-design.github.io/a-taste-of-brazil/press.html?utm_source=publicity_desk&utm_medium=outreach&utm_campaign=reviewer_intro&utm_content=book_facts
```

These are examples of labels, not claims that any account or campaign exists. `utm_source` identifies the channel, `utm_medium` the traffic type, `utm_campaign` the campaign and `utm_content` the specific post or link. Optional `utm_term` is also supported. Use only letters, numbers, underscore and hyphen, maximum 80 characters per value. Never include names, email addresses, reviewer identities or other personal information. If a URL already has a query, use `&` rather than a second `?`.

The small script carries valid labels across links to HTML pages within this project. It reads labels from the current URL only; it does not retain sessions or read the full referrer. Direct or unlabelled visits have an empty campaign object. Navigation without JavaScript still works, but does not carry campaign tags between pages. Canonicals and sitemap URLs omit tags.

**Retailer URLs are preserved exactly.** Campaign tags are not appended to the Google Play product URL. Marked purchase links have `data-retailer="google-play-books"` and a placement tag. This avoids relying on a retailer accepting or reporting UTM tags.

## Event interface

`assets/hub.js` dispatches `atob:measurement` custom events on `document`:

- `page_view`: page arrival.
- `page_interaction`: navigation/footer click and destination pathname.
- `retailer_click`: activation of a marked purchase link, retailer ID and button placement. Mouse primary/middle clicks and keyboard link activation are supported. Context-menu opening cannot reliably be observed.

Each event has `schema_version: 1`, a UTC ISO timestamp, page pathname, and the five allowlisted campaign fields when valid. No IP address, user ID, full referrer, screen fingerprint or arbitrary query string is included. These events are transient; dispatching an event is **not collecting analytics**. The visitor clock may be inaccurate and automatic traffic is not filtered. Clicks indicate an intention to visit a retailer, not a completed purchase.

A future approved collector can attach a listener before `hub.js` runs. For example, in a developer console a listener can inspect subsequent click events:

```js
document.addEventListener('atob:measurement', event => console.log(event.detail));
```

The initial page event has already fired by the time a console listener is added. This example does not persist events. Do not add transmission, identifiers or storage without reviewing actual privacy requirements and updating the public privacy page. A cookie banner is not needed for the technology currently used; future technology may change that.

## What is and is not evidence

| Signal | Available now? | Meaning/limit |
| --- | --- | --- |
| Labelled campaign URL | Yes | Identifies a planned publicity source |
| Page/retailer event format | Yes, in the active page | Future integration interface; not saved counts |
| Aggregate visits or clicks | No | GitHub Pages provides no general visitor event database |
| Referral history or unique visitors | No | Deliberately no persistent identifiers/session tracking |
| Search discovery | Not configured | Free Search Console can later show Google impressions/clicks once the owner verifies the site |
| Book purchases/conversion rate | No | Requires real retailer/distributor reporting; cannot be inferred from clicks |
| Cross-retailer sales attribution | No | Depends on genuine reporting capabilities; UTM labels alone cannot prove sales |

For Project 42, keep a private campaign register with source, medium, campaign, content, destination URL, publication UTC date and evidence link. Separately retain genuine retailer/distributor sales exports, the report period, territory and provenance. Compare time periods cautiously; simultaneous publicity and sales do not prove causation. Do not store sales files, outreach contact lists or personal data in this public repository.

No backend is built merely to gather evidence. A later zero-cost collection option should be evaluated only when its hosting, privacy, retention and actual free limits are known. Until then report measured sales from official reports and campaign activity from the register; do not report uncollected visits or retailer clicks as evidence.
