# -*- make -*-
# Last edited: <2022-03-14 10:47:58 wcobb>

PACKAGE="threat"
PYVER="3.8"
PIP=$(shell which pip )
PWD=$(shell pwd)
PYTHON=$(shell which python )
EDITOR=$(shell which emacs )
VERSION=$(shell echo "`date -u +'%Y%m%d%H%M%S'`" )
COMPANY="Blueprint Technologies, LLC."
PKGDESC="Portable Hardware-accelerated AutoTagger"
DISTDIR="dist"
DOCSDIR=$(shell if [ -e $(HOME)/Documents ]; then echo "${HOME}/Documents" ; else echo "${HOME}/docs" ; fi )

help:
	@echo "Python Makefile..."
	@echo ""
	@echo "Command Options"
	@echo ""
	@echo "	make all       -- creates the package and documentation"
	@echo "	make install   -- install the package and documentation"
	@echo "	make clean     -- clean up the directory hierarchy"
	@echo "	make sphinx    -- creates the documentation"
	@echo "	make wheel     -- creates the package"
	@echo "	make uninstall -- uninstall the package (if installed)"
	@echo "	make distclean -- clean and uninstall"
	@echo "	make edit      -- edit the makefile using $(EDITOR)"
	@echo "	make help      -- prints out this message"
	@echo ""
	@echo "Boiler-plate environment variables:"
	@echo ""
	@echo "	PYTHON   = $(PYTHON)"
	@echo "	PIP      = $(PIP)"
	@echo "	EDITOR   = $(EDITOR)"
	@echo "	VERSION  = $(VERSION)"
	@echo "	PYVER    = $(PYVER)"
	@echo "	PACKAGE  = $(PACKAGE)"
	@echo "	COMPANY  = $(COMPANY)"
	@echo "	PKGDESC  = $(PKGDESC)"
	@echo "	DISTDIR  = $(DISTDIR)"
	@echo "	DOCSDIR  = $(DOCSDIR)"
	@echo ""

all : wheel # sphinx

wheel:
	@if [ ! -e $(PWD)/$(DISTDIR) ]; then \
	     mkdir -p $(PWD)/$(DISTDIR) ;\
	 fi
	@echo "================================="
	@echo "CURRENT_VERSION = $(VERSION)"
	@echo "================================="
	@echo "from setuptools import setup"                   >  setup.py
	@echo "setup(name='$(PACKAGE)',"                       >> setup.py
	@echo "      packages=['$(PACKAGE)',"                  >> setup.py
	@echo "                '$(PACKAGE).common',"           >> setup.py
	@echo "                '$(PACKAGE).platform',"         >> setup.py
	@echo "                '$(PACKAGE).core',"             >> setup.py
	@echo "               ],"                              >> setup.py
	@echo "      description='$(COMPANY) $(PKGDESC)',"     >> setup.py
	@echo "      version='${VERSION}',"                    >> setup.py
	@echo "      url='file:$(PWD)/$(DISTDIR)/$(PACKAGE)'," >> setup.py
	@echo "      author=['Wesley Cobb', ],"                >> setup.py
	@echo "      author_email=['wesley@bpcs.com', ],"      >> setup.py
	@echo "      keywords=['pip',"                         >> setup.py
	@echo "                'blueprint',"                   >> setup.py
	@echo "                'fits',"                        >> setup.py
	@echo "                '$(PACKAGE)',"                  >> setup.py
	@echo "                'data_science',])"              >> setup.py
	@$(PYTHON) setup.py sdist
	@$(PYTHON) setup.py config
	@$(PYTHON) setup.py build
	@$(PYTHON) setup.py bdist_wheel
	@rm -rf $(PWD)/build

