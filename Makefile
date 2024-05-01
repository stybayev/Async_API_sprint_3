admin-dev:
	docker-compose -f docker-compose-dev.yaml exec django-api make admin


run-dev:
	docker-compose -f docker-compose-dev.yaml up -d

stop-dev:
	docker-compose -f docker-compose-dev.yaml down --volumes
	docker-compose -f docker-compose-dev.yaml down

rm-dev:
	docker-compose -f docker-compose-dev.yaml rm
	
build-dev:
	docker-compose -f docker-compose-dev.yaml build
