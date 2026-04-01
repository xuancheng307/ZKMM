// Shared sidebar loader — fetches components/sidebar.html and marks current page active
(function () {
  var sidebar = document.querySelector('.sidebar');
  if (!sidebar) return;

  fetch('components/sidebar.html')
    .then(function (r) { return r.text(); })
    .then(function (html) {
      sidebar.innerHTML = html;
      // Mark current page link as active
      var current = location.pathname.split('/').pop() || 'index.html';
      var links = sidebar.querySelectorAll('nav a[href]');
      links.forEach(function (a) {
        if (a.getAttribute('href') === current) {
          a.classList.add('active');
        }
      });
    });
})();
