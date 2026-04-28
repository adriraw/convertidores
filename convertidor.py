from moviepy.editor import VideoFileClip
import os

carpeta = r"ruta/a/tu/carpeta"  # Change this for ur route to the folder with .mov files

for archivo in os.listdir(carpeta):
    if archivo.endswith(".mov"):
        entrada = os.path.join(carpeta, archivo)
        salida = os.path.join(carpeta, archivo.replace(".mov", ".mp4"))
        
        print(f"Convirtiendo: {archivo}")
        clip = VideoFileClip(entrada)
        clip.write_videofile(salida)
        clip.close()
        print(f"✅ Listo: {salida}")

print("All archives converted!")