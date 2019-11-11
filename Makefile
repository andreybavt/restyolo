SHELL = /bin/bash

install:
	python3 -m venv env;
	source env/bin/activate; \
	pip install -r requirements.txt; \
	pip install -r pytorch_yolov3/requirements.txt; \
	cd pytorch_yolov3/weights && chmod +x download_weights.sh
	cd pytorch_yolov3/weights && ./download_weights.sh
	chmod +x run.sh;