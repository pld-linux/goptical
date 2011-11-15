# TODO: dime (DXF renderer), plplot (renderer)
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	GNU Optical design and simulation library
Summary(pl.UTF-8):	Biblioteka do projektowania i symulacji optycznych GNU Optical
Name:		goptical
Version:	0.90
Release:	0.1
License:	GPL v3+
Group:		Libraries
Source0:	http://alpha.gnu.org/gnu/goptical/%{name}-%{version}.tar.gz
# Source0-md5:	ad3c85d16815ee8673908780ec287763
Patch0:		%{name}-sh.patch
Patch1:		%{name}-info.patch
URL:		http://gnu.org/software/goptical/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-glut-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gd-devel
BuildRequires:	gsl-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
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
