(function () {
  const cfg = window.APP_CONFIG || { MODE: 'static' };
  if (!cfg.MODE || cfg.MODE === 'static') return;

  const originalFetch = window.fetch.bind(window);
  function typeFromUrl(input) {
    const raw = typeof input === 'string' ? input : (input && input.url) || '';
    const clean = raw.split('?')[0].replace(/^https?:\/\/[^/]+/, '');
    const match = clean.match(/(?:^|\/)content\/([a-z0-9_-]+)\.json$/i);
    return match ? match[1] : null;
  }

  window.fetch = function patchedFetch(input, init) {
    const type = typeFromUrl(input);
    const method = (init && init.method ? init.method : 'GET').toUpperCase();
    if (type && method === 'GET') {
      const base = cfg.CONTENT_BASE_URL || (cfg.API_BASE_URL + '/content');
      const sep = base.includes('?') ? '&' : '?';
      return originalFetch(`${base}${sep}type=${encodeURIComponent(type)}`, {
        credentials: 'include',
        cache: 'no-store'
      });
    }
    return originalFetch(input, init);
  };
})();
