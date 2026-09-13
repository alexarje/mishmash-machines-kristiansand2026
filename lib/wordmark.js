/* Rolling wordmark, adapted from mishmash-web/site/assets/js/wordmark.js.
   The inline MISH/MASH mark has its I/A, S and H columns built as vertical
   strips of repeated glyphs behind a clip. This rolls one to three of them
   at random intervals, in random directions, like a split-flap board that
   never quite settles. Runs on every mark inside the slides (title and
   strip openers), not on the small mark in the corner. Readers who prefer
   reduced motion see the static mark. */
(function () {
  'use strict';
  if (!window.matchMedia) { return; }
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var P = 129.66;                 // pitch between repeated S and H glyphs
  var IA = [127.104, 132.216];    // I to A and A to I steps (sum = 2P)
  var EASE = 'cubic-bezier(.7, 0, .3, 1)';

  function rand(a, b) { return a + Math.random() * (b - a); }
  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function animate(mark) {
    var cols = {
      s:  { el: mark.querySelector('.mm-col-s'),  off: 0, busy: false, period: P },
      h:  { el: mark.querySelector('.mm-col-h'),  off: 0, busy: false, period: P },
      ia: { el: mark.querySelector('.mm-col-ia'), off: 0, busy: false, period: 2 * P, parity: 0 }
    };
    if (!cols.s.el || !cols.h.el || !cols.ia.el) { return; }

    function set(c, off, ms) {
      c.el.style.transition = ms ? 'transform ' + ms + 'ms ' + EASE : 'none';
      c.el.style.transform = 'translateY(' + off.toFixed(3) + 'px)';
      c.off = off;
    }
    function roll(key, dir, ms) {
      var c = cols[key];
      if (c.busy) { return; }
      c.busy = true;
      var step = P;
      if (key === 'ia') {
        step = ((dir < 0) === (c.parity === 0)) ? IA[0] : IA[1];
        c.parity ^= 1;
      }
      set(c, c.off + dir * step, ms);
      window.setTimeout(function () {
        if (Math.abs(Math.abs(c.off) - c.period) < 0.5) {
          set(c, 0, 0);
          void c.el.getBoundingClientRect();
        }
        c.busy = false;
      }, ms + 40);
    }
    function gesture(n) {
      var keys = ['s', 'h', 'ia'].sort(function () { return Math.random() - 0.5; }).slice(0, n);
      var shared = Math.random() < 0.5 ? pick([-1, 1]) : 0;
      var delay = 0;
      keys.forEach(function (key) {
        var dir = shared || pick([-1, 1]);
        var ms = Math.round(rand(650, 1100));
        window.setTimeout(function () { roll(key, dir, ms); }, delay);
        delay += Math.round(rand(90, 280));
      });
    }
    function visible() {
      var sec = mark.closest('section');
      return !sec || sec.classList.contains('present');
    }
    function loop() {
      if (!reduce.matches && !document.hidden && visible()) {
        gesture(pick([1, 1, 2, 2, 3]));
      }
      window.setTimeout(loop, Math.round(rand(2500, 8000)));
    }
    window.setTimeout(loop, Math.round(rand(700, 1500)));
    var link = mark.closest('.mm-wordmark') || mark;
    link.addEventListener('mouseenter', function () { if (!reduce.matches) { gesture(3); } });
  }

  document.querySelectorAll('.reveal .slides .mm-wordmark-svg').forEach(animate);
})();
