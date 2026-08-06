# test_api_project — quick pytest / Allure runners
#
# Requires: make (Git Bash / WSL / Chocolatey), Python venv, allure CLI
#
# Examples:
#   make help
#   make test
#   make critical
#   make post
#   make marker M=security
#   make file F=tests/test_memes_get.py
#   make allure

.PHONY: help install install-dev test lint mypy \
	pre-commit pre-commit-run pre-commit-install \
	critical medium security \
	authorize get post put delete e2e \
	marker file failed last allure allure-gen clean

PYTHON ?= python
PYTEST ?= $(PYTHON) -m pytest
PRE_COMMIT ?= $(PYTHON) -m pre_commit
ALLURE_DIR ?= allure-results
ALLURE_REPORT ?= allure-report

.DEFAULT_GOAL := help

help: ## Show available targets
	@echo Available targets:
	@echo   make install             - install dependencies from requirements.txt
	@echo   make install-dev         - install runtime + mypy/pre-commit + git hooks
	@echo   make lint                - run mypy
	@echo   make mypy                - alias for lint
	@echo   make pre-commit          - run all pre-commit hooks on all files
	@echo   make pre-commit-run      - alias for pre-commit
	@echo   make pre-commit-install  - install git hooks only
	@echo   make test                - run all tests
	@echo   make critical            - only @pytest.mark.critical
	@echo   make medium              - only @pytest.mark.medium
	@echo   make security            - only @pytest.mark.security
	@echo   make authorize           - tests/test_memes_authorize.py
	@echo   make get                 - tests/test_memes_get.py
	@echo   make post                - tests/test_memes_post.py
	@echo   make put                 - tests/test_memes_update.py
	@echo   make delete              - tests/test_memes_delete.py
	@echo   make e2e                 - tests/test_e2e_meme_full_cycle.py
	@echo   make marker M=...        - custom marker     (make marker M=critical)
	@echo   make file F=...          - specific file     (make file F=tests/test_memes_get.py)
	@echo   make failed              - rerun failed only (--lf)
	@echo   make last                - stop on first failure (-x)
	@echo   make allure              - generate and open Allure report
	@echo   make allure-gen          - generate report without serve
	@echo   make clean               - remove caches and report artifacts

install: ## Install dependencies
	$(PYTHON) -m pip install -r requirements.txt

install-dev: install ## Install runtime + dev tooling
	$(PYTHON) -m pip install -r requirements-dev.txt
	$(PRE_COMMIT) install

lint: ## Run mypy type checks
	$(PYTHON) -m mypy

mypy: lint ## Alias for lint

pre-commit-install: ## Install pre-commit git hooks
	$(PRE_COMMIT) install

pre-commit-run: ## Run all pre-commit hooks on all files
	$(PRE_COMMIT) run --all-files

pre-commit: pre-commit-run ## Alias for pre-commit-run

test: ## Run all tests
	$(PYTEST)

critical: ## Critical tests
	$(PYTEST) -m critical

medium: ## Medium-priority tests
	$(PYTEST) -m medium

security: ## Security tests
	$(PYTEST) -m security

authorize: ## Authorization tests
	$(PYTEST) tests/test_memes_authorize.py

get: ## GET meme tests
	$(PYTEST) tests/test_memes_get.py

post: ## POST meme tests
	$(PYTEST) tests/test_memes_post.py

put: ## PUT meme tests
	$(PYTEST) tests/test_memes_update.py

delete: ## DELETE meme tests
	$(PYTEST) tests/test_memes_delete.py

e2e: ## E2E full meme lifecycle
	$(PYTEST) tests/test_e2e_meme_full_cycle.py

marker: ## Custom marker: make marker M=security
ifndef M
	$(error Provide a marker: make marker M=critical)
endif
	$(PYTEST) -m "$(M)"

file: ## Specific file: make file F=tests/test_memes_get.py
ifndef F
	$(error Provide a file: make file F=tests/test_memes_get.py)
endif
	$(PYTEST) "$(F)"

failed: ## Rerun only failed tests
	$(PYTEST) --lf --last-failed-no-failures none

last: ## Stop on first failure
	$(PYTEST) -x

allure-gen: ## Generate Allure HTML report
	allure generate $(ALLURE_DIR) -o $(ALLURE_REPORT) --clean

allure: allure-gen ## Generate and open Allure report
	allure open $(ALLURE_REPORT)

clean: ## Remove pytest caches and Allure artifacts
	-$(PYTHON) -c "import shutil, pathlib; \
paths=['.pytest_cache','allure-results','allure-report','htmlcov','_site','previous-history','allure-history-folder']; \
[shutil.rmtree(p, ignore_errors=True) for p in paths]; \
[p.unlink(missing_ok=True) for p in pathlib.Path('.').rglob('*.pyc')]"
	@echo Clean done.
