#
# Conditional build:
%bcond_with	tests		# build without tests

%define		orgname		extra-cmake-modules
%define		kdeframever	5.39
Summary:	Extra Cmake Modules for KF5
Name:		kf5-%{orgname}
Version:	5.39.0
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{orgname}-%{version}.tar.xz
# Source0-md5:	777b57222f5c23d1599b8e8774e96b73
URL:		http://www.kde.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	qt5-assistant
BuildRequires:	qt5-linguist
BuildRequires:	rpmbuild(macros) >= 1.698
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

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

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	../
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
        DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/ECM ECM-doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING-CMAKE-SCRIPTS README.rst ECM-doc/*
%{_datadir}/ECM
%{_mandir}/man7/ecm*.7*
