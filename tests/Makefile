# -*- makefile -*-

FILES=$(shell ls test_*.py )
VERBOSE="False"

all:
	@echo "Performing Tests:"
	@echo "#test,pass,fail" > results.csv
	@for this_file in $(FILES) ; do \
             echo "`echo $$this_file`,`python $$this_file`" >> results.csv ;\
	     if [ $(VERBOSE) = "True" ]; then \
	        echo "`echo $$this_file | sed s/'.py'/''/` => (`python $$this_file`)";\
             fi ;\
	 done
	@python -c "import pandas as pd ; import numpy as np ; df = pd.read_csv(\"results.csv\") ; print(f\"pass:{np.sum(df['pass'])}, fail:{np.sum(df['fail'])}\")"

clean:
	@rm -f *~
	@rm -f results.csv
	@rm -rf __pycache__
