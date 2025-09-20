/*! fuurin-charts.js v0.1
   Lightweight helpers for simple charts (no deps)
   - Currently: bar chart enhancer for Weekly Study Time
   Usage:
     <div class="bar-chart" data-bar-chart data-max="100">
       <div class="bar-container" data-value="45"> ... <div class="bar-fill"></div> ... </div>
       ...
     </div>
   Notes:
   - If data-max is not provided on the chart, the script will compute it
     from the maximum data-value among bars.
   - If data-value is missing on a bar, it will try to parse the sibling
     .bar-value text (e.g., "45m").
   - Runs on DOMContentLoaded and htmx:afterSwap.
*/
(function(){
  function toNumber(val){
    if (val == null) return NaN;
    if (typeof val === 'number') return val;
    if (typeof val === 'string') {
      var m = val.match(/(-?\d+(?:\.\d+)?)/);
      return m ? parseFloat(m[1]) : NaN;
    }
    return NaN;
  }

  function initBarChart(root){
    var charts = (root || document).querySelectorAll('[data-bar-chart]');
    if (!charts || charts.length === 0) return;

    charts.forEach(function(chart){
      try {
        var bars = chart.querySelectorAll('.bar-container');
        if (!bars.length) return;

        // Collect values
        var values = [];
        bars.forEach(function(bar){
          var vAttr = bar.getAttribute('data-value');
          var v = toNumber(vAttr);
          if (isNaN(v)){
            var valEl = bar.querySelector('.bar-value');
            if (valEl) v = toNumber(valEl.textContent);
          }
          if (!isNaN(v)) values.push(v); else values.push(0);
        });

        // Determine max
        var maxAttr = chart.getAttribute('data-max');
        var max = toNumber(maxAttr);
        if (isNaN(max) || max <= 0){
          max = values.reduce(function(m,x){ return x>m?x:m; }, 0) || 1;
        }

        // Animate bar fills
        bars.forEach(function(bar, idx){
          var fill = bar.querySelector('.bar-fill');
          if (!fill) return;
          var value = values[idx] || 0;
          var pct = Math.max(0, Math.min(100, (value / max) * 100));

          // Accessibility
          fill.setAttribute('role', 'img');
          fill.setAttribute('aria-label', value + ' out of ' + max);

          // Start collapsed, then animate to height
          fill.style.willChange = 'height';
          var finalHeight = pct.toFixed(2) + '%';
          // If no height set yet or different, animate
          var start = getComputedStyle(fill).height;
          // Force to 0 first for a minimal animation on first render
          fill.style.height = '0%';
          requestAnimationFrame(function(){
            requestAnimationFrame(function(){
              fill.style.height = finalHeight;
            });
          });
        });
      } catch(e){ /* noop */ }
    });
  }

  function init(root){ initBarChart(root); }

  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', function(){ init(document); });
  } else { init(document); }

  // Re-run after HTMX swaps
  document.addEventListener('htmx:afterSwap', function(ev){
    var tgt = ev && ev.detail && ev.detail.target ? ev.detail.target : document;
    init(tgt);
  });
})();
