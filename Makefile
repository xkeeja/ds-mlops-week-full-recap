clear_remote:
	git remote remove origin

create_venv:
	pyenv virtualenv 3.10.6 mlops-recap
	pyenv local mlops-recap

install_amd64:
	pip install --upgrade pip
	pip install -e '.[amd64]'

install_m1:
	pip install --upgrade pip
	pip install -e '.[m1]'

run_api:
	uvicorn salaries.fastapi.fastapi:app --reload

docker_build:
	docker build --platform linux/amd64 -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:amd64 .

docker_build_m1:
	docker build -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:arm .

docker_run:
	docker run -it -e PORT=8000 -p 8000:8000 --env-file .env \
	-v ${GOOGLE_APPLICATION_CREDENTIALS}:/root/.config/gcloud/application_default_credentials.json \
	${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:amd64

docker_run_m1:
	docker run -it -e PORT=8000 -p 8000:8000 --env-file .env \
	-v ${GOOGLE_APPLICATION_CREDENTIALS}:/root/.config/gcloud/application_default_credentials.json \
	${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:arm

docker_push:
	docker push ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:amd64

gcloud_run:
	gcloud run deploy --image ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}:amd64 --region ${GCR_REGION} --env-vars-file .env.yaml
