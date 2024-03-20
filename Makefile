
start:
	cd app && python app.py

import:
	curl -i -X PUT \
		-H "Content-Type: application/json" \
		-d '{"file_path_or_url": "$(shell pwd)/data/movielist.csv"}' \
		'http://localhost:5000/movies/import'

get_worst_producers:
	curl -i 'http://localhost:5000/producers/worsts'

dev:
	cd app && python dev.py

test:
	cd app && pytest ../.