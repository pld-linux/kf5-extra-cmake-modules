# TODO where to put files and docs of KF5
%define         _state          stable
%define		orgname		extra-cmake-modules

Summary:	Extra Cmake Modules for KF5
Name:		kf5-extra-cmake-modules
Version:	1.0.0
Release:	0.2
License:	See COPYING-CMAKE-SCRIPTS
Group:		X11/Libraries
Source0:	ftp://ftp.kde.org/pub/kde/%{_state}/frameworks/5.0.0/%{orgname}-%{version}.tar.xz
# Source0-md5:	a7b9e8756fdc2b3a8518ad9f9d21dfd5
URL:		http://www.kde.org/
BuildRequires:	cmake >= 2.8.12
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	sphinx-pdg
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

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
%if "%{_rpmversion}" >= "5"
BuildArch:     noarch
%endif

%description doc
Documentation for ECM.

%prep
%setup -q -n %{orgname}-%{version}

%build
install -d build
cd build
%cmake \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DKCFG_INSTALL_DIR=%{_datadir}/config.kcfg \
	-DPLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQT_PLUGIN_INSTALL_DIR=%{qt5dir}/plugins \
	-DQML_INSTALL_DIR=%{qt5dir}/qml \
	-DIMPORTS_INSTALL_DIR=%{qt5dirs}/imports \
	-DSYSCONF_INSTALL_DIR=%{_sysconfdir} \
	-DLIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_LIBEXEC_INSTALL_DIR=%{_libexecdir} \
	-DKF5_INCLUDE_INSTALL_DIR=%{_includedir} \
	-DECM_MKSPECS_INSTALL_DIR=%{qt5dir}/mkspecs/modules \
	-D_IMPORT_PREFIX=%{_prefix} \
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
