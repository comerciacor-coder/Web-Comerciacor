// Verificación de un paz y salvo: consulta al CRM de COMERCIACOR (crm.comerciacor.com)
(function () {
  'use strict';
  var CRM = 'https://crm.comerciacor.com';
  var f = document.getElementById('vps-form'); var res = document.getElementById('vps-res');
  if (!f) return;
  function mostrar(html, tipo) { res.hidden = false; res.className = 'ps-msg' + (tipo ? ' ps-' + tipo : ''); res.innerHTML = html; }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (x) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[x]; }); }
  // el código puede venir en la dirección: /verificar-paz-y-salvo/?c=XXXX
  var q = new URLSearchParams(location.search).get('c'); if (q) f.codigo.value = q;
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var b = f.querySelector('button'); b.disabled = true;
    fetch(CRM + '/publico/paz-y-salvo/verificar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ codigo: f.codigo.value }) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.error || 'No pudimos verificar el código. Intente de nuevo.'); return j; }); })
      .then(function (j) {
        if (j.valido) mostrar('<strong>✓ Paz y salvo auténtico.</strong><br>' + esc(j.consecutivo) + ', expedido el ' + esc(j.fecha_texto) + ' por COMERCIACOR S.A.S.<br>Obligación N.º <strong>' + esc(j.cuenta) + '</strong> a nombre de <strong>' + esc(j.titular) + '</strong>, C.C. ' + esc(j.documento) + '.', 'ok');
        else mostrar('<strong>✗ No existe un paz y salvo con ese código.</strong><br>Revise el código o comuníquese con COMERCIACOR al 310 587 3423.', 'error');
      })
      .catch(function (e) { mostrar(esc(e instanceof TypeError ? 'No pudimos conectarnos. Revise su conexión a internet e intente de nuevo.' : e.message), 'error'); })
      .then(function () { b.disabled = false; });
  });
  if (q) f.requestSubmit ? f.requestSubmit() : f.dispatchEvent(new Event('submit'));
})();
