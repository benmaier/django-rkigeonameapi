default: 
	make python

clean:
	-rm -f *.o
	make pyclean

clean_all:
	make clean
	make pyclean

pyclean:
	-rm -f *.so
	-rm -rf *.egg-info*
	-rm -rf ./tmp/
	-rm -rf ./build/

python:
	pip install -e ../django-rkigeonameapi --no-binary :all:

checkdocs:
	python setup.py checkdocs

pypi:
	mkdir -p dist
	touch dist/dummy
	rm dist/*
	python setup.py sdist
	twine upload dist/*

readme:
	pandoc --from markdown_github --to rst README.md > _README.rst
	sed -e "s/^\:\:/\.\. code\:\: bash/g" _README.rst > README.rst
	rm _README.rst
