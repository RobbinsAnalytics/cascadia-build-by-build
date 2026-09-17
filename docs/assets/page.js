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
   * One breakpoint, on the host element's clientWidth.
   */
  var BP = { narrow: 700 };
  window.CASCADIA_BREAKPOINTS = [BP.narrow];

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
    if (scroller) { host.style.setProperty('--wrap-w', scroller.clientWidth + 'px'); }
    shadows();
  }

  window.addEventListener('resize', layout);
  if (scroller) { scroller.addEventListener('scroll', shadows); }
  layout();
})();
