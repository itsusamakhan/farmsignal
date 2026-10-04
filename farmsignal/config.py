from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BBOX = (73.04, 30.59, 73.06, 30.61)  # west, south, east, north; demonstration area near Sahiwal, Punjab, Pakistan
REGION = 'Sahiwal, Punjab, Pakistan'
DEMO_FARM = (30.60, 73.05)  # lat, lon of the fictional demonstration registration
OUTSIDE_FARM = (31.52, 74.35)  # Lahore: outside the saved area
DB = ROOT / 'data/cache.sqlite'
PROPERTIES = {'phh2o': (10, 'pH'), 'sand': (10, '%'), 'silt': (10, '%'), 'clay': (10, '%'), 'soc': (10, 'g/kg'), 'cec': (10, 'cmol(c)/kg'), 'cfvo': (10, 'vol%'), 'bdod': (100, 'kg/dm3')}
DEPTHS = ['0-5cm', '5-15cm', '15-30cm']
IGH = '+proj=igh +datum=WGS84 +units=m +no_defs'
