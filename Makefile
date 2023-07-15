.PHONY: run
run:
	(cd docs; bundle exec jekyll serve)

.PHONY: install
install:
	(cd docs; bundle)
	pip install -r requirements.txt

.PHONY: lint
lint:
	ruff check .
