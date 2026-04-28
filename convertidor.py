from moviepy import VideoFileClip
import os

carpeta = r"C:\Users\name\Videos" #en "name" pon tu nombre de usuario del ordenador, por ejemplo: C:\Users\adri\Videos

# Buscar archivos MOV
archivos_mov = [f for f in os.listdir(carpeta) if f.lower().endswith(".mov")]

if not archivos_mov:
    print("⚠️  No se encontraron archivos .mov en la carpeta.")
    exit()

print(f"📂 Se encontraron {len(archivos_mov)} archivo(s) .mov para convertir:")
for f in archivos_mov:
    print(f"   - {f}")
print()

convertidos = []
fallidos = []

for archivo in archivos_mov:
    entrada = os.path.join(carpeta, archivo)
    salida = os.path.join(carpeta, archivo.replace(".mov", ".mp4"))

    print(f"⏳ Convirtiendo: {archivo}")
    try:
        clip = VideoFileClip(entrada)
        clip.write_videofile(salida)
        clip.close()
        convertidos.append(archivo)
        print(f"✅ Listo: {archivo}\n")
    except Exception as e:
        fallidos.append((archivo, str(e)))
        print(f"❌ Error al convertir {archivo}: {e}\n")

# Resumen final
print("=" * 50)
print("📊 RESUMEN FINAL")
print("=" * 50)

if convertidos:
    print(f"\n✅ Convertidos correctamente ({len(convertidos)}):")
    for f in convertidos:
        print(f"   - {f.replace('.mov', '.mp4')}")

if fallidos:
    print(f"\n❌ Fallidos ({len(fallidos)}):")
    for f, error in fallidos:
        print(f"   - {f} → {error}")

print()
