#!/usr/bin/env python3
"""Genera las páginas HTML del sitio de COMERCIACOR a partir de catalogo.json
y de los textos legales en fuente/legal/.

Uso (desde la raíz del repositorio):
    python3 fuente/generar.py

El resultado queda en la carpeta sitio/, que es la que publica Render.
"""
import html
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "fuente"
SITIO = RAIZ / "sitio"

datos = json.loads((FUENTE / "catalogo.json").read_text(encoding="utf-8"))
EMP = datos["empresa"]
DOMINIO = EMP["dominio"].rstrip("/")
e = html.escape
CUR = ' aria-current="page"'

ICONO_WA = (
    '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 '
    '4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.2h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.23 8.23 0 0 1-4.2-1.15l-.3-.18'
    '-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.23 '
    '8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23'
    '-1.47-1.38-1.72-.14-.25-.01-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.16.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.41-.42-.56'
    '-.43h-.48a.92.92 0 0 0-.67.31c-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1'
    '.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.29Z"/></svg>'
)


def wa(texto=None):
    url = f"https://wa.me/{EMP['whatsapp']}"
    if texto:
        url += "?text=" + quote(texto)
    return url


def boton_wa(texto_mensaje, etiqueta, extra=""):
    return (f'<a class="boton boton-wa {extra}" href="{e(wa(texto_mensaje))}" target="_blank" rel="noopener">'
            f'{ICONO_WA}<span>{e(etiqueta)}</span></a>')


def nav(actual):
    marcas = "".join(
        f'<a href="/{m["slug"]}/"{CUR if actual == m["slug"] else ""}>{e(m["nombre"])}</a>'
        for m in datos["marcas_motos"]
    )
    def act(slug):
        return ' aria-current="page"' if actual == slug else ""
    return f"""
<header class="encabezado">
  <div class="contenedor">
    <a class="logo" href="/" aria-label="COMERCIACOR, ir al inicio"><img src="/assets/img/logo-comerciacor.png" alt="COMERCIACOR S.A.S." width="611" height="135"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menú</button>
    <nav class="nav" id="nav" aria-label="Principal">
      <a href="/"{act("inicio")}>Inicio</a>
      <details>
        <summary>Motos</summary>
        <div class="submenu">{marcas}</div>
      </details>
      <a href="/tecnologia/"{act("tecnologia")}>Tecnología</a>
      <a href="/medios-de-pago/"{act("medios-de-pago")}>Medios de pago</a>
      {boton_wa("Hola, quiero información sobre el crédito con COMERCIACOR.", "Escríbenos", "boton-sm")}
    </nav>
  </div>
</header>"""


def pie():
    anio = date.today().year
    return f"""
<footer class="pie">
  <div class="contenedor">
    <div class="pie-grid">
      <div>
        <span class="pie-logo"><img src="/assets/img/logo-comerciacor.png" alt="COMERCIACOR S.A.S." width="611" height="135" loading="lazy"></span>
        <p>Crédito para motocicletas, electrodomésticos y tecnología. Detrás de todos nuestros productos hay servicio, calidad y garantía.</p>
        <p>{e(EMP["nombre"])} · NIT {e(EMP["nit"])}</p>
      </div>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li>WhatsApp: <a href="{e(wa())}" target="_blank" rel="noopener">{e(EMP["whatsapp_visible"])}</a></li>
          <li>Instagram: <a href="https://www.instagram.com/{e(EMP["instagram"])}/" target="_blank" rel="noopener">@{e(EMP["instagram"])}</a></li>
          <li><a href="/medios-de-pago/">Medios de pago</a></li>
        </ul>
      </div>
      <div>
        <h2>Legal</h2>
        <ul>
          <li><a href="/autorizacion-consulta/">Autorización de consulta</a></li>
          <li><a href="/politica-de-privacidad/">Política de privacidad</a></li>
          <li><a href="/terminos-y-condiciones/">Términos y condiciones</a></li>
          <li><a href="/politica-datos-personales/">Política de datos personales</a></li>
        </ul>
      </div>
    </div>
    <div class="pie-final">© {anio} {e(EMP["nombre"])} Todos los derechos reservados.</div>
  </div>
</footer>
<a class="wa-flotante" href="{e(wa("Hola, quiero información sobre el crédito con COMERCIACOR."))}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{ICONO_WA}</a>
<script src="/assets/js/main.js" defer></script>"""


