install:
	python3 -m venv env2;
	source env2/bin/activate; \
	pip install -r requirements.txt; \
	cd pytorch_yolov3/weights && chmod +x download_weights.sh
	cd pytorch_yolov3/weights && ./download_weights.sh
	chmod +x run.sh;