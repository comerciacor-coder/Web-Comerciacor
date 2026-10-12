# Sitio web de COMERCIACOR S.A.S.

Sitio estático (HTML, CSS y un poco de JavaScript) que reemplaza el sitio hecho con el creador de sitios de GoDaddy. Se aloja en GitHub y se publica en Render.

## Qué hay en el repositorio

```
sitio/            Lo que se publica en internet (Render sirve esta carpeta)
  index.html      Inicio
  bajaj/ honda/ akt/ hero/ auteco/ yamaha/ suzuki/   Catálogo de motos por marca
  tecnologia/     Computadores, impresoras y electrodomésticos
  medios-de-pago/ Cuentas bancarias, Wompi y ADDI
  autorizacion-consulta/ politica-de-privacidad/ terminos-y-condiciones/ politica-datos-personales/
  assets/         Estilos, script e imágenes
  robots.txt      Permite que Google indexe el sitio
  sitemap.xml     Mapa del sitio para Google
fuente/           Datos con los que se generan las páginas
  catalogo.json   Motos, tecnología, cuentas bancarias y WhatsApp
  legal/          Textos legales
  generar.py      Script que vuelve a crear las páginas de sitio/
render.yaml       Configuración de Render
```

## Cómo cambiar el contenido

**Opción sencilla:** edita directamente el archivo HTML de la página en GitHub (botón del lápiz) y guarda. Render publica el cambio solo, en uno o dos minutos.

**Opción recomendada para el catálogo:** edita `fuente/catalogo.json` (por ejemplo, para agregar una moto), pon la foto en `sitio/assets/img/motos/` con el mismo nombre que indicas en `"img"`, y ejecuta en tu computador:

```
python3 fuente/generar.py
```

Luego sube los cambios a GitHub. El script regenera todas las páginas, el `sitemap.xml` y el `robots.txt`.

Para agregar una moto, copia una línea como esta dentro de la marca que corresponda:

```json
{"nombre": "Pulsar NS 160 FI", "img": "bajaj-pulsar-ns160-fi", "fabricante": "https://grupouma.com/..."}
```

## Paso a paso: de GoDaddy a GitHub y Render

Haz los pasos en este orden. Así el sitio nunca se cae durante el cambio.

### 1. Subir a GitHub

1. Entra a github.com con tu cuenta y crea un repositorio nuevo llamado `comerciacor-web` (puede ser privado).
2. Sube todo el contenido de esta carpeta. Desde la web: **Add file → Upload files**, arrastra las carpetas `sitio` y `fuente` y los archivos `render.yaml`, `README.md` y `.gitignore`, y pulsa **Commit changes**.

   Si usas la terminal:
   ```
   git remote add origin https://github.com/TU-USUARIO/comerciacor-web.git
   git push -u origin main
   ```

### 2. Publicar en Render

1. Entra a dashboard.render.com e inicia sesión con tu cuenta de GitHub.
2. Pulsa **New → Blueprint** y elige el repositorio `comerciacor-web`. Render lee `render.yaml` y crea el sitio estático `comerciacor`.
   (También funciona **New → Static Site**: deja el comando de build como `echo "Sitio listo"` y el directorio de publicación como `sitio`.)
3. Al terminar, Render te da una dirección como `https://comerciacor.onrender.com`. Ábrela y revisa todo: menú, catálogo, botones de WhatsApp, medios de pago.

### 3. Conectar comerciacor.com

1. En Render, abre el sitio → **Settings → Custom Domains → Add Custom Domain** y escribe `comerciacor.com`. Render agrega también `www.comerciacor.com`.
2. En GoDaddy, primero desconecta el dominio del creador de sitios: **Mis productos → Sitios web y marketing → Configuración → Dominio**, y quita la conexión de comerciacor.com.
3. En GoDaddy, ve a **Mis productos → Dominios → comerciacor.com → DNS** y deja así los registros del sitio web:

   | Tipo  | Nombre | Valor                         |
   |-------|--------|-------------------------------|
   | A     | @      | 216.24.57.1                   |
   | CNAME | www    | comerciacor.onrender.com      |

   - Borra cualquier otro registro **A** de `@` y cualquier registro **AAAA**.
   - Si hay **Reenvío de dominio** (forwarding) activo, desactívalo.
   - **No toques los registros MX, TXT ni los nameservers.** Si tienen correo con el dominio, seguirá funcionando.
   - Usa el valor exacto `.onrender.com` que te muestre Render; puede ser distinto si el nombre `comerciacor` ya estaba ocupado.
4. Vuelve a Render y pulsa **Verify**. Cuando quede verificado, Render activa el certificado HTTPS automáticamente. Puede tardar desde unos minutos hasta algunas horas.

### 4. Bajar el sitio de GoDaddy

Cuando `https://comerciacor.com` ya cargue el sitio nuevo:

- Cancela **solo** el plan del creador de sitios (Websites + Marketing).
- **No canceles el dominio** comerciacor.com: sigue registrado y renovándose en GoDaddy, solo apunta a Render.

### 5. Avisarle a Google

1. Entra a Google Search Console (search.google.com/search-console) y agrega `comerciacor.com`.
2. En **Sitemaps**, envía `https://comerciacor.com/sitemap.xml`.

El sitio anterior bloqueaba a los buscadores; este los permite, así que Google empezará a mostrarlo en los resultados.

## Direcciones del sitio anterior

`render.yaml` redirige las direcciones viejas para que nadie llegue a una página rota:

- `/computadores` y `/impresoras` → `/tecnologia/`
- `/terminos-y-condiciones-1` → `/terminos-y-condiciones/`

Las demás (`/bajaj`, `/honda`, `/medios-de-pago`, páginas legales, etc.) conservan la misma dirección.
