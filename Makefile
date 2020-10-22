VENV_PY_VERSION := /usr/local/bin/python3.8
VENV_NAME := djangoenv


PY38:
	$(VENV_PY_VERSION) --version

	
$(VENV_NAME):  PY38
	@echo $(shell pwd)
	$(VENV_PY_VERSION) -m pip install --upgrade pip
	$(VENV_PY_VERSION) -m pip install virtualenv
	
	if [ -d "$(VENV_NAME)" ]; \
        then \
        echo "$(VENV_NAME) is present";\
        ls -lrt $(VENV_NAME); \
        else \
        virtualenv --clear --always-copy -p $(VENV_PY_VERSION) $(VENV_NAME); \
    fi
	
	. $(VENV_NAME)/bin/activate

	pip --version
	pip install Django selenium graphene>=2.0
	

runserver: $(VENV_NAME)
	. $(VENV_NAME)/bin/activate
	cd demo && python manage.py runserver 0.0.0.0:8000 &