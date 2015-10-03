SHELL=/bin/bash

all:
	@for a in $$(ls); do \
		if [ -e $$a/conf.py ]; then \
			pushd $$a > /dev/null; \
			echo $$a; \
			sphinx-build -E -b html . html; \
			popd > /dev/null; \
		fi; \
	done;

clean:
	@rm *.pyc -f
	@for a in $$(ls); do \
		if [ -e $$a/conf.py ]; then \
			pushd $$a > /dev/null; \
			rm html *~ -rf; \
			popd > /dev/null; \
		fi; \
	done;
