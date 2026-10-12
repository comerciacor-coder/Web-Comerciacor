// Menú móvil
(function () {
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var abierto = nav.classList.toggle('abierto');
    btn.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    btn.textContent = abierto ? 'Cerrar' : 'Menú';
  });
  // Cierra el submenú de Motos al hacer clic fuera
  document.addEventListener('click', function (ev) {
    document.querySelectorAll('.nav details[open]').forEach(function (d) {
      if (!d.contains(ev.target)) d.removeAttribute('open');
    });
  });
})();
