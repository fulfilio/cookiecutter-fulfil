migrate:
	rm -rf migrations/versions/*
	FLASK_APP=manage.py flask maint clear_migration_history
	FLASK_APP=manage.py flask db migrate --splice
	find migrations/versions -name "*.pyc" -exec rm {} \;
	find migrations/versions -name "*.py" -type f -exec sed -i "s/ChoiceType(length=255)/ChoiceType([('', '')])/g" {} \;
	FLASK_APP=manage.py flask db upgrade
