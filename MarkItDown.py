#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

VERSION = "v1.0"
BOX_W = 78          # ancho total de la caja (incluye bordes)
INNER = BOX_W - 2   # ancho interior
BAR_W = 40          # ancho de la barra de progreso

# ─────────────────────────────────────────────────────────────
#  Compatibilidad de terminal
# ─────────────────────────────────────────────────────────────

def _supports_unicode() -> bool:
    enc = sys.stdout.encoding or ""
    try:
        "┌─│█░✓✗✔✖⏱🚀".encode(enc)
        return True
    except (UnicodeEncodeError, LookupError):
        return False


UNI = _supports_unicode()

if UNI:
    G = {
        "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
        "ml": "├", "mr": "┤", "h": "─", "v": "│",
        "sep": "─", "dbl": "═",
        "full": "█", "empty": "░",
        "ok": "✓", "bad": "✗", "ok2": "✔", "bad2": "✖",
        "clock": "⏱", "rocket": "🚀 ",
    }
else:
    G = {
        "tl": "+", "tr": "+", "bl": "+", "br": "+",
        "ml": "+", "mr": "+", "h": "-", "v": "|",
        "sep": "-", "dbl": "=",
        "full": "#", "empty": ".",
        "ok": "[OK]", "bad": "[X]", "ok2": "+", "bad2": "-",
        "clock": ">", "rocket": "",
    }

TIPOS = {
    ".pdf": "PDF", ".docx": "Word", ".doc": "Word", ".dotx": "Word",
    ".xlsx": "Excel", ".xls": "Excel", ".xlsm": "Excel",
    ".pptx": "PowerPoint", ".ppt": "PowerPoint",
    ".csv": "CSV", ".tsv": "TSV", ".json": "JSON", ".xml": "XML",
    ".html": "HTML", ".htm": "HTML", ".txt": "Texto", ".md": "Markdown",
    ".epub": "EPub", ".zip": "ZIP",
    ".jpg": "Imagen", ".jpeg": "Imagen", ".png": "Imagen", ".gif": "Imagen",
    ".wav": "Audio", ".m4a": "Audio",
}

EXT_VALIDAS = set(TIPOS.keys())

# ─────────────────────────────────────────────────────────────
#  Utilidades de dibujo
# ─────────────────────────────────────────────────────────────

def dw(s: str) -> int:
    """Ancho visual aproximado (emoji = 2 columnas)."""
    return sum(2 if ord(c) > 0x2E80 and not (0x2500 <= ord(c) <= 0x27BF) else 1 for c in s)


def pad(s: str, n: int) -> str:
    return s + " " * max(0, n - dw(s))


def cut(s: str, n: int) -> str:
    if dw(s) <= n:
        return s
    return s[: max(0, n - 1)] + "…" if UNI else s[: max(0, n - 3)] + "..."


def linea(texto: str = "") -> str:
    return G["v"] + pad(" " + texto, INNER) + G["v"]


def borde(tipo: str) -> str:
    izq, der = {"top": ("tl", "tr"), "mid": ("ml", "mr"), "bot": ("bl", "br")}[tipo]
    return G[izq] + G["h"] * INNER + G[der]


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def humano(n: int) -> str:
    for unidad in ("B", "KB", "MB", "GB"):
        if n < 1024 or unidad == "GB":
            return f"{n:.0f} {unidad}" if unidad == "B" else f"{n:.1f} {unidad}"
        n /= 1024
    return f"{n:.1f} GB"


def cronometro(seg: float) -> str:
    seg = int(seg)
    return f"{seg // 3600:02d}:{seg % 3600 // 60:02d}:{seg % 60:02d}"


def tipo_de(p: Path) -> str:
    return TIPOS.get(p.suffix.lower(), p.suffix.lstrip(".").upper() or "?")

# ─────────────────────────────────────────────────────────────
#  Pantalla principal
# ─────────────────────────────────────────────────────────────

def dibujar_menu(archivos):
    limpiar()
    titulo = f"{G['rocket']}MarkItDown Converter"
    hueco = INNER - dw(" " + titulo) - dw(VERSION) - 1

    print(borde("top"))
    print(G["v"] + " " + titulo + " " * max(1, hueco) + VERSION + " " + G["v"])
    print(borde("mid"))
    print(linea())
    print(linea("Archivos cargados"))
    print(linea())

    if not archivos:
        print(linea("  (vacío)"))
        print(linea())
    else:
        print(linea(f" {'#':<3} {pad('Nombre', 45)} {pad('Tipo', 11)} {'Tamaño'}"))
        print(linea(" " + G["sep"] * (INNER - 3)))
        for i, ruta in enumerate(archivos, 1):
            p = Path(ruta)
            try:
                size = humano(p.stat().st_size)
            except OSError:
                size = "?"
            print(linea(f" {i:<3} {pad(cut(p.name, 45), 45)} {pad(tipo_de(p), 11)} {size}"))
        print(linea())
        print(linea(f" Total: {len(archivos)} archivo{'s' if len(archivos) != 1 else ''}"))

    print(linea())
    print(borde("mid"))
    print(linea())
    for tecla, desc in [("A", "Agregar archivos"), ("F", "Agregar carpeta"),
                        ("C", "Convertir"), ("L", "Limpiar lista"), ("Q", "Salir")]:
        print(linea(f"  {tecla}  {desc}"))
    print(linea())
    print(borde("bot"))

# ─────────────────────────────────────────────────────────────
#  Entrada de archivos
# ─────────────────────────────────────────────────────────────

def normalizar(entrada: str) -> str:
    """Limpia comillas y escapes que agregan las terminales al arrastrar."""
    s = entrada.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    elif os.name != "nt":
        s = s.replace("\\ ", " ").replace("\\'", "'").replace('\\"', '"')
    return s.strip()


