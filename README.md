# Audio-to-text bot
This telegram bot allows users to send a link for video to [telegram bot](https://t.me/audio_to_text_tg_bot) and get analytics on audio track.

**Features**:
- [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10) - framework for API
- [Uvicorn](https://www.uvicorn.org/) - for ASGI web server
- [pytelegrambotapi](https://pypi.org/project/pyTelegramBotAPI/) - for telegram bot
- [Rabbitmq](https://www.rabbitmq.com/) - message broker
- [Pika](https://pika.readthedocs.io/en/stable/) - implementation of the AMQP 0-9-1 protocol for RabbitMQ
- [Pydantic-settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/) - for project settings with data validation
- [Docker Compose](https://docs.docker.com/compose/) - for running application (containers for application, rabbitmq, workers and bot)
- [Pytest](https://docs.pytest.org/en/latest/) - for tests with pytest fixtures
- CI/CD pipeline: Github action for pytest and docker image build before pull request in main
- [Poetry](https://python-poetry.org/) - for packaging and dependency management
- [Loguru](https://loguru.readthedocs.io/en/stable/api/logger.html) - for logging errors
- [Pre-commit](https://pre-commit.com/) - black, flake8 and isort formate code before each commit
## Getting started
You need to add secret data in src/secrets directory before building project: bot token from [BotFather](https://telegram.me/BotFather) and username and password for rabbitmq management.
Then run this command to start project using docker.
```Shell
docker-compose up --build
```
## How to build project for development?
Clone github repository
```Shell
git clone https://github.com/KatyaLubyankina/Audio-to-text-bot.git
```
Change directory to Audio-to-text-bot
```Shell
cd Audio-to-text-bot
```
Start conda environment from environment_droplet.yml
```Shell
conda env create -f environment_droplet.yml
```
Activate conda environment
```Shell
conda activate condaenv
```
Add configuration for poetry
```Shell
poetry config virtualenvs.in-project false --local
poetry config virtualenvs.path <your path to anaconda>/anaconda3/envs --local
```
Install packages with poetry
```Shell
poetry install
```
Run this command to set up the git hooks scripts
```Shell
pre-commit install
```
Call pre-commit command to initialize environment for pre-commit-hooks.
```Shell
pre-commit
```
## FastAPI endpoints
