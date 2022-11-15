#
# Conditional build:
%bcond_without	doc		# build without doc
%bcond_without	tests		# build without tests

%define		orgname		extra-cmake-modules
%define		kdeframever	5.100
Summary:	Extra Cmake Modules for KF5
Summary(pl.UTF-8):	Dodatkowe moduły Cmake'a dla KF5
Name:		kf5-%{orgname}
Version:	5.100.0
Release:	1
License:	BSD
Group:		Development/Building
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{orgname}-%{version}.tar.xz
# Source0-md5:	5e14f205ed0c5bb25d9357574975e47a
Patch0:		%{orgname}-tests.patch
Patch1:		kdefetchtranslations-test.patch
Patch2:		no-fatal-warnings.patch
URL:		https://kde.org/
BuildRequires:	cmake >= 3.16
BuildRequires:	qt5-assistant >= 5.9.0
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.698
BuildRequires:	sed >= 4.0
%{?with_doc:BuildRequires:	sphinx-pdg >= 1.2}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with tests}
BuildRequires:	Qt5Core-devel >= 5.9.0
BuildRequires:	Qt5Quick-devel >= 5.9.0
BuildRequires:	libstdc++-devel >= 6:5
%endif
BuildConflicts:	qmake
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Extra CMake Modules package, or ECM, adds to the modules provided
by CMake, including both ones used by find_package() to find common
software and ones that can be used directly in CMakeLists.txt files to
perform common tasks.

In addition, it provides common build settings used in software
produced by the KDE community.

While the driving force of this module is to reduce duplication in
CMake scripts across KDE software, it is intended to be useful for any
software that uses the CMake build system.

%description -l pl.UTF-8
Pakiet Extra CMake Modules (ECM) dostarcza dodatkowe moduły do tych
dostarczanych przez CMake'a, zawierające te używane przez
find_package() do szukania popularnego oprogramowania, a także takie,
których można używać bezpośrednio w CMakeLists.txt do wykonywania
wspólnych zadań.

Ponadto pakiet dostarcza wspólne ustawienia budowana używane w
oprogramowaniu tworzonym przez społeczność KDE.

O ile główną motywacją tego modułu jest zmniejszenie duplikacji w
skryptach CMake'a w oprogramowaniu KDE, ma także być przydatny dla
dowolnych programów wykorzystujących system budowania CMake.

%package apidocs
Summary:	API documentation for %{orgname}
Summary(pl.UTF-8):	Dokumentacja API %{orgname}
Group:		Documentation
Obsoletes:	kf5-extra-cmake-modules-doc < 1.4.0

%description apidocs
API documentation for %{orgname}.

%description apidocs -l pl.UTF-8
Dokumentacja API dla %{orgname}.

%prep
%setup -q -n %{orgname}-%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p1

# causes make install failure after running tests
%{__sed} -i -e '/ECMToolchainAndroidTest/d' tests/CMakeLists.txt

%build
install -d build
cd build
%cmake \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	%{!?with_doc:-DBUILD_HTML_DOCS=OFF} \
	..

%{__make}

%if %{with tests}
# GenerateSipBindings wants clang and has libclang checks incompatible with libclang >= 4
# ECMPoQmToolsTest fails to build it's own moc file
ctest -E '(GenerateSipBindings|ECMPoQmToolsTest)' --output-on-failure
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build -j1 install \
        DESTDIR=$RPM_BUILD_ROOT

sed -i -e 's#/usr/bin/env bash#/bin/bash#' $RPM_BUILD_ROOT%{_datadir}/ECM/kde-modules/kde-git-commit-hooks/pre-commit.in
sed -i -e 's#/usr/bin/env bash#/bin/bash#' $RPM_BUILD_ROOT%{_datadir}/ECM/kde-modules/kde-git-commit-hooks/clang-format.sh

%if %{with doc}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/ECM ECM-doc
%endif
install -d $RPM_BUILD_ROOT%{_datadir}/qlogging-categories5

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING-CMAKE-SCRIPTS README.rst
%{_datadir}/ECM
%{_datadir}/qlogging-categories5
%{_mandir}/man7/ecm*.7*

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc ECM-doc/html/*
%endif
