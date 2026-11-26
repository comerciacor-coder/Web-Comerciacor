// Solicitud de paz y salvo: habla con el CRM de COMERCIACOR (crm.comerciacor.com)
(function () {
  'use strict';
  var CRM = 'https://crm.comerciacor.com';
  var f1 = document.getElementById('ps-form');
  var f2 = document.getElementById('ps-codigo');
  var msg = document.getElementById('ps-msg');
  if (!f1 || !f2) return;
  var token = null;

  function mostrar(texto, tipo) { msg.hidden = !texto; msg.className = 'ps-msg' + (tipo ? ' ps-' + tipo : ''); msg.textContent = texto || ''; }
  function limpiarErrores() { var e = f1.querySelectorAll('.ps-err'); for (var i = 0; i < e.length; i++) e[i].textContent = ''; }
  function llamar(ruta, datos) {
    return fetch(CRM + '/publico/paz-y-salvo/' + ruta, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(datos) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) { var e = new Error(j.error || 'No pudimos atender la solicitud. Intenta de nuevo.'); e.errors = j.errors; throw e; } return j; }); })
      .catch(function (e) { if (e instanceof TypeError) throw new Error('No pudimos conectarnos. Revisa tu conexión a internet e intenta de nuevo.'); throw e; });
  }
  function ocupado(form, si) { var b = form.querySelector('button[type=submit]'); b.disabled = si; b.dataset.t = b.dataset.t || b.textContent; b.textContent = si ? 'Un momento…' : b.dataset.t; }

  // el error de un campo se borra en cuanto se corrige
  f1.addEventListener('input', function (ev) { var n = ev.target.name; var s = n && f1.querySelector('[data-err="' + n + '"]'); if (s) s.textContent = ''; });
  f1.addEventListener('change', function (ev) { var n = ev.target.name; var s = n && f1.querySelector('[data-err="' + n + '"]'); if (s) s.textContent = ''; });
  f1.addEventListener('submit', function (ev) {
    ev.preventDefault(); limpiarErrores(); mostrar('');
    var d = { cedula: f1.cedula.value, nombre: f1.nombre.value, celular: f1.celular.value, email: f1.email.value, acepta: f1.acepta.checked };
    ocupado(f1, true);
    llamar('solicitar', d).then(function (r) {
      token = r.token;
      document.getElementById('ps-codigo-txt').textContent = 'Te enviamos un código de 6 dígitos por mensaje de texto al celular ' + r.celular + '. Vence en ' + r.minutos + ' minutos. Obligación: ' + r.obligaciones.join(', ') + '.';
      f1.hidden = true; f2.hidden = false; f2.codigo.value = ''; f2.codigo.focus();
    }).catch(function (e) {
      if (e.errors) { for (var k in e.errors) { var s = f1.querySelector('[data-err="' + k + '"]'); if (s) s.textContent = e.errors[k]; } }
      mostrar(e.message, 'error');
    }).then(function () { ocupado(f1, false); });
  });

  f2.addEventListener('submit', function (ev) {
    ev.preventDefault(); mostrar('');
    ocupado(f2, true);
    llamar('confirmar', { token: token, codigo: f2.codigo.value }).then(function (r) {
      f2.hidden = true;
      mostrar('¡Listo! Enviamos tu paz y salvo (' + r.paz_salvos.map(function (p) { return p.consecutivo + ', obligación ' + p.cuenta; }).join('; ') + ') a tu correo ' + r.email + '. Si no lo ves en unos minutos, revisa la carpeta de correo no deseado.', 'ok');
    }).catch(function (e) { mostrar(e.message, 'error'); }).then(function () { ocupado(f2, false); });
  });

  document.getElementById('ps-volver').addEventListener('click', function () { token = null; f2.hidden = true; f1.hidden = false; mostrar(''); });
})();
