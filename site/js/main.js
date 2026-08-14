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

  /* --- Email de-obfuscation -----------------------------------------------
     The address is not in the HTML. It arrives base64-encoded and reversed,
     split across two attributes, and is only ever assembled here. Harvesters
     that pattern-match the raw page find nothing to take.

     Until this runs, every one of these links points at the Instagram DM, so
     a visitor without JavaScript still has a working way to get in touch. */
  function decodeEmail(el) {
    var joined = (el.getAttribute('data-email-a') || '') +
                 (el.getAttribute('data-email-b') || '');
    if (!joined) return '';
    try {
      return atob(joined.split('').reverse().join(''));
    } catch (e) {
      return '';   // malformed: leave the Instagram fallback in place
    }
  }

  document.querySelectorAll('[data-email-a]').forEach(function (el) {
    var address = decodeEmail(el);
    if (!address) return;

    var subject = el.getAttribute('data-email-subject');
    var body = el.getAttribute('data-email-body');
    var href = 'mailto:' + address;
    if (subject) href += '?subject=' + subject;
    if (body) href += (subject ? '&' : '?') + 'body=' + body;

    el.setAttribute('href', href);
    // mailto: must not open in a new tab; it would leave a blank window behind.
    el.removeAttribute('target');
    el.removeAttribute('rel');

    // Where the address itself was the link text, show it now that we have it.
    if (el.hasAttribute('data-email-text')) el.textContent = address;
  });

  /* --- Food carousel ------------------------------------------------------
     The track scrolls natively, so swipe and trackpad already work without
     this. All we add is a pair of arrows, and we only show them when the
     track genuinely overflows. */
  document.querySelectorAll('[data-carousel]').forEach(function (carousel) {
    var track = carousel.querySelector('[data-carousel-track]');
    var prev = carousel.querySelector('[data-carousel-prev]');
    var next = carousel.querySelector('[data-carousel-next]');
    if (!track || !prev || !next) return;

    function step() {
      var item = track.querySelector('.carousel__item');
      var gap = parseFloat(getComputedStyle(track).columnGap || '16') || 16;
      return item ? item.getBoundingClientRect().width + gap : track.clientWidth * 0.8;
    }

    function update() {
      var overflows = track.scrollWidth > track.clientWidth + 4;
      prev.hidden = next.hidden = !overflows;
      if (!overflows) return;
      // 2px of slack: sub-pixel widths stop scrollLeft hitting the exact end.
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    }

    prev.addEventListener('click', function () {
      track.scrollBy({ left: -step(), behavior: 'smooth' });
    });
    next.addEventListener('click', function () {
      track.scrollBy({ left: step(), behavior: 'smooth' });
    });

    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
    update();
  });

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
