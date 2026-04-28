"""
Convertidor interactivo de imágenes a WebP o AVIF
Uso:
    python convertir_imagenes.py
"""

import sys
from pathlib import Path
from PIL import Image

FORMATOS_ENTRADA = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp", ".avif"}

SEP = "─" * 50


def preguntar(pregunta: str, opciones: list[str], por_defecto: int = 0) -> str:
    print(f"\n  {pregunta}")
    for i, op in enumerate(opciones):
        marca = "▶" if i == por_defecto else " "
        print(f"  {marca} [{i + 1}] {op}")
    while True:
        resp = input(f"\n  Elige (1-{len(opciones)}) [Enter = {por_defecto + 1}]: ").strip()
        if resp == "":
            return opciones[por_defecto]
        if resp.isdigit() and 1 <= int(resp) <= len(opciones):
            return opciones[int(resp) - 1]
        print("  Opción no válida, inténtalo de nuevo.")


def preguntar_numero(pregunta: str, minimo: int, maximo: int, por_defecto: int) -> int:
    while True:
        resp = input(f"\n  {pregunta} [{minimo}-{maximo}] (Enter = {por_defecto}): ").strip()
        if resp == "":
            return por_defecto
        if resp.isdigit() and minimo <= int(resp) <= maximo:
            return int(resp)
        print(f"  Introduce un número entre {minimo} y {maximo}.")


def preguntar_ruta(pregunta: str) -> Path:
    while True:
        resp = input(f"\n  {pregunta}\n  > ").strip().strip('"').strip("'")
        ruta = Path(resp)
        if ruta.exists():
            return ruta
        print(f"  No se encontró: {ruta}")


def listar_imagenes(carpeta: Path) -> list[Path]:
    return sorted([f for f in carpeta.rglob("*") if f.suffix.lower() in FORMATOS_ENTRADA])


def elegir_imagenes(carpeta: Path) -> list[Path]:
    todas = listar_imagenes(carpeta)
    if not todas:
        print(f"\n  No se encontraron imágenes en '{carpeta}'")
        sys.exit(1)

    modo = preguntar(
        "¿Qué imágenes quieres convertir?",
        [
            f"Todas las imágenes de la carpeta ({len(todas)} encontradas)",
            "Solo una imagen específica",
            "Seleccionar varias imágenes manualmente",
        ],
    )

    if modo.startswith("Todas"):
        return todas

    if modo.startswith("Solo una"):
        print(f"\n  Imágenes disponibles en '{carpeta}':")
        for i, f in enumerate(todas):
            print(f"  [{i + 1:>2}] {f.name}")
        while True:
            resp = input("\n  Número de imagen: ").strip()
            if resp.isdigit() and 1 <= int(resp) <= len(todas):
                return [todas[int(resp) - 1]]
            print("  Número no válido.")

    # Selección múltiple manual
    print(f"\n  Imágenes disponibles en '{carpeta}':")
    for i, f in enumerate(todas):
        print(f"  [{i + 1:>2}] {f.name}")
    print("\n  Escribe los números separados por comas (ej: 1,3,5)")
    while True:
        resp = input("  > ").strip()
        try:
            indices = [int(x.strip()) for x in resp.split(",")]
            if all(1 <= idx <= len(todas) for idx in indices):
                seleccion = [todas[idx - 1] for idx in indices]
                print(f"\n  Seleccionadas: {len(seleccion)} imágenes")
                return seleccion
        except ValueError:
            pass
        print("  Formato no válido. Ejemplo: 1,3,5")


