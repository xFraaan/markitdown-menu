# MarkItDown Menu

Una interfaz de terminal para **MarkItDown** que facilita la conversión de múltiples archivos a **Markdown** mediante un menú interactivo.

Ideal para convertir documentos de forma rápida sin tener que ejecutar comandos manualmente.

## Características

- 📄 Agregar archivos individuales.
- 📁 Agregar carpetas completas.
- 📂 Escaneo opcional de subcarpetas.
- 📊 Barra de progreso durante la conversión.
- ✅ Resumen de conversiones exitosas y errores.
- 💻 Compatible con Windows, Linux y macOS.
- 🎨 Compatible con terminales Unicode y ASCII.

---

## Requisitos

- Python 3.10 o superior
- MarkItDown

Instala MarkItDown con:

```bash
pip install "markitdown[all]"
```

---

## Uso

Clona el repositorio:

```bash
git clone https://github.com/xFraaan/markitdown-menu.git
cd markitdown-menu
```

Ejecuta el programa:

```bash
python MarkItDown.py
```

---

## Menú principal

```text
┌──────────────────────────────────────────────┐
│      🚀 MarkItDown Converter v1.0            │
├──────────────────────────────────────────────┤
│                                              │
│ Archivos cargados                            │
│                                              │
│ #  Nombre             Tipo        Tamaño     │
│ ──────────────────────────────────────────── │
│ 1  documento.pdf      PDF         1.2 MB     │
│ 2  informe.docx       Word        540 KB     │
│                                              │
│ Total: 2 archivos                            │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│ A  Agregar archivos                          │
│ F  Agregar carpeta                           │
│ C  Convertir                                 │
│ L  Limpiar lista                             │
│ Q  Salir                                     │
│                                              │
└──────────────────────────────────────────────┘
```

---

## Conversión

Durante la conversión se muestra el progreso en tiempo real.

```text
Convirtiendo...

██████████████████████████░░░░░░░░░░ 65%

✓ documento.pdf
✓ informe.docx
… presentación.pptx
```

---

## Resumen

Al finalizar se muestra un resumen del proceso.

```text
═══════════════════════════════════════════════════════════════

           Conversión finalizada

✔ Correctos : 12
✖ Errores   : 1
⏱ Tiempo    : 00:00:08

═══════════════════════════════════════════════════════════════
```

---

## Formatos compatibles

El programa acepta los formatos soportados por **MarkItDown**, entre ellos:

- PDF
- Word (.doc, .docx)
- Excel (.xls, .xlsx)
- PowerPoint (.ppt, .pptx)
- Markdown
- Texto (.txt)
- HTML
- XML
- JSON
- ZIP

---

## Salida

Los archivos Markdown (`.md`) se generan automáticamente en la misma carpeta del archivo original.

Si ya existe un archivo con ese nombre, se crea uno nuevo automáticamente para evitar sobrescribirlo.

Ejemplo:

```text
informe.pdf

↓

informe.md
```

Si ya existe:

```text
informe.pdf
informe.md

↓

informe_1.md
```

---

## Créditos

Este proyecto utiliza **MarkItDown** de Microsoft para realizar la conversión de documentos a Markdown.

👉 https://github.com/microsoft/markitdown

---

## Licencia

Este proyecto está distribuido bajo la licencia **MIT**.
