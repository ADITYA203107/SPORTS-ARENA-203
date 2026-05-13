(function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
  }
  window.getCsrfToken = function () {
    const m = document.querySelector('meta[name="csrf-token"]');
    return (m && m.content) || getCookie('csrftoken') || '';
  };
  window.fetchJSON = function (url, opts) {
    opts = opts || {};
    opts.headers = Object.assign(
      { 'X-Requested-With': 'XMLHttpRequest', Accept: 'application/json' },
      opts.headers || {}
    );
    if (opts.method && opts.method.toUpperCase() !== 'GET') {
      opts.headers['X-CSRFToken'] = window.getCsrfToken();
    }
    return fetch(url, opts).then((r) => r.json());
  };
})();