def pagina(ruta, titulo, descripcion, actual, cuerpo, extra_head=""):
    url = DOMINIO + ruta
    doc = f"""<!doctype html>
<html lang="es-CO">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_CO">
<meta property="og:site_name" content="COMERCIACOR">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{DOMINIO}/assets/img/banner-comerciacor.webp">
<meta name="theme-color" content="#163356">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/estilos.css">
{extra_head}
</head>
<body>
<a class="saltar" href="#contenido">Saltar al contenido</a>
{nav(actual)}
<main id="contenido">
{cuerpo}
</main>
{pie()}
</body>
</html>
"""
    destino = SITIO / ruta.strip("/") / "index.html" if ruta != "/" else SITIO / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(doc, encoding="utf-8")
    return ruta


rutas = []

# ---------------- Inicio ----------------
logos = "".join(
    f'<a class="marca" href="/{m["slug"]}/"><img src="/assets/img/marcas/{m["logo"]}.webp" alt="{e(m["nombre"])}" loading="lazy"></a>'
    for m in datos["marcas_motos"]
)
for extra, nombre in [("tvs", "TVS"), ("ceronte", "Ceronte")]:
    logos += f'<span class="marca"><img src="/assets/img/marcas/{extra}.webp" alt="{nombre}" loading="lazy"></span>'

ld = {
    "@context": "https://schema.org",
    "@type": "Store",
    "name": "COMERCIACOR S.A.S.",
    "url": DOMINIO,
    "logo": DOMINIO + "/assets/img/logo-comerciacor.png",
    "image": DOMINIO + "/assets/img/banner-comerciacor.webp",
    "telephone": "+" + EMP["whatsapp"],
    "taxID": EMP["nit"],
    "description": "Crédito para motocicletas, electrodomésticos y tecnología en Colombia.",
    "sameAs": [f"https://www.instagram.com/{EMP['instagram']}/"],
}

