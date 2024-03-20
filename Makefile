# APP_HOST=192.168.65.3
APP_HOST=localhost

build-image:
	cd app && docker build -t movies .

run-image:
	docker run \
		--rm \
		-p 5000:5000 \
		-v $(shell pwd)/data/:/data/ \
		movies

start:
	cd app && python app.py

import:
	curl -i -X PUT \
		-H "Content-Type: application/json" \
		-d '{"file_path_or_url": "/data/movielist.csv"}' \
		'http://${APP_HOST}:5000/movies/import'

get_worst_producers:
	curl -i 'http://${APP_HOST}:5000/producers/worsts'

dev:
	cd app && python dev.py

test:
	cd app && pytest ../.