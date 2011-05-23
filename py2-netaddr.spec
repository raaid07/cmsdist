### RPM external py2-netaddr 0.7.4
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
Source: http://github.com/drkjam/netaddr/tarball/rel-%realversion?/%n-%realversion.tar.gz
Requires: python

%prep
%setup -n drkjam-netaddr-*

%build
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
for f in %i/bin/netaddr; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done
