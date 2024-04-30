run:
	source .venv/bin/activate
	python -m fazbot

install:
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	cp config-example example

lint:
	pylint fazbot\ --disable=R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,W

linttest:
	pylint tests\ --disable=R0901,R0913,R0916,R0912,R0902,R0914,R01702,R0917,R0904,R0911,R0915,R0903,C0301,C0114,C0115,C0116,W
