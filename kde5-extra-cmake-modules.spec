# TODO where to put files and docs of KF5
%define         _state          stable
%define		orgname		extra-cmake-modules
%define         qt5ver           5.2.0

Summary:	Extra Cmake Modules for KF5
Name:		kde5-extra-cmake-modules
Version:	1.0.0
Release:	0.1
License:	See COPYING-CMAKE-SCRIPTS
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/5.0.0/%{orgname}-%{version}.tar.xz
# Source0-md5:	a7b9e8756fdc2b3a8518ad9f9d21dfd5
URL:		http://www.kde.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	sphinx-pdg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Extra CMake Modules package, or ECM, adds to the modules provided
by CMake, including both ones used by ``find_package()`` to find
common software and ones that can be used directly in
``CMakeLists.txt`` files to perform common tasks.

In addition, it provides common build settings used in software
produced by the KDE community.

While the driving force of this module is to reduce duplication in
CMake scripts across KDE software, it is intended to be useful for any
software that uses the CMake build system.

%package doc
Summary:	Documentation for ECM
Group:		Documentation
BuildArch:	noarch

%description doc
Documentation for ECM.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build/ install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING-CMAKE-SCRIPTS README.rst
%{_datadir}/ECM
%{_mandir}/man7/ecm*

%files doc
%defattr(644,root,root,755)
%{_docdir}/ECM
