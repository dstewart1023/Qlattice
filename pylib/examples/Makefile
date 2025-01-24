SHELL=/bin/bash

all: run

tests = make-sample-gauge-field.log \
		qar.log \
		lat-io.log \
		field-utils.log \
		qcd-utils.log \
		hmc-pure-gauge.log \
		field-selection.log \
		selected-field.log \
		fields-io.log \
		free-invert.log

tests_gpt = gpt-qlat-convert.log \
			gpt-qlat-smear.log \
			gpt-qlat-sample-gauge-field.log \
			gpt-qlat-lanc.log \
			gpt-qlat-free-invert.log \
			gpt-qlat-mdwf.log \
			gpt-qlat-madwf.log \
			gpt-qlat-gfix-mdwf.log \
			gpt-qlat-rbc-ukqcd-invert.log

run: cqlat-example $(tests) $(tests_gpt)

%.log: %.py
	mpirun --np 2 ./"$<" --mpi 1.1.1.2 --mpi_split 1.1.1.1 --mpi 1.1.2 --mpi_split 1.1.1 | tee "$@".full
	-rm -rfv results
	-grep -v "^Timer\|^GPT\|^Grid\|timing: \|Timing: \|local time slice\|^clean_cache:" "$@".full > "$@"

cqlat-example: cqlat.log

cqlat.log:
	-make -C cqlat -j 2
	python3 -c "import cqlat ; cqlat.hello_world()" > cqlat.log

clean:
	-rm -v *.log.full
	-make -C cqlat clean
	-rm -v cqlat.so

clean-logs: clean
	-touch $(tests_gpt)
	-rm -v cqlat.log $(tests)

clean-logs-gpt: clean-logs
	-rm -v $(tests_gpt) $(tests)
