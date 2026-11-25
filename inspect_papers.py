from pathlib import Path
import json
import re
import pypdfium2 as pdfium
import pdfplumber
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent
items = []
for path in sorted((ROOT / 'papers').glob('*.pdf')):
    if b'%%EOF' not in path.read_bytes()[-2048:]:
        print(path.stem, 'still downloading')
        continue
    image_path = ROOT / 'pages' / (path.stem + '.png')
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ''
        lines = page.extract_text_lines()
        captions = [line for line in lines if re.match(r'^(Fig\.?\s*1\b|Figure\s*1\b)', line['text'])]
        (ROOT / 'pages' / (path.stem + '.txt')).write_text('\n\n'.join(p.extract_text() or '' for p in pdf.pages[:2]))
        info = {'id': path.stem, 'size': [page.width, page.height], 'caption_lines': captions, 'header': text[:600]}
        items.append(info)
        print(json.dumps(info, ensure_ascii=False))
    if not image_path.exists():
        doc = pdfium.PdfDocument(path)
        page = doc[0]
        page.render(scale=2).to_pil().convert('RGB').save(image_path)
        page.close()
        doc.close()

for group in range(0, len(items), 5):
    subset = items[group:group+5]
    sheet = Image.new('RGB', (500*len(subset), 700), '#d9dfe5')
    draw = ImageDraw.Draw(sheet)
    for i, item in enumerate(subset):
        im = Image.open(ROOT / 'pages' / (item['id'] + '.png'))
        im.thumbnail((490, 660))
        sheet.paste(im, (i*500+(500-im.width)//2, 30))
        draw.text((i*500+12, 8), item['id'], fill='black')
    sheet.save(ROOT / 'pages' / f'contact_{group//5+1}.jpg')
(ROOT / 'pages' / 'inspection.json').write_text(json.dumps(items, ensure_ascii=False, indent=2))