inicio = f"""
<section class="portada">
  <div class="contenedor">
    <div>
      <h1>Financia tu moto fácil y rápido</h1>
      <p class="lead">En COMERCIACOR tienes crédito para motocicleta, electrodomésticos y tecnología. Detrás de cada producto hay servicio, calidad y garantía.</p>
      <div class="acciones">
        {boton_wa("Hola, quiero cotizar una moto a crédito.", "Cotizar por WhatsApp")}
        <a class="boton boton-linea" href="#marcas">Ver motos</a>
      </div>
    </div>
    <div class="portada-visual">
      <img src="/assets/img/motos/bajaj-pulsar-ns160-fi.webp" alt="Motocicleta Bajaj Pulsar NS 160 FI" width="800" height="600" fetchpriority="high">
      <div class="carretera" aria-hidden="true"></div>
      <a class="placa" href="{e(wa("Hola, quiero información sobre el crédito para moto."))}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp al {e(EMP['whatsapp_visible'])}">
        <span class="placa-numero">{e(EMP["whatsapp_visible"])}</span>
        <span class="placa-pie">ESCRÍBENOS POR WHATSAPP</span>
      </a>
    </div>
  </div>
</section>

<section class="seccion" id="marcas">
  <div class="contenedor">
    <div class="intro">
      <h2>Las marcas que financiamos</h2>
      <p>Elige la marca para ver los modelos disponibles y pide tu cotización con crédito.</p>
    </div>
    <div class="marcas">{logos}</div>
  </div>
</section>

<section class="seccion seccion-oscura">
  <div class="contenedor">
    <div class="intro">
      <h2>Cómo sacar tu moto a crédito</h2>
    </div>
    <ol class="pasos">
      <li><h3>Escoge tu moto</h3><p>Revisa los modelos por marca y elige la que mejor se ajusta a ti.</p></li>
      <li><h3>Escríbenos por WhatsApp</h3><p>Te enviamos la cotización y te contamos qué necesitas para el estudio de crédito.</p></li>
      <li><h3>Autoriza la consulta</h3><p>Con tu <a href="/autorizacion-consulta/" style="color:#fff">autorización de consulta</a> revisamos tu solicitud y te damos respuesta.</p></li>
    </ol>
  </div>
</section>

<section class="seccion">
  <div class="contenedor dividido">
    <img src="/assets/img/pagos.webp" alt="Pago con tarjeta en datáfono" width="900" height="449" loading="lazy">
    <div>
      <h2>Medios de pago</h2>
      <ul class="lista-pagos">
        <li>Transferencia o consignación a nuestras cuentas corrientes Bancolombia o Davivienda.</li>
        <li>Tarjeta de crédito con enlace de pago Wompi: pídelo por WhatsApp.</li>
        <li>Tu cupo ADDI.</li>
      </ul>
      <a class="boton boton-linea" href="/medios-de-pago/">Ver cuentas bancarias</a>
    </div>
  </div>
</section>

<section class="seccion" style="padding-top:0">
  <div class="contenedor dividido">
    <div>
      <h2>Servicio al cliente</h2>
      <p>Escríbenos por WhatsApp al {e(EMP["whatsapp_visible"])} para consultar tu estado de cuenta, tramitar una garantía o enviar tu soporte de pago. Por el mismo medio te enviamos tu recibo.</p>
      {boton_wa("Hola, necesito ayuda con mi cuenta.", "Hablar con servicio al cliente")}
    </div>
    <img src="/assets/img/servicio.webp" alt="Asesora de servicio al cliente" width="900" height="449" loading="lazy">
  </div>
</section>
"""
rutas.append(pagina(
    "/", "COMERCIACOR | Crédito para motos, electrodomésticos y tecnología",
    "Financia tu moto fácil y rápido con COMERCIACOR. Crédito para motos Bajaj, Honda, AKT, Hero, Victory, Yamaha y Suzuki, electrodomésticos y tecnología.",
    "inicio", inicio,
    f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'))

# ---------------- Marcas de motos ----------------
for marca in datos["marcas_motos"]:
    filtro = "".join(
        f'<a href="/{m["slug"]}/"{CUR if m["slug"] == marca["slug"] else ""}>{e(m["nombre"])}</a>'
        for m in datos["marcas_motos"]
    )
    tarjetas = []
    for mod in marca["modelos"]:
        nombre_completo = f'{marca["nombre"].split()[0]} {mod["nombre"]}' if not mod["nombre"].lower().startswith("victory") else mod["nombre"]
        ficha = ""
        if mod.get("specs"):
            filas = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in mod["specs"])
            ficha = f'<details class="ficha"><summary>Características técnicas</summary><dl>{filas}</dl></details>'
        nota = f'<p class="moto-nota">{e(mod["nota"])}</p>' if mod.get("nota") else ""
        tarjetas.append(f"""
      <article class="moto">
        <div class="moto-foto"><img src="/assets/img/motos/{mod["img"]}.webp" alt="Moto {e(nombre_completo)}" loading="lazy"></div>
        <div class="moto-cuerpo">
          <p class="moto-marca">{e(marca["nombre"])}</p>
          <h2>{e(mod["nombre"])}</h2>
          {nota}{ficha}
          <div class="moto-acciones">
            {boton_wa(f"Hola, quiero cotizar la moto {nombre_completo} a crédito.", "Cotizar a crédito")}
            <a class="enlace-fab" href="{e(mod["fabricante"])}" target="_blank" rel="noopener">Ver ficha del fabricante</a>
          </div>
        </div>
      </article>""")
    cuerpo = f"""
<section class="cabecera-pagina">
  <div class="contenedor">
    <p class="migas"><a href="/">Inicio</a> / Motos / {e(marca["nombre"])}</p>
    <h1 class="placa placa-titulo">{e(marca["nombre"])}</h1>
    <p>Pregunta por tu crédito para moto y cotiza con nosotros por WhatsApp.</p>
    <nav class="filtro-marcas" aria-label="Otras marcas">{filtro}</nav>
  </div>
</section>
<section class="seccion">
  <div class="contenedor">
    <div class="catalogo">{"".join(tarjetas)}
    </div>
  </div>
</section>"""
    modelos = ", ".join(m["nombre"] for m in marca["modelos"][:4])
    rutas.append(pagina(
        f'/{marca["slug"]}/', f'Motos {marca["nombre"]} a crédito | COMERCIACOR',
        f'Compra tu moto {marca["nombre"]} a crédito con COMERCIACOR: {modelos} y más. Cotiza por WhatsApp.',
        marca["slug"], cuerpo))

# ---------------- Tecnología ----------------
tec = datos["tecnologia"]
d = tec["destacado"]
filas = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in d["specs"])
marcas_tec = "".join(
    f'<span class="marca"><img src="/assets/img/tecnologia/marca-{slug}.webp" alt="{e(n)}" loading="lazy"></span>'
    for slug, n in tec["marcas"])
