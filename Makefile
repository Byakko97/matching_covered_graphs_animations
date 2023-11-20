run:
	python3 src/api/run.py $(algo) $(test)

test:
	python3 src/api/test.py $(algo)

animate:
	python3 src/api/animate.py $(algo) $(test) $(if $(f), -f $(f), ) $(if $(filter true,$(m)), -m, )