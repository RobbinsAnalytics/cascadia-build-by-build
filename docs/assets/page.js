/**
 * Cascadia Build by Build: the page's only script.
 *
 * The matrix is an HTML table, not a canvas. This file composes no figure and
 * no sentence (K2); src/build_page.py writes every one of those. It decides
 * two things about geometry:
 *
 *   1. Below one declared breakpoint, measured on the matrix HOST's width and
 *      not the window's (CHART-REVIEW K6), the surface headers show their
 *      number only and the band headers their abbreviation. Both mappings are
 *      declared in the markup by src/build_page.py and printed in the key
 *      under the table at every width, so nothing is deleted, only
 *      abbreviated (Rule 5.5).
 *   2. When the table is wider than its container it scrolls sideways inside
 *      a wrapper with a sticky row-label column, and this file toggles the
 *      scroll shadows that make that affordance visible (Rule 5.1's narrow
 *      treatment). The document itself never scrolls sideways (Rule 5.3,
 *      WCAG 1.4.10; asserted by src/render_charts.py at every width).
 *
 * No animation, no transition, no tooltip, no reader control. Nothing here
 * runs on an event a static render cannot see except the resize itself.
 */
(function () {
  'use strict';

  /**
   * EVERY WIDTH AT WHICH THIS PAGE CHANGES ITS MIND, DECLARED IN ONE PLACE.
   * Two breakpoints, both on the host element's clientWidth.
   *   narrow: below it the full-name header no longer fits (the wide table is
   *           964 px inside a 24 px card padding), so headers show numbers,
   *           the key moves above the table and the era becomes a group row.
   *           The first build set this at 700 and the panel found the table
   *           silently cropped between 742 and ~1030; the crossing now sits
   *           where the wide table actually fits.
   *   numbers: below it the narrow layout's 48 px cells with names no
   *           longer fit either (panel finding 3), so headers show numbers
   *           only, cells drop to 24 px and the key moves above the table.
   *   hint:   below it even the narrow table (466 px) is wider than the
   *           wrapper (host less 12 px of card padding), so it scrolls and a
   *           sentence says so.
   */
  var BP = { hint: 478, numbers: 830, narrow: 990 };
  window.CASCADIA_BREAKPOINTS = [BP.hint, BP.numbers, BP.narrow];

  var host = document.getElementById('matrix');
  if (!host) { return; }
  var scroller = host.querySelector('.table-scroll');

  function shadows() {
    if (!scroller) { return; }
    var max = scroller.scrollWidth - scroller.clientWidth;
    scroller.classList.toggle('scrolls', max > 1);
    scroller.classList.toggle('can-left', scroller.scrollLeft > 1);
    scroller.classList.toggle('can-right', scroller.scrollLeft < max - 1);
  }

  function layout() {
    var w = host.clientWidth;
    host.classList.toggle('narrow', w < BP.narrow);
    host.classList.toggle('numbers', w < BP.numbers);
    host.classList.toggle('hint', w < BP.hint);
    if (scroller) { host.style.setProperty('--wrap-w', scroller.clientWidth + 'px'); }
    shadows();
  }

  window.addEventListener('resize', layout);
  if (scroller) { scroller.addEventListener('scroll', shadows); }
  layout();
})();
