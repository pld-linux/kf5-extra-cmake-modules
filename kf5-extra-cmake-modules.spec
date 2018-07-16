#
# Conditional build:
%bcond_without	tests		# build without tests

%define		orgname		extra-cmake-modules
%define		kdeframever	5.48
Summary:	Extra Cmake Modules for KF5
Summary(pl.UTF-8):	Dodatkowe moduły Cmake'a dla KF5
Name:		kf5-%{orgname}
Version:	5.48.0
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{orgname}-%{version}.tar.xz
# Source0-md5:	58c0a638cf85734c03fb5228b240182e
Patch0:		%{orgname}-tests.patch
URL:		http://www.kde.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	qt5-assistant >= 5.5.1
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.698
BuildRequires:	sed >= 4.0
BuildRequires:	sphinx-pdg >= 1.2
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with tests}
BuildRequires:	Qt5Core-devel >= 5.5.1
BuildRequires:	Qt5Gui-devel >= 5.5.1
BuildRequires:	Qt5Network-devel >= 5.5.1
BuildRequires:	Qt5Qml-devel >= 5.5.1
BuildRequires:	Qt5Quick-devel >= 5.5.1
BuildRequires:	libstdc++-devel >= 6:4.9
BuildRequires:	qt5-build >= 5.5.1
%endif
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

%prep
%setup -q -n %{orgname}-%{version}
%patch0 -p1

# causes make install failure after running tests
%{__sed} -i -e '/ECMToolchainAndroidTest/d' tests/CMakeLists.txt

%build
install -d build
cd build
%cmake .. \
	%{!?with_tests:-DBUILD_TESTING=OFF}

%{__make}

%if %{with tests}
# GenerateSipBindings wants clang and has libclang checks incompatible with libclang >= 4
ctest -E GenerateSipBindings
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build -j1 install \
        DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_docdir}/ECM ECM-doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING-CMAKE-SCRIPTS README.rst ECM-doc/*
%{_datadir}/ECM
%{_mandir}/man7/ecm*.7*
