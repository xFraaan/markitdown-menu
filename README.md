# MarkItDown Menu

Una interfaz de terminal para **MarkItDown** que permite convertir múltiples archivos a **Markdown** de forma sencilla mediante un menú interactivo.

## Características

- 📄 Agregar archivos individuales o carpetas completas.
- 📂 Escaneo opcional de subcarpetas.
- 📊 Barra de progreso durante la conversión.
- ✅ Resumen de archivos convertidos y errores.
- 💻 Compatible con Windows, Linux y macOS.

## Requisitos

- Python 3.10+
- MarkItDown

Instala MarkItDown:

```bash
pip install "markitdown[all]"
```

## Uso

```bash
python MarkItDown.py
```

## Menú

```
A → Agregar archivos
F → Agregar carpeta
C → Convertir
L → Limpiar lista
Q → Salir
```

Los archivos `.md` se generan automáticamente en la misma carpeta del archivo original.

## Créditos

Este proyecto utiliza **MarkItDown** de Microsoft para realizar la conversión de documentos a Markdown. :contentReference[oaicite:0]{index=0}

## Licencia

MIT
