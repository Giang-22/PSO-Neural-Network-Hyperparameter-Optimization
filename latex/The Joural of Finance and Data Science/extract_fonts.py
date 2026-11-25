import fitz
from collections import Counter

pdf_path = r'd:\Code\JupyterNotebook\PSO\references\The Joural of Finance and Data Science\Deep learning and the international capital asset pricing model.pdf'
doc = fitz.open(pdf_path)

font_counts = Counter()
font_sizes = Counter()
style_samples = {}

for page_idx in range(len(doc)):
    page = doc[page_idx]
    blocks = page.get_text('dict')['blocks']
    for b in blocks:
        if 'lines' in b:
            for l in b['lines']:
                for s in l['spans']:
                    fn = s['font']
                    sz = round(s['size'], 2)
                    text = s['text'].strip()
                    if text:
                        font_counts[fn] += len(text)
                        font_sizes[(fn, sz)] += len(text)
                        if (fn, sz) not in style_samples and len(text) > 5:
                            style_samples[(fn, sz)] = text[:60]

print('=== Top Fonts by Character Count ===')
for fn, cnt in font_counts.most_common(15):
    print(f'{fn:35s}: {cnt:6d} chars')

print('\n=== Top Font + Size Combinations ===')
for (fn, sz), cnt in font_sizes.most_common(25):
    sample = style_samples.get((fn, sz), '')
    print(f'{fn:30s} {sz:5.2f} pt ({cnt:5d} chars): "{sample}"')
