test:
	@env PYTHONPATH=.:$$PYTHONPATH python sample_proj/manage.py test weeky agenda

run:
	@env PYTHONPATH=.:$$PYTHONPATH python sample_proj/manage.py runserver

shell:
	@env PYTHONPATH=.:$$PYTHONPATH python sample_proj/manage.py shell
