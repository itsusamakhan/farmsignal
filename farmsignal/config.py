from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BBOX = (34.99, 1.01, 35.01, 1.03)  # west, south, east, north; demonstration near Kitale
DB = ROOT / 'data/cache.sqlite'
PROPERTIES = {'phh2o': (10, 'pH'), 'sand': (10, '%'), 'silt': (10, '%'), 'clay': (10, '%'), 'soc': (10, 'g/kg'), 'cec': (10, 'cmol(c)/kg'), 'cfvo': (10, 'vol%'), 'bdod': (100, 'kg/dm3')}
DEPTHS = ['0-5cm', '5-15cm', '15-30cm']
IGH = '+proj=igh +datum=WGS84 +units=m +no_defs'
