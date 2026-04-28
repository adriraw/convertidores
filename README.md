# 🛠️ Convertidores

Colección de scripts de Python para convertir y descargar archivos multimedia de forma sencilla desde la terminal.

---

## 📦 Scripts disponibles

| Script | Función |
|---|---|
| `convertidor.py` | Convierte archivos `.mov` a `.mp4` |
| `youtube_mp3.py` | Descarga audio de YouTube en `.mp3` |
| `youtube_mp4.py` | Descarga vídeo de YouTube en `.mp4` |
| `convertir_imagenes.py` | Convierte imágenes a `.webp` o `.avif` |

---

## ⚙️ Requisitos

- Python 3.10 o superior
- pip

---

## 🎬 convertidor.py — MOV a MP4

Convierte todos los archivos `.mov` de una carpeta a `.mp4` usando `moviepy`.

### Instalación

```bash
pip install moviepy
```

### Configuración

Abre el script y cambia la ruta de la carpeta:

```python
carpeta = r"C:\Users\TU_USUARIO\Videos"
```

### Uso

```bash
python convertidor.py
```

El script busca todos los `.mov` en la carpeta, los convierte y guarda los `.mp4` en la misma ubicación. Al finalizar muestra un resumen con los archivos convertidos y los posibles errores.

---

## 🎵 youtube_mp3.py — YouTube a MP3

Descarga el audio de un vídeo de YouTube y lo guarda como `.mp3` a 192 kbps.

### Instalación

```bash
pip install yt-dlp
```

> El script instala `yt-dlp` automáticamente si no lo tienes.

### Configuración

Abre el script y cambia la carpeta de destino:

```python
carpeta_destino = r"C:\Users\TU_USUARIO\Music"
```

### Uso

```bash
python youtube_mp3.py https://www.youtube.com/watch?v=XXXXX
```

---

## 🎥 youtube_mp4.py — YouTube a MP4

Descarga un vídeo de YouTube en la mejor calidad disponible en formato `.mp4`.

### Instalación

```bash
pip install yt-dlp
```

> El script instala `yt-dlp` automáticamente si no lo tienes.

### Configuración

Abre el script y cambia la carpeta de destino:

```python
carpeta_destino = r"C:\Users\TU_USUARIO\Videos"
```

### Uso

```bash
python youtube_mp4.py https://www.youtube.com/watch?v=XXXXX
```

---

## 🖼️ convertir_imagenes.py — Imágenes a WebP / AVIF

Convierte imágenes desde cualquier formato (JPG, PNG, BMP, TIFF...) a `.webp` o `.avif`. Funciona de forma interactiva: pregunta paso a paso qué convertir, con qué calidad y dónde guardar.

### Instalación

```bash
pip install Pillow
```

### Uso

```bash
python convertir_imagenes.py
```

El script te irá preguntando:

1. Ruta de la imagen o carpeta
2. Si convertir todas, una sola, o una selección manual
3. Formato de salida (WebP o AVIF)
4. Calidad (1-100, recomendado 85)
5. Ancho máximo en píxeles (opcional, útil para fotos de móvil)
6. Carpeta de destino

---

## 📝 Notas

- Los scripts de YouTube requieren conexión a internet y que el vídeo sea público.
- `convertidor.py` re-encodea el vídeo, por lo que puede tardar varios minutos según el tamaño.
- Para imágenes de iPhone (4032×3024px) se recomienda usar `--ancho-max 1600` para reducir el peso significativamente.
- AVIF ofrece mejor compresión que WebP pero tiene menos compatibilidad con navegadores antiguos.

---

## 📄 Licencia

MIT License
