PYTHON ?= python3.12
PY ?= .venv/bin/python
.PHONY: setup data train evaluate test offline demo
setup:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -r requirements.txt
data:
	$(PY) scripts/acquire.py
	$(PY) scripts/forecast.py
	$(PY) scripts/preprocess.py
train:
	$(PY) scripts/build_examples.py
	$(PY) scripts/train.py
evaluate:
	$(PY) scripts/evaluate.py
test:
	$(PY) -m pytest -q
offline:
	$(PY) scripts/offline_demo.py
demo:
	$(PY) -m uvicorn farmsignal.api:app --host 127.0.0.1 --port 8765
