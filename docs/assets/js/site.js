/* Progressive enhancement only: the site works without this file.
   A link with data-open-details="<id>" opens that <details> before jumping to it (Fees: Good Faith Estimate),
   and arriving with #gfe in the address does the same. */
(function () {
  function openFor(link) {
    var d = document.getElementById(link.getAttribute('data-open-details'));
    if (d) d.open = true;
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-open-details]');
    if (a) openFor(a);
  });
  if (location.hash) {
    var a = document.querySelector('a[data-open-details][href="' + location.hash + '"]');
    if (a) openFor(a);
  }
})();
