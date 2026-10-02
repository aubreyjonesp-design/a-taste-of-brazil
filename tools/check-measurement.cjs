/* Run with node tools/check-measurement.cjs. No test packages needed. */
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const code = fs.readFileSync(__dirname + '/../assets/hub.js', 'utf8');
function run(query) {
  const events = [], handlers = {}, origin = 'https://aubreyjonesp-design.github.io';
  const root = '/a-taste-of-brazil/';
  const anchor = (url, data = {}, inNav = false) => ({href: url, dataset: data,
    closest: selector => selector === 'a[href]' ? null : inNav ? {} : null});
  const internal = anchor(origin + root + 'press.html');
  const sibling = anchor(origin + '/other-project/');
  const purchase = anchor('https://play.google.com/store/books/details/Edneia_Silveira_A_Taste_of_Brazil?id=nNATEgAAQBAJ', {retailer: 'google-play-books', placement: 'home'});
  const download = anchor(origin + root + 'assets/book-facts.txt');
  const nav = anchor(origin + root + 'buy.html', {}, true);
  const document = {
    documentElement: {dataset: {siteRoot: root}},
    querySelectorAll: () => [internal, sibling, purchase, download, nav],
    dispatchEvent: event => events.push(event.detail),
    addEventListener: (name, handler) => handlers[name] = handler
  };
  const noNetwork = () => {throw Error('Unexpected collection request');};
  vm.runInNewContext(code, {document, URL, URLSearchParams, Date,
    location: {origin, pathname: root, search: query, href: origin + root + query},
    CustomEvent: class {constructor(type, options) {this.type=type;this.detail=options.detail;}},
    fetch: noNetwork, navigator: {sendBeacon: noNetwork},
    localStorage: new Proxy({}, {get: noNetwork}), sessionStorage: new Proxy({}, {get: noNetwork})
  });
  return {events, internal, sibling, purchase, download, nav,
    click: (a, button=0) => handlers[button === 1 ? 'auxclick' : 'click']({button, target: {closest: () => a}})};
}
let r=run('?utm_source=instagram&utm_medium=social&utm_campaign=book_discovery&utm_content=profile&email=private@example.com');
assert.equal(r.events[0].event, 'page_view');
assert.equal(r.events[0].campaign.utm_source, 'instagram');
assert.equal(r.events[0].campaign.email, undefined);
assert.equal(new URL(r.internal.href).searchParams.get('utm_campaign'), 'book_discovery');
assert.equal(new URL(r.sibling.href).search, '');
assert.equal(new URL(r.download.href).search, '');
assert.equal(r.purchase.href, 'https://play.google.com/store/books/details/Edneia_Silveira_A_Taste_of_Brazil?id=nNATEgAAQBAJ');
r.click(r.purchase); r.click(r.purchase, 1); r.click(r.nav);
assert.deepEqual(r.events.map(e => e.event), ['page_view','retailer_click','retailer_click','page_interaction']);
assert.equal(r.events[1].retailer, 'google-play-books');assert.equal(r.events[1].placement, 'home');
assert.equal(r.events[3].destination, '/a-taste-of-brazil/buy.html');
assert.ok(!Number.isNaN(Date.parse(r.events[1].timestamp)));
r=run('?utm_source=someone%40example.com&utm_campaign='+'x'.repeat(81)+'&utm_content=valid-token');
assert.equal(r.events[0].campaign.utm_source, undefined);assert.equal(r.events[0].campaign.utm_campaign, undefined);assert.equal(r.events[0].campaign.utm_content,'valid-token');
r=run('');assert.equal(Object.keys(r.events[0].campaign).length, 0);
console.log('PASS: campaign propagation within project, invalid and non-allowlisted query rejection, unchanged retailer/download URLs, click and middle-click events, UTC timestamp, no storage/network calls. DOM harness only; browser tests remain separate.');
