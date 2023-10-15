run:
	python3 src/exec/run.py $(algo) $(test)

test:
	python3 src/exec/test.py $(algo)

animate:
	python3 src/exec/animate.py $(algo) $(test) $(if $(f), -f $(f), ) $(if $(m), -m)