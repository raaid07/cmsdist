### RPM external xrootd 5.3.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}

%define tag v%{realversion}
%define branch stable-5.3.x
%define github_user xrootd
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake
Requires: zlib
Requires: python3
Requires: libxml2

%prep
%setup -n %n-%{realversion}

%build
# By default xrootd has perl, fuse, krb5, readline, and crypto enabled. 
# libfuse and libperl are not produced by CMSDIST.

rm -rf build; mkdir build; cd build
cmake .. \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_BUILD_TYPE=Release \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE \
  -DENABLE_PYTHON=TRUE \
  -DXRD_PYTHON_REQ_VERSION=3 \
  -DCMAKE_PREFIX_PATH="${PYTHON3_ROOT};${LIBXML2_ROOT}"

make %makeprocesses VERBOSE=1
make install
%{relocatePy3SitePackages}

%install
%define strip_files %i/lib
