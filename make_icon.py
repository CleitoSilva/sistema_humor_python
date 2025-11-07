from PIL import Image

# abre sua imagem PNG
im = Image.open("icon.png").convert("RGBA")

# tamanhos múltiplos pro .ico (fica nítido em vários lugares do Windows)
sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

im.save("icon.ico", sizes=sizes)
print("✅ Gerado icon.ico com sucesso!")