### RPM external p5-extutils-cbuilder 0.280202
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn ExtUtils-CBuilder
Source: http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/%{downloadn}-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make
