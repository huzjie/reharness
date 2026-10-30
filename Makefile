.PHONY: doctor bench test install clean serve

doctor:
	python -m reharness doctor

bench:
	python -m reharness bench

test:
	python -m unittest discover -s tests -t .

install:
	python -m pip install -e .

serve:
	python -m reharness serve --port 8790

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