sphinx:
	@if [ ! -e $(PWD)/$(DISTDIR) ]; then \
	     mkdir -p $(PWD)/$(DISTDIR) ;\
	 fi
	@echo "#!/usr/bin/env python"                                                 >  docs/source/conf.py
	@echo "#"                                                                     >> docs/source/conf.py
	@echo "# Copyright (C) 2022, by $(COMPANY)"                                   >> docs/source/conf.py
	@echo "# All Rights Reserved."                                                >> docs/source/conf.py
	@echo "#"                                                                     >> docs/source/conf.py
	@echo "# Revised $(VERSION)"                                                  >> docs/source/conf.py
	@echo ""                                                                      >> docs/source/conf.py
	@echo "import os"                                                             >> docs/source/conf.py
	@echo "import sys"                                                            >> docs/source/conf.py
	@echo "sys.path.insert(0, os.path.abspath('../..'))"                          >> docs/source/conf.py
	@echo "project = '${PACKAGE}'"                                                >> docs/source/conf.py
	@echo "copyright = '2022, Blueprint Technologies LLC'"                        >> docs/source/conf.py
	@echo "authors = ['Wesley Cobb (wesley@bpcs.com)', 'Demian Esnaurrizar (desnaurrizar@bpcs.com)']," >> docs/source/conf.py
	@echo "# The short X.Y version"                                               >> docs/source/conf.py
	@echo "version = '$(VERSION)'"                                                >> docs/source/conf.py
	@echo "release = '$(VERSION)'"                                                >> docs/source/conf.py
	@echo "extensions = ["                                                        >> docs/source/conf.py
	@echo "    'sphinx.ext.autodoc',"                                             >> docs/source/conf.py
	@echo "    'sphinx.ext.doctest',"                                             >> docs/source/conf.py
	@echo "    'sphinx.ext.intersphinx',"                                         >> docs/source/conf.py
	@echo "    'sphinx.ext.todo',"                                                >> docs/source/conf.py
	@echo "    'sphinx.ext.coverage',"                                            >> docs/source/conf.py
	@echo "    'sphinx_rtd_theme',"                                               >> docs/source/conf.py
	@echo "    'sphinx.ext.imgmath',"                                             >> docs/source/conf.py
	@echo "    'sphinx.ext.ifconfig',"                                            >> docs/source/conf.py
	@echo "    'sphinx.ext.napoleon',"                                            >> docs/source/conf.py
	@echo "    'sphinx.ext.viewcode',"                                            >> docs/source/conf.py
	@echo "]"                                                                     >> docs/source/conf.py
	@echo "templates_path = ['.templates']"                                       >> docs/source/conf.py
	@echo "source_suffix = '.rst'"                                                >> docs/source/conf.py
	@echo "master_doc = 'index'"                                                  >> docs/source/conf.py
	@echo "language = None"                                                       >> docs/source/conf.py
	@echo "intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}" >> docs/source/conf.py
	@echo "exclude_patterns = []"                                                 >> docs/source/conf.py
	@echo "html_theme = 'sphinx_rtd_theme'"                                       >> docs/source/conf.py
	@echo "todo_include_todos = True"                                             >> docs/source/conf.py
	@echo ""                                                                      >> docs/source/conf.py
#
# ==================== run sphinx to generate the html docs =========================
#
	@sphinx-apidoc -f -o docs/source $(PACKAGE)
	@cd $(PWD)/docs ; sphinx-build -b html source/ build/ ; cd $(PWD)
	@if [ ! -e $(PWD)/$(DISTDIR)/$(PACKAGE) ]; then \
	     mkdir $(PWD)/$(DISTDIR)/$(PACKAGE) ;\
	 fi
	@cp -rpv $(PWD)/docs/build/* $(PWD)/$(DISTDIR)/$(PACKAGE)
	@rm -rf  $(PWD)/docs/build
#
# ==================== run sphinx to generate the latex docs ========================
#
#	@cd $(PWD)/docs ; sphinx-build -b latex source/ build/ ; cd $(PWD)
#	@cd $(PWD)/docs/build ; make ; cd $(PWD)
#	@cp $(PWD)/docs/build/$(PACKAGE).pdf $(PWD)/$(DISTDIR)
#	@rm -rf $(PWD)/docs/build

install: install-package # install-docs
	@rm -rf build
	@rm -rf $(PACKAGE).egg-info
	@rm -rf docs/build

install-package:
	@echo "installing pip package..."
	@if [ -e $(PWD)/$(DISTDIR)/$(WHEELDIR)/$(PACKAGE)*.whl ]; then \
	     $(PIP) install --upgrade $(PWD)/$(DISTDIR)/$(WHEELDIR)/$(PACKAGE)*.whl ;\
	 fi
	@pip list | egrep $(PACKAGE)

install-docs:
	@echo "installing html documentation to $(DOCSDIR)/$(PACKAGE) ..."
	@if [ ! -e $(DOCSDIR)/$(PACKAGE) ]; then \
	     mkdir -p $(DOCSDIR)/$(PACKAGE) ;\
	 fi
	@cp -rpv $(PWD)/$(DISTDIR)/$(PACKAGE) $(DOCSDIR)/$(PACKAGE)
#	@echo "installing latex pdf documentation to $(DOCSDIR) ..."
#	@cp -v $(PWD)/$(DISTDIR)/$(PACKAGE).pdf $(DOCSDIR)

clean:
	@rm -f setup.py
	@rm -f `find . -name "*~" -print`
	@rm -f `find . -name "gmon.out" -print`
	@rm -f `find . -name "*.fits" -print`
	@rm -f docs/source/conf.py
	@rm -f $(PWD)/$(DISTDIR)/$(PACKAGE)*.whl
	@rm -f $(PWD)/$(DISTDIR)/$(PACKAGE)*.tgz
	@rm -rf `find . -name "__pycache__" -print`

uninstall:
	@echo "removing pip package..."
	@if [ "x`pip list | egrep -i $(PACKAGE)`" != "x" ]; then \
	     $(PIP) uninstall -y $(PACKAGE)* ;\
	 fi
	@echo "removing $(DOCSDIR)/$(PACKAGE).pdf... (latex docs)"
	@rm -f $(DOCSDIR)/$(PACKAGE).pdf
	@echo "removing $(DOCSDIR)/$(PACKAGE) ... (html docs)"
	@rm -rf $(DOCSDIR)/$(PACKAGE)

distclean: clean uninstall
	@rm -rf dist 

test:
	@cd tests ; make -f Makefile ; cd -

tags:
	@find . -name "*.py" -print -type f | xargs etags -a

edit:
	@$(EDITOR) Makefile

update:
	@make -f Makefile distclean all install
	@make -f Makefile clean
