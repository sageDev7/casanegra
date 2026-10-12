"""Logo de Casanegra desde el badge circular que mandó Axel (logo-original.png, no se toca).
- Fondo navy estimado con una superficie cuadrática; los elementos claros (oro y blanco) se separan
  con 'aclarar a alfa' respecto de ese fondo. Lo más oscuro que el fondo (la puntita negra de la
  balanza, un error del original) se descarta. Los anillos del círculo quedan afuera (radio > 380).
- Salida: logo.png = CASANEGRA / línea con puntos / & ASOCIADOS (sin balanza ni «ESTUDIO JURÍDICO», pedido de Axel)."""
import os
import numpy as np
from PIL import Image
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = np.array(Image.open(os.path.join(D, "logo-original.png")).convert("RGB")).astype(float)
H, W, _ = im.shape
yy, xx = np.mgrid[0:H, 0:W]
lum = im.mean(2)
r = np.hypot(xx - W / 2, yy - H / 2)

# fondo: píxeles navy (oscuros y azulados) -> superficie cuadrática por canal
sel = (lum < 80) & (im[..., 2] > im[..., 0] + 25)
F = lambda x, y: np.stack([np.ones_like(x), x / W, y / H, (x / W) ** 2, (y / H) ** 2, x * y / (W * H)], -1)
bg = np.zeros_like(im)
for c in range(3):
    coef, *_ = np.linalg.lstsq(F(xx[sel], yy[sel]), im[..., c][sel], rcond=None)
    bg[..., c] = F(xx, yy) @ coef
bg = bg.clip(0, 254)

a = ((im - bg) / (255 - bg)).max(2).clip(0, 1)          # cuánto se "aclara" respecto del fondo
a = np.where(a < 0.06, 0, (a - 0.06) / 0.94)
a[r > 380] = 0                                           # sin los anillos del badge
# la puntita negra arriba del fiel de la balanza (error del original): se borra con su contorno
a[(yy < 247) & (abs(xx - W / 2) < 30)] = 0
col = np.where(a[..., None] > 0, bg + (im - bg) / np.maximum(a[..., None], 1e-3), 0).clip(0, 255)
full = Image.fromarray(np.dstack([col, a * 255]).astype(np.uint8), "RGBA")

# piezas por franjas horizontales
rows = np.where((a > 0.15).sum(1) > 2)[0]
bands, start = [], rows[0]
for i in range(1, len(rows)):
    if rows[i] - rows[i - 1] > 8:
        bands.append((start, rows[i - 1])); start = rows[i]
bands.append((start, rows[-1]))
print("franjas:", bands)

def crop(y0, y1, x0=0, x1=W):
    p = full.crop((x0, y0 - 2, x1, y1 + 3)); return p.crop(p.getbbox())

# esperado: [balanza+línea], [CASANEGRA], [línea con puntos], [& ASOCIADOS], [ESTUDIO JURÍDICO]
# Axel pidió el logo SIN la balanza y SIN «ESTUDIO JURÍDICO»: solo CASANEGRA / línea / & ASOCIADOS.
bal, nom, lin, aso, est = bands[:5]
casa, line, asoc = crop(*nom), crop(*lin), crop(*aso)
w = max(casa.width, line.width, asoc.width)
g1, g2 = 22, 18
logo = Image.new("RGBA", (w, casa.height + g1 + line.height + g2 + asoc.height), (0, 0, 0, 0))
y = 0
for p, g in ((casa, g1), (line, g2), (asoc, 0)):
    logo.alpha_composite(p, ((w - p.width) // 2, y)); y += p.height + g
logo.save(os.path.join(D, "logo.png"))
print("logo.png", logo.size)
