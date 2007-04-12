%define	major 0
%define libname	%mklibname unicall %{major}

Summary:	A interface independance library for telephony call control
Name:		libunicall
Version:	0.0.3
Release:	%mkrel 3
License:	GPL
Group:		System/Libraries
URL:		http://www.soft-switch.org/libunicall
Source0:	http://www.soft-switch.org/libunicall/libunicall-%{version}.tar.bz2
Patch0:		libunicall-zaptel_header.diff
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRequires:	tiff-devel >= 3.6.1-3mdk
BuildRequires:	spandsp-devel
BuildRequires:	audiofile-devel
BuildRequires:	libxml2-devel
BuildRequires:	jpeg-devel
BuildRequires:	file
BuildRequires:  zaptel-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
libunicall is an interface independance library for telephony call control.

%package -n	%{libname}
Summary:	Steve's SpanDSP library for telephony spans
Group:          System/Libraries

%description -n	%{libname}
libunicall is an interface independance library for telephony call control.

%package -n	%{libname}-devel
Summary:	Header files and libraries needed for development with libunicall
Group:		Development/C
Provides:	%{name}-devel lib%{name}-devel
Obsoletes:	%{name}-devel lib%{name}-devel
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This package includes the header files and libraries needed for
developing programs using libunicall.

%prep

%setup -q
%patch0 -p1

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force && aclocal-1.7 && autoconf && automake-1.7 --add-missing --copy

%configure2_5x

make CFLAGS="%{optflags} -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%dir %{_includedir}/unicall
%{_includedir}/unicall/*.h
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la


