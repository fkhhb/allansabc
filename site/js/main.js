/* Allan's ABC — allansabc.com
   Progressive enhancement only. Everything works with JS disabled. */

(function () {
  'use strict';

  /* The .js flag is set by an inline script in <head> so it lands before first
     paint — setting it from this deferred file would flash the content in,
     out, then back. See index.html. */

  /* --- Mobile nav --------------------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var mobileNav = document.getElementById('mobile-nav');

  if (toggle && mobileNav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      mobileNav.classList.toggle('is-open', !open);
    });

    mobileNav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        toggle.setAttribute('aria-expanded', 'false');
        mobileNav.classList.remove('is-open');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && mobileNav.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        mobileNav.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  /* --- Header shadow once scrolled --------------------------------------- */
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 12);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* --- Highlight today's opening hours ------------------------------------ */
  // getDay(): 0 = Sunday ... 6 = Saturday, matching the data-day attributes.
  var today = new Date().getDay();
  var row = document.querySelector('.hours__row[data-day="' + today + '"]');
  if (row) {
    row.classList.add('is-today');
    var day = row.querySelector('.hours__day');
    if (day) {
      var flag = document.createElement('span');
      flag.className = 'visually-hidden';
      flag.textContent = ' (today)';
      day.appendChild(flag);
    }
  }

  /* --- Footer year -------------------------------------------------------- */
  var year = document.getElementById('year');
  if (year) year.textContent = String(new Date().getFullYear());

  /* --- Reveal on scroll --------------------------------------------------- */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var items = document.querySelectorAll('.reveal');

  if (reduced || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  }
})();
