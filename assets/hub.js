/* No cookies, storage, identifiers or network reporting. See docs/MEASUREMENT.md. */
(() => {
  'use strict';
  const campaign = {};
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const query = new URLSearchParams(location.search);
  for (const key of keys) {
    const value = query.get(key);
    if (value && /^[a-zA-Z0-9_-]{1,80}$/.test(value)) campaign[key] = value;
  }
  // The canonical root is supplied separately for nested article pages.
  const siteRoot = document.documentElement.dataset.siteRoot;
  function emit(type, fields = {}) {
    const event = {schema_version: 1, event: type, timestamp: new Date().toISOString(),
      page: location.pathname, campaign: {...campaign}, ...fields};
    document.dispatchEvent(new CustomEvent('atob:measurement', {detail: event}));
  }
  for (const a of document.querySelectorAll('a[href]')) {
    const target = new URL(a.href, location.href);
    if (target.origin === location.origin && target.pathname.startsWith(siteRoot) &&
        (target.pathname.endsWith('.html') || target.pathname.endsWith('/'))) {
      for (const [key, value] of Object.entries(campaign)) target.searchParams.set(key, value);
      a.href = target.href;
    }
  }
  emit('page_view');
  function click(event) {
    const a = event.target.closest && event.target.closest('a[href]');
    if (!a) return;
    if (a.dataset.retailer) emit('retailer_click', {retailer: a.dataset.retailer, placement: a.dataset.placement || 'body'});
    else if (a.closest('nav') || a.closest('footer')) emit('page_interaction', {interaction: 'navigation', destination: new URL(a.href).pathname});
  }
  document.addEventListener('click', click);
  document.addEventListener('auxclick', event => {if (event.button === 1) click(event);});
})();
