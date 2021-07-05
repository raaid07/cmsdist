### RPM external madgraph5amcatnlo 2.7.3
%define versiontag 2_7_3
Provides: perl(Compress::Zlib)
Provides: perl(List::Util)
Source: https://launchpad.net/mg5amcnlo/2.0/2.7.x/+download/MG5_aMC_v%{realversion}.py3.tar.gz
Patch0: madgraph5amcatnlo-config
# Compile and install internal and external packages
#Patch1: madgraph5amcatnlo-compile

Requires: python3 py3-six
Requires: hepmc
# Needed for ExRoot analysis package
Requires: root   
# Needed for Syscalc package
Requires: lhapdf
Requires: gosamcontrib
Requires: fastjet
Requires: pythia8
Requires: thepeg

%prep
%setup -n MG5_aMC_v%{versiontag}_py3
%patch0 -p1
#%patch1 -p1

sed -i -e "s|\${HEPMC_ROOT}|${HEPMC_ROOT}|g" input/mg5_configuration.txt
sed -i -e "s|\${PYTHIA8_ROOT}|${PYTHIA8_ROOT}|g" input/mg5_configuration.txt
sed -i -e "s|\${LHAPDF_ROOT}|${LHAPDF_ROOT}|g" input/mg5_configuration.txt
sed -i -e "s|\${FASTJET_ROOT}|${FASTJET_ROOT}|g" input/mg5_configuration.txt
sed -i -e "s|\${GOSAMCONTRIB_ROOT}|${GOSAMCONTRIB_ROOT}|g" input/mg5_configuration.txt
sed -i -e "s|\${THEPEG_ROOT}|${THEPEG_ROOT}|g" input/mg5_configuration.txt
sed -i -e "s|@MADGRAPH5AMCATNLO_ROOT@|%{i}|g" input/mg5_configuration.txt
sed -i -e "s|SHFLAG = \-fPIC|SHFLAG = \-fPIC \-fcommon|g" vendor/StdHEP/src/stdhep_arch

%build
export FC="$(which gfortran) -std=legacy"

# Start small NLO event generation to make sure that all additional packages are compiled
cat <<EOF > basiceventgeneration.txt
generate p p > t t~ [QCD]
output basiceventgeneration
launch
set nevents 5
EOF
./bin/mg5_aMC ./basiceventgeneration.txt

# Remove all downloaded tgz files before building the package
find . -type f -name '*.tgz' -delete

%install
rsync -avh %{_builddir}/MG5_aMC_v%{versiontag}_py3/ %{i}/
sed -ideleteme 's|#!.*/bin/python|#!/usr/bin/env python|' \
    %{i}/Template/LO/bin/internal/addmasses_optional.py \
    %{i}/madgraph/various/progressbar.py
find %{i} -name '*deleteme' -delete

%post
%{relocateConfig}input/mg5_configuration.txt