cuerpo = f"""
<section class="cabecera-pagina">
  <div class="contenedor">
    <p class="migas"><a href="/">Inicio</a> / Tecnología</p>
    <h1>Tecnología y electrodomésticos a crédito</h1>
    <p>Computadores, impresoras y electrodomésticos de las principales marcas. Pregunta por el producto que necesitas.</p>
  </div>
</section>
<section class="seccion">
  <div class="contenedor">
    <article class="destacado">
      <img src="/assets/img/tecnologia/{d["img"]}.webp" alt="{e(d["nombre"])}" loading="lazy">
      <div>
        <h2>{e(d["nombre"])}</h2>
        <dl>{filas}</dl>
        {boton_wa(f"Hola, quiero información del {d['nombre']} a crédito.", "Cotizar a crédito")}
      </div>
    </article>
  </div>
</section>
<section class="seccion" style="padding-top:0">
  <div class="contenedor">
    <div class="intro">
      <h2>Marcas que comercializamos</h2>
      <p>¿Buscas otro computador, impresora o electrodoméstico? Escríbenos y te cotizamos.</p>
    </div>
    <div class="marcas">{marcas_tec}</div>
    <div class="acciones">{boton_wa("Hola, quiero cotizar un producto de tecnología o electrodoméstico.", "Cotizar otro producto")}</div>
  </div>
</section>"""
rutas.append(pagina("/tecnologia/", "Tecnología y electrodomésticos a crédito | COMERCIACOR",
                    "Computadores, impresoras y electrodomésticos a crédito: HP, Lenovo, Acer, Asus, Epson, Samsung, LG, Kalley, Haceb y más.",
                    "tecnologia", cuerpo))

# ---------------- Medios de pago ----------------
cuentas = "".join(f"""
      <div class="cuenta">
        <h3>{e(b["banco"])}</h3>
        <dl><dt>Tipo</dt><dd>{e(b["tipo"])}</dd><dt>Número</dt><dd>{e(b["numero"])}</dd><dt>Llave</dt><dd>{e(b["llave"])}</dd><dt>Titular</dt><dd>{e(EMP["nombre"])}</dd><dt>NIT</dt><dd>{e(EMP["nit"])}</dd></dl>
      </div>""" for b in datos["bancos"])
cuerpo = f"""
<section class="cabecera-pagina">
  <div class="contenedor">
    <p class="migas"><a href="/">Inicio</a> / Medios de pago</p>
    <h1>Medios de pago</h1>
    <p>Paga tu cuota por transferencia, consignación, tarjeta de crédito o cupo ADDI.</p>
  </div>
</section>
<section class="seccion">
  <div class="contenedor">
    <h2>Transferencias o consignaciones</h2>
    <div class="cuentas">{cuentas}
    </div>
    <div class="aviso">
      <p><strong>Envía tu soporte de pago</strong> o la captura de la transferencia por WhatsApp al {e(EMP["whatsapp_visible"])} y te enviamos tu recibo de pago.</p>
      {boton_wa("Hola, envío mi soporte de pago.", "Enviar soporte de pago")}
    </div>
  </div>
</section>
<section class="seccion" style="padding-top:0">
  <div class="contenedor dividido">
    <div>
      <h2>Tarjeta de crédito y ADDI</h2>
      <p>Para pagar con tarjeta de crédito, solicita por WhatsApp tu enlace de pago Wompi. También puedes usar tu cupo ADDI.</p>
      {boton_wa("Hola, quiero un enlace de pago Wompi.", "Solicitar enlace Wompi")}
    </div>
    <img src="/assets/img/pagos.webp" alt="Pago con tarjeta en datáfono" width="900" height="449" loading="lazy">
  </div>
</section>"""
rutas.append(pagina("/medios-de-pago/", "Medios de pago | COMERCIACOR",
                    "Cuentas Bancolombia y Davivienda de COMERCIACOR S.A.S., pagos con tarjeta por Wompi y cupo ADDI.",
                    "medios-de-pago", cuerpo))