def convertir(imagen_path: Path, formato: str, calidad: int, ancho_max: int | None, carpeta_salida: Path | None) -> dict:
    try:
        with Image.open(imagen_path) as img:
            if img.mode in ("RGBA", "LA", "PA"):
                fondo = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "PA":
                    img = img.convert("RGBA")
                fondo.paste(img, mask=img.split()[-1])
                img = fondo
            elif img.mode != "RGB":
                img = img.convert("RGB")

            if ancho_max and img.width > ancho_max:
                ratio = ancho_max / img.width
                img = img.resize((ancho_max, int(img.height * ratio)), Image.LANCZOS)

            if carpeta_salida:
                carpeta_salida.mkdir(parents=True, exist_ok=True)
                ruta_salida = carpeta_salida / (imagen_path.stem + f".{formato}")
            else:
                ruta_salida = imagen_path.with_suffix(f".{formato}")

            tamaño_original = imagen_path.stat().st_size
            img.save(ruta_salida, formato.upper(), quality=calidad)
            tamaño_nuevo = ruta_salida.stat().st_size
            ahorro = round((1 - tamaño_nuevo / tamaño_original) * 100, 1)

            return {
                "ok": True,
                "salida": ruta_salida,
                "original_kb": round(tamaño_original / 1024, 1),
                "nuevo_kb": round(tamaño_nuevo / 1024, 1),
                "ahorro": ahorro,
            }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    print(f"\n  {SEP}")
    print("  Convertidor de imágenes → WebP / AVIF")
    print(f"  {SEP}")

    # 1. Ruta de entrada
    ruta = preguntar_ruta("Ruta de la imagen o carpeta:")

    if ruta.is_file():
        if ruta.suffix.lower() not in FORMATOS_ENTRADA:
            print(f"\n  Formato no soportado: {ruta.suffix}")
            sys.exit(1)
        archivos = [ruta]
    else:
        archivos = elegir_imagenes(ruta)

    # 2. Formato de salida
    formato_elegido = preguntar(
        "Formato de salida:",
        ["WebP  (compatible con todos los navegadores)", "AVIF  (mejor compresión, soporte moderno)"],
    )
    formato = "webp" if formato_elegido.startswith("WebP") else "avif"

    # 3. Calidad
    calidad = preguntar_numero("Calidad de compresión:", 1, 100, 85)

    # 4. Ancho máximo (opcional)
    redimensionar = preguntar("¿Redimensionar imágenes?", ["No, mantener tamaño original", "Sí, definir ancho máximo"])
    ancho_max = None
    if redimensionar.startswith("Sí"):
        ancho_max = preguntar_numero("Ancho máximo en píxeles:", 50, 8000, 1920)

    # 5. Carpeta de salida
    destino = preguntar(
        "¿Dónde guardar las imágenes convertidas?",
        ["En la misma carpeta que el original", "En una carpeta de salida separada"],
    )
    carpeta_salida = None
    if destino.startswith("En una carpeta"):
        nombre = input("\n  Nombre de la carpeta de salida (Enter = 'convertidas'): ").strip()
        carpeta_salida = Path(nombre if nombre else "convertidas")

    # 6. Resumen antes de convertir
    print(f"\n  {SEP}")
    print(f"  Imágenes a convertir : {len(archivos)}")
    print(f"  Formato              : .{formato}")
    print(f"  Calidad              : {calidad}%")
    print(f"  Ancho máximo         : {f'{ancho_max}px' if ancho_max else 'sin límite'}")
    print(f"  Destino              : {carpeta_salida if carpeta_salida else 'misma carpeta'}")
    print(f"  {SEP}")

    confirmar = input("\n  ¿Continuar? (Enter = sí / n = cancelar): ").strip().lower()
    if confirmar == "n":
        print("\n  Cancelado.\n")
        sys.exit(0)

    # 7. Conversión
    print()
    ok = err = 0
    for archivo in archivos:
        resultado = convertir(archivo, formato, calidad, ancho_max, carpeta_salida)
        if resultado["ok"]:
            signo = "-" if resultado["ahorro"] >= 0 else "+"
            print(f"  ✓  {archivo.name}")
            print(f"     {resultado['original_kb']} KB → {resultado['nuevo_kb']} KB  ({signo}{abs(resultado['ahorro'])}%)")
            print(f"     → {resultado['salida']}\n")
            ok += 1
        else:
            print(f"  ✗  {archivo.name}  →  Error: {resultado['error']}\n")
            err += 1

    print(f"  {SEP}")
    print(f"  Completado: {ok} convertidas, {err} errores")
    print(f"  {SEP}\n")


if __name__ == "__main__":
    main()
