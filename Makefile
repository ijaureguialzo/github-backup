#!make

help: _header
	${info}
	@echo Opciones:
	@echo -------------
	@echo backup
	@echo -------------

_header:
	@echo -------------
	@echo GitHub Backup
	@echo -------------

crear_usuarios:
	@poetry run python backup.py