# ---------------- Páginas legales ----------------
def md_a_html(texto):
    # Une líneas partidas a mitad de frase (empiezan en minúscula) con la anterior.
    lineas = []
    for l in texto.splitlines():
        l = l.strip()
        if not l:
            continue
        if lineas and re.match(r"^[a-záéíóúñ]", l) and not lineas[-1].startswith("## "):
            lineas[-1] += " " + l
        else:
            lineas.append(l)
    out, en_lista = [], False
    for i, l in enumerate(lineas):
        if l.startswith("## "):
            if en_lista: out.append("</ul>"); en_lista = False
            if i == 0:
                continue  # el primer título se usa como h1
            out.append(f"<h2>{e(l[3:])}</h2>")
        elif l.startswith("- "):
            if not en_lista: out.append("<ul>"); en_lista = True
            out.append(f"<li>{e(l[2:])}</li>")
        else:
            if en_lista: out.append("</ul>"); en_lista = False
            out.append(f"<p>{e(l)}</p>")
    if en_lista: out.append("</ul>")
    return "\n".join(out)

legales = [
    ("autorizacion-consulta", "Autorización de consulta en centrales de riesgo"),
    ("politica-de-privacidad", "Política de privacidad"),
    ("terminos-y-condiciones", "Términos y condiciones"),
    ("politica-datos-personales", "Política de datos personales"),
]
for slug, titulo in legales:
    contenido = md_a_html((FUENTE / "legal" / f"{slug}.md").read_text(encoding="utf-8"))
    cuerpo = f"""
<section class="cabecera-pagina">
  <div class="contenedor">
    <p class="migas"><a href="/">Inicio</a> / {e(titulo)}</p>
    <h1>{e(titulo)}</h1>
  </div>
</section>
<section class="seccion">
  <div class="contenedor legal">
{contenido}
  </div>
</section>"""
    rutas.append(pagina(f"/{slug}/", f"{titulo} | COMERCIACOR", f"{titulo} de COMERCIACOR S.A.S.", slug, cuerpo))

# ---------------- 404 ----------------
pagina("/404/", "Página no encontrada | COMERCIACOR", "La página que buscas no existe.", "", f"""
<section class="vacio">
  <div class="contenedor">
    <h1>Esta página no existe</h1>
    <p>Puede que el enlace esté desactualizado. Vuelve al inicio o escríbenos y te ayudamos.</p>
    <div class="acciones" style="justify-content:center"><a class="boton boton-linea" href="/">Ir al inicio</a>{boton_wa("Hola, necesito ayuda.", "Escríbenos")}</div>
  </div>
</section>""")
(SITIO / "404.html").write_text((SITIO / "404" / "index.html").read_text(encoding="utf-8"), encoding="utf-8")
(SITIO / "404" / "index.html").unlink()
(SITIO / "404").rmdir()

# ---------------- sitemap y robots ----------------
hoy = date.today().isoformat()
urls = "".join(f"<url><loc>{DOMINIO}{r}</loc><lastmod>{hoy}</lastmod></url>" for r in rutas)
(SITIO / "sitemap.xml").write_text(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
(SITIO / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n", encoding="utf-8")

print(f"Listo: {len(rutas)} páginas generadas en {SITIO}")
