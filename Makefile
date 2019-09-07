PROJECT_ROOT=$(strip $(patsubst %/, %, $(dir $(abspath $(lastword $(MAKEFILE_LIST))))))

reset_migration:
	@find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

migrate_auto_make:
	@python $(PROJECT_ROOT)/manage.py makemigrations
	@python $(PROJECT_ROOT)/manage.py migrate

django_ipython_shell:
	@python manage.py shell_plus --ipython

.PHONY: reset_migration migrate_auto_make django_ipython_shell