def agregar_archivos(archivos):
    print("\nArrastra los archivos aquí, uno por línea.")
    print("Enter en línea vacía para volver al menú.\n")
    while True:
        try:
            ruta = normalizar(input("  Archivo: "))
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not ruta:
            return
        p = Path(ruta).expanduser()
        if not p.exists():
            print(f"   {G['bad']} No existe\n")
        elif p.is_dir():
            print(f"   {G['bad']} Es una carpeta (usa la opción F)\n")
        elif str(p.resolve()) in {str(Path(a).resolve()) for a in archivos}:
            print(f"   {G['bad']} Ya está en la lista\n")
        else:
            archivos.append(str(p))
            print(f"   {G['ok']} Agregado\n")


def agregar_carpeta(archivos):
    print("\nArrastra la carpeta aquí (Enter para cancelar).\n")
    try:
        ruta = normalizar(input("  Carpeta: "))
        if not ruta:
            return
        p = Path(ruta).expanduser()
        if not p.is_dir():
            print(f"\n   {G['bad']} No es una carpeta válida")
            input("\n  Enter para continuar...")
            return
        recursivo = input("  ¿Incluir subcarpetas? [s/N]: ").strip().lower() in ("s", "si", "sí", "y")
    except (EOFError, KeyboardInterrupt):
        print()
        return

    patron = "**/*" if recursivo else "*"
    ya = {str(Path(a).resolve()) for a in archivos}
    nuevos = 0
    for f in sorted(p.glob(patron)):
        if f.is_file() and f.suffix.lower() in EXT_VALIDAS and str(f.resolve()) not in ya:
            archivos.append(str(f))
            ya.add(str(f.resolve()))
            nuevos += 1

    print(f"\n   {G['ok']} {nuevos} archivo(s) agregado(s)")
    input("\n  Enter para continuar...")

# ─────────────────────────────────────────────────────────────
#  Conversión
# ─────────────────────────────────────────────────────────────

def ruta_salida(origen: Path) -> Path:
    destino = origen.with_suffix(".md")
    if destino.resolve() == origen.resolve():
        destino = origen.with_name(origen.name + ".md")
    base, n = destino, 1
    while destino.exists():
        destino = base.with_name(f"{base.stem}_{n}{base.suffix}")
        n += 1
    return destino


def barra(pct: float) -> str:
    llenos = int(BAR_W * pct)
    return G["full"] * llenos + G["empty"] * (BAR_W - llenos)


def error_corto(res) -> str:
    txt = (res.stderr or res.stdout or "").strip()
    if not txt:
        return f"código {res.returncode}"
    ultima = txt.splitlines()[-1].strip()
    return cut(ultima, 45)


def convertir(archivos):
    resultados = []
    inicio = time.monotonic()

    for i, ruta in enumerate(archivos):
        limpiar()
        print("\nConvirtiendo...\n")
        print(f"  {barra(i / len(archivos))}  {int(i / len(archivos) * 100)}%\n")
        for nombre, ok, msg in resultados:
            print(f"  {G['ok'] if ok else G['bad']} {nombre}" + (f" ({msg})" if msg else ""))
        print(f"  … {Path(ruta).name}")

        origen = Path(ruta)
        try:
            res = subprocess.run(
                ["markitdown", str(origen), "-o", str(ruta_salida(origen))],
                capture_output=True, text=True,
                encoding="utf-8", errors="replace",
            )
            if res.returncode == 0:
                resultados.append((origen.name, True, ""))
            else:
                resultados.append((origen.name, False, error_corto(res)))
        except OSError as e:
            resultados.append((origen.name, False, cut(str(e), 45)))

    limpiar()
    print("\nConvirtiendo...\n")
    print(f"  {barra(1.0)}  100%\n")
    for nombre, ok, msg in resultados:
        print(f"  {G['ok'] if ok else G['bad']} {nombre}" + (f" ({msg})" if msg else ""))

    resumen(resultados, time.monotonic() - inicio)


def resumen(resultados, transcurrido):
    ok = sum(1 for _, e, _ in resultados if e)
    err = len(resultados) - ok
    regla = G["dbl"] * 63

    print(f"\n{regla}\n")
    print("           Conversión finalizada\n")
    print(f"   {G['ok2']} Correctos : {ok}")
    print(f"   {G['bad2']} Errores   : {err}")
    print(f"   {G['clock']} Tiempo    : {cronometro(transcurrido)}")
    print(f"\n{regla}")
    input("\n  Enter para volver al menú...")

# ─────────────────────────────────────────────────────────────
#  Bucle principal
# ─────────────────────────────────────────────────────────────

def main():
    if shutil.which("markitdown") is None:
        print(f"{G['bad']} No se encontró 'markitdown' en el PATH.")
        print("   Instálalo con:  pip install markitdown[all]")
        input("\n  Enter para salir...")
        return 1

    archivos = []
    for arg in sys.argv[1:]:  # permite arrastrar archivos sobre el script
        p = Path(arg).expanduser()
        if p.is_file():
            archivos.append(str(p))

    while True:
        dibujar_menu(archivos)
        try:
            op = input("\n  Opción: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if op == "a":
            agregar_archivos(archivos)
        elif op == "f":
            agregar_carpeta(archivos)
        elif op == "c":
            if not archivos:
                input("\n  No hay archivos cargados. Enter para continuar...")
                continue
            try:
                convertir(archivos)
            except KeyboardInterrupt:
                print("\n\n  Conversión cancelada.")
                input("\n  Enter para continuar...")
        elif op == "l":
            archivos.clear()
        elif op == "q":
            return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
