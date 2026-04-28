import subprocess
import sys

# Instalar yt-dlp si no está instalado
try:
    import yt_dlp
except ImportError:
    print("⏳ Instalando yt-dlp...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

carpeta_destino = r"C:\Users\name\Music" #en "name" pon tu nombre de usuario del ordenador, por ejemplo: C:\Users\adri\Videos

if len(sys.argv) < 2:
    print("❌ Debes pasar la URL como argumento.")
    print("   Uso: python youtube_mp3.py https://www.youtube.com/watch?v=XXXXX")
    sys.exit(1)

url = sys.argv[1].strip()

opciones = {
    'format': 'bestaudio/best',
    'outtmpl': carpeta_destino + r'\%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

print("\n⏳ Descargando...")

try:
    with yt_dlp.YoutubeDL(opciones) as ydl:
        info = ydl.extract_info(url, download=True)
        titulo = info.get('title', 'archivo')
    print(f"\n✅ Descargado correctamente: {titulo}.mp3")
    print(f"📂 Guardado en: {carpeta_destino}")
except Exception as e:
    print(f"\n❌ Error al descargar: {e}")
