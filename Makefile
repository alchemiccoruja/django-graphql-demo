VENV_PY_VERSION := /usr/local/bin/python3.8
PIP := /usr/local/bin/pip3.8

VENV_NAME := djangoenv


PY38:
	$(VENV_PY_VERSION) --version
	$(PIP) --version
	
	

$(VENV_NAME):  PY38
	@echo $(shell pwd)
	$(VENV_PY_VERSION) -m pip install --upgrade pip
	$(PIP) install virtualenv
	
	if [ -d "$(VENV_NAME)" ]; \
        then \
        echo "$(VENV_NAME) is present";\
        ls -lrt $(VENV_NAME); \
        else \
        virtualenv --clear --always-copy -p $(VENV_PY_VERSION) $(VENV_NAME); \
    fi