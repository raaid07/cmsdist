### RPM external py2-pyxml 0.8.4
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/pyxml/PyXML-%{realversion}.tar.gz
Requires: python expat

%prep
%setup -n PyXML-%{realversion}

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/xmlproc_*; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
