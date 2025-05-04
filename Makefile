# Make file for Guardian Data Streaming Project


# Vars
PROJECT_NAME := guardian-data-streaming-project
PYTHON_INTERPRETER := python3
WD := $(shell pwd)
PYTHONPATH := $(WD)
SHELL := /bin/bash
PIP := $(PYTHON_INTERPRETER) -m pip

ACTIVATE_ENV := source ./venv/bin/activate

define execute_in_env
	$(ACTIVATE_ENV) && $1
endef

create-environment:
	@echo ">>> Creating environment for $(PROJECT_NAME)..."
	@set -e; \
	if [ ! -d "venv" ]; then \
		$(PYTHON_INTERPRETER) --version; \
		$(PIP) install -q virtualenv; \
		virtualenv venv --python=$(PYTHON_INTERPRETER); \
	else \
		echo "Virtual environment already exists, skipping creation."; \
	fi

# Install project dependencies
requirements: create-environment
	$(call execute_in_env, $(PIP) install -r requirements.txt)

# Install Bandit for security analysis
bandit:
	$(call execute_in_env, $(PIP) install bandit)

# Install Black for code formatting
black:
	$(call execute_in_env, $(PIP) install black)

# Install Flake8 for linting
flake8:
	$(call execute_in_env, $(PIP) install flake8)

# Install Coverage for code coverage analysis
coverage:
	$(call execute_in_env, $(PIP) install coverage)

# Set up development tools (Black, Coverage)
dev-setup: bandit black flake8 coverage

# Run Bandit for security checks
run-bandit:
	$(call execute_in_env, bandit -r -lll ./src ./tests)

# Format code with Black
run-black:
	$(call execute_in_env, black ./src/*.py ./tests/*.py)

# Run Flake8 to check code style
run-flake8:
	$(call execute_in_env, flake8 ./src ./tests)

# Run the tests
run-test:
	$(call execute_in_env, PYTHONPATH=$(PYTHONPATH)/src pytest -v)

# Run the coverage check
check-coverage:
	$(call execute_in_env, PYTHONPATH=$(PYTHONPATH)/src pytest --cov=src tests/)

# Run all checks (code formatting, unit tests, and coverage)
run-checks: run-bandit run-black run-flake8 run-test check-coverage


# Remove virtual environment, coverage, pycache, and other generated files
clean:
	rm -rf venv .coverage .pytest_cache */__pycache__
