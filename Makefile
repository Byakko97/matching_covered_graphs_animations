run:
	python3 src/executables/run.py $(algo) $(test)

test:
	python3 src/executables/test.py $(algo)

animate:
	python3 src/executables/animate.py $(algo) $(test) $(if $(f), -f $(f), ) $(if $(m), -m)