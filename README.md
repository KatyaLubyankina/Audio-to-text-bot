# How to build project for development?
Clone github repositiory
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
