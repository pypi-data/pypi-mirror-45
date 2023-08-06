comptest_package=zuper_json,zuper_ipce
coverage_include='*src/zuper_json*'
coveralls_repo_token=5eha7C63Y0403x9LRaGscdqQet7yC3WoR


all: test-zuper-utils

test-zuper-utils:
	rm -f .coverage
	rm -rf cover
	nosetests --cover-html --cover-tests --with-coverage --cover-package=zuper_json zuper_json   -v


test-zuper-all:
	rm -f .coverage
	rm -rf cover
	nosetests --cover-html --cover-tests --with-coverage --cover-package=zuper_json,zuper_ipce zuper_json zuper_ipce  -v





docker-36-build:
	docker build -f Dockerfile.python3.6 -t python36 .

docker-36-test:  docker-37-build
	docker run -it -v $(PWD)/src/zuper_json:/project/src/zuper_json -w /project python36 make all

docker-36-shell:
	docker run -it   python36 /bin/bash


docker-37-build:
	docker build -f Dockerfile.python3.7 -t python37 .

docker-37-test: docker-37-build
	docker run -it -v $(PWD)/src/zuper_json:/project/src/zuper_json -w /project python37 make all

docker-37-shell:
	docker run -it   python37 /bin/bash


bump-upload:
	$(MAKE) bump
	$(MAKE) upload

bump:
	bumpversion patch

upload:
	git push --tags
	git push
	rm -f dist/*
	python setup.py sdist
	twine upload dist/*


out=out-comptests
coverage_dir=out-coverage
coverage_run=coverage run

tests-clean:
	rm -rf $(out) $(coverage_dir) .coverage .coverage.*


# junit:
# 	mkdir -p $(out)/junit
# 	comptests-to-junit $(out)/compmake > $(out)/junit/junit.xml

# tests:
# 	comptests --nonose $(comptest_package)

# tests-contracts:
# 	comptests --contracts --nonose  $(comptest_package)

# tests-contracts-coverage:
# 	$(MAKE) tests-coverage-single-contracts
# 	$(MAKE) coverage-report
# 	$(MAKE) coverage-coveralls

# tests-coverage:
# 	$(MAKE) tests-coverage-single-nocontracts
# 	$(MAKE) coverage-report
# 	$(MAKE) coverage-coveralls


# tests-coverage-single-nocontracts:
# 	-DISABLE_CONTRACTS=1 comptests -o $(out) --nonose -c "exit"  $(comptest_package)
# 	-DISABLE_CONTRACTS=1 $(coverage_run)  `which compmake` $(out)  -c "rmake"

# tests-coverage-single-contracts:
# 	-DISABLE_CONTRACTS=1 comptests -o $(out) --nonose -c "exit"  $(comptest_package)
# 	-DISABLE_CONTRACTS=0 $(coverage_run)  `which compmake` $(out) --contracts -c "rmake"

# tests-coverage-parallel-contracts:
# 	-DISABLE_CONTRACTS=1 comptests -o $(out) --nonose -c "exit" $(comptest_package)
# 	-DISABLE_CONTRACTS=0 $(coverage_run)  `which compmake` $(out) --contracts -c "rparmake"

# coverage-report:
# 	coverage combine
# 	coverage html -d $(coverage_dir)

coverage-coveralls:
	# without --nogit, coveralls does not find the source code
	COVERALLS_REPO_TOKEN=$(coveralls_repo_token) coveralls



