# TODO: dime (DXF renderer), plplot (renderer)
#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	GNU Optical design and simulation library
Summary(pl.UTF-8):	Biblioteka do projektowania i symulacji optycznych GNU Optical
Name:		goptical
Version:	1.0
Release:	1
License:	GPL v3+
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/goptical/%{name}-%{version}.tar.gz
# Source0-md5:	a65d1dc6af36d481ef8ea34a0ccd9823
Patch0:		%{name}-includes.patch
Patch1:		%{name}-info.patch
URL:		http://gnu.org/software/goptical/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gd-devel
BuildRequires:	gsl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	rpmbuild(macros) >= 1.749
BuildRequires:	xorg-lib-libX11-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Goptical is a C++ optical design and simulation library. Goptical is
free software and is part of the GNU project.

It provides model classes for optical components, surfaces and
materials. It enables building optical systems by creating and
placing various optical components in a 3D space and simulates light
propagation through the system. Classical optical design analysis
tools can be used on optical systems.

%description -l pl.UTF-8
Goptical to biblioteka C++ do projektowania i symulacji optycznych.
Jest to oprogramowanie wolnodostępne, będące częścią projektu GNU.

Udostępnia klasy modeli dla elementów optycznych, powierzchni oraz
materiałów. Pozwala na konstruowanie systemów optycznych poprzez
tworzenie i umieszczanie różnych elementów optycznych w przestrzeni
trójwymiarowej, a następnie symulowanie rozprowadzania światła przez
te systemy. W tych systemach optycznych można używać klasycznych
narzędzi do analizy optycznej.

%package devel
Summary:	Header files for Goptical libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Goptical
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gd-devel
Requires:	gsl-devel
Requires:	libstdc++-devel
Requires:	xorg-lib-libX11-devel

%description devel
Header files for Goptical libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Goptical.

%package static
Summary:	Static Goptical libraries
Summary(pl.UTF-8):	Statyczne biblioteki Goptical
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Goptical libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Goptical.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd goptical_core
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../goptical_design
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd ..
%if "%{_ver_ge %{cxx_version} 7.0}" == "1"
# code is not ready for C++17
CXXFLAGS="%{rpmcxxflags} -std=gnu++14"
%endif
%configure \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/libgoptical-1.0.so
%attr(755,root,root) %{_libdir}/libgoptical_design-1.0.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgoptical.so
%attr(755,root,root) %{_libdir}/libgoptical_design.so
%{_libdir}/libgoptical.la
%{_libdir}/libgoptical_design.la
%{_includedir}/Goptical
%{_infodir}/goptical.info*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgoptical.a
%{_libdir}/libgoptical_design.a
%endif
