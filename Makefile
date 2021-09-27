all:
	pytest
	mutmut run --paths-to-mutate caesar_cipher.py

.PHONY: all
