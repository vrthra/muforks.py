.PRECIOUS: mutated.%

mutated.% : %
	python3 forktrans.py $* > mutated.$*.x
	mv mutated.$*.x mutated.$*


mutate.%: mutated.% | .pids
	rm -f .pids/*
	python3 mutated.$*

.pids:; mkdir -p .pids

clean:
	rm -rf .pids/*
	rm -rf __pycache__/

show:
	for i in .pids/*; do echo $$i; cat $$i; echo; done
