PWD = $(shell pwd)

.PHONY: upload
upload:
	@echo PWD: $(PWD)
	@cd $(PWD); source $(PWD)/venv/bin/activate
	@rm -rf ./dist/*
	@python3.6 setup.py sdist build
	twine upload --verbose dist/* && rm -rf ./dist/*
