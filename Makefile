.DEFAULT_GOAL := help

PYTHONPATH=
SHELL=/bin/zsh
VENV=.venv

ifeq ($(OS),Windows_NT)
	VENV_BIN=$(VENV)/Scripts
else
	VENV_BIN=$(VENV)/bin
endif

.venv:  ## Set up Python virtual environment and install requirements
	python3 -m venv $(VENV)
	$(MAKE) requirements

.PHONY: requirements
requirements: .venv ## Install/refresh Python project requirements
	@echo "Installing core project dependencies..."
	$(VENV_BIN)/pip install --upgrade -r requirements.txt
	@echo "Installing project dependencies for development..."
	$(VENV_BIN)/pip install --upgrade -r requirements-dev.txt \
	&& $(VENV_BIN)/pip install --upgrade -r requirements-lint.txt \

.PHONY: run
run: ## Run the app locally
	@echo "Running app locally..."
	$(VENV_BIN)/streamlit run app/app/Welcome.py

# TODO: fix this, since the if conditional is not working. might need to change it to Makefile syntax iso shell syntax
# .PHONY: run-docker
# run-docker: ## Run the app in a Docker container
# 	@if [ "$(docker images -q hst-streamlit 2> /dev/null)" == "" ]; then \
# 		@echo "Docker image does not exist! \
# 		@echo Building Docker image..." \
#   		docker build -t hst-streamlit . \
# 	fi
# 	@echo "Running app in Docker container..."
# 	docker run -p 8501:8501 hst-streamlit

.PHONY: test
test: ## Test the project
	@echo "Running tests..."
	$(VENV_BIN)/python -m pytest tests/ 

.PHONY: coverage
coverage: ## Generate coverage report
	@echo "Generating coverage report..."
	$(VENV_BIN)/coverage run -m pytest tests/ \
	&& $(VENV_BIN)/coverage report -m

.PHONY: lint
lint:  ## Run autoformatting, linting, and static type checking
	$(VENV_BIN)/black .
	$(VENV_BIN)/ruff check
	$(VENV_BIN)/typos
	$(VENV_BIN)/mypy .

.PHONY: clean
clean:  ## Clean up caches and virtual environment
	@rm -rf .ruff_cache/
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf .coverage
	@rm -rf yfinance.cache
	@rm -rf http_cache.sqlite
	@rm -rf .venv/

.PHONY: help
help:  ## Display this help screen
	@echo "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}' | sort
