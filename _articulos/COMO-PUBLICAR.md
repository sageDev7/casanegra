# Cómo publicar un artículo nuevo (sin panel)

1. Crear un archivo en esta carpeta (`_articulos/`) con el nombre que va a tener la URL, en minúsculas y con guiones.
   Ejemplo: `amparo-ambiental-cordoba.md` → se publica en `/articulos/amparo-ambiental-cordoba`.
2. Arriba del todo, entre dos líneas `---`, los datos del artículo:

```
---
titulo: Título completo del artículo
fecha: 2026-11-15
area: Derecho Ambiental
autor: francisco        (francisco | paula | estudio)
resumen: Una o dos frases que aparecen en el listado y en Google.
fuente: (opcional) medio donde se publicó originalmente
imagen: nombre.jpg      (opcional: SOLO si el cliente mandó una foto para este artículo)
borrador: si            (opcional: si está, no se publica)
---
```

   Si hay `imagen`, el archivo va en `img/articulos/` (horizontal, idealmente 1600 px de ancho y menos de 400 KB).
   Se usa de fondo en la cabecera del artículo y como imagen al compartirlo. Sin `imagen`, la cabecera va con el degradé del sitio.
3. Debajo, el texto en Markdown:
   - `## Título de sección` y `### Subtítulo`
   - Párrafos separados por una línea en blanco
   - `**negrita**`, `*itálica*`, `[texto del link](https://...)`
   - Listas con `- ` al principio de cada línea (o `1. ` para numeradas)
   - Citas destacadas con `> ` al principio
   - Notas al pie: en el texto `[^1]` y al final `[^1]: Texto de la nota.`
   - Si un párrafo empieza con un número seguido de punto (ej. «1. Como señala…»), escribirlo `1\. Como señala…` para que no se convierta en lista.
4. Correr desde la carpeta del proyecto:

```
python _scripts/publicar.py
```

   Genera la página del artículo, actualiza `articulos.html` (con el filtro por área) y los últimos 3 de la home.
5. Subir al hosting: la carpeta `articulos/`, `articulos.html` e `index.html`.

Las áreas nuevas aparecen solas como filtro en el listado. Para sumar un autor nuevo, agregarlo en `AUTORES` dentro de `_scripts/publicar.py`.
