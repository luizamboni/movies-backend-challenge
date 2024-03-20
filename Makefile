
start:
	cd app && python app.py

import:
	curl -i -X POST \
		-H "Content-Type: application/json" \
		-d '{"file_path_or_url": "$(shell pwd)/data/movielisst.csv"}' \
		'http://localhost:5000/import-data'

producers:
	curl -i 'http://localhost:5000/producers/intervals'

dev:
	cd app && python dev.py

test:
	cd app && pytest ../.