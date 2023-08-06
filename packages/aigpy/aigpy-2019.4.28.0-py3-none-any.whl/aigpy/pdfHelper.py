import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, portrait

def imag2pdf(self, imaglist, filename):
    (maxw, maxh) = Image.open(imaglist[0]).size
    c = canvas.Canvas(filename, pagesize=(maxw, maxh))
    for item in imaglist:
        name = os.path.abspath(item)
        c.drawImage(name, 0, 0, maxw, maxh)
        c.showPage()
    c.save()
