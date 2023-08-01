# Template for FastAPI project
Template with:
- poetry (fastapi, python 3.10.10, uvicorn, pre-commit, loguru and pytest)
- dockerfile - to run uvicorn server 
- docker-compose - build app in container
- pre-commit configuration - black, isort and flake8 
- folder for online documentation generation (based on Template_Swagger repository)
- github action - pytest and docker image build on push or pull request to master branch (CI/CD)