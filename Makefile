#
# 'make build' should install needed Python modules and
# initialize CONFIG.py
#
# 'make test' should run the test server (with debugging)
# 'make run PORT=5656'  should run the flask application under gunicorn on port 5656
#
# 

###
# You may need to configure these variables:
###
PY = python3      # You might need a specific version like python3.4
PYVENV = pyvenv   # You might need a specific version like pyvenv-3.4
PORT = 5656       # Choose a port number that doesn't conflict, or specify as arg to make

install:	CONFIG.py
	rm -rf env  # In case it is already there
	$(PYVENV) env
	(. env/bin/activate ; pip3 install -r requirements.txt)

test:	env CONFIG.py
	(. env/bin/activate; $(PY) flask_main.py)

run:	env CONFIG.py
	(. env/bin/activate; gunicorn -b 0.0.0.0:$(PORT) flask_main:app) &

env:
	build

CONFIG.py:  CONFIG.base.py
	echo "Warning: Copying CONFIG.py from base version; it may need editing"
	cp CONFIG.base.py CONFIG.py

