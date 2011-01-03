%define	major 0
%define libname %mklibname unicall %{major}
%define develname %mklibname unicall -d

Summary:	A interface independance library for telephony call control
Name:		libunicall
Version:	0.0.6
Release:	%mkrel 0.pre1.3
License:	LGPL
Group:		System/Libraries
URL:		http://www.soft-switch.org/unicall/installing-mfcr2.html
Source0:	http://www.soft-switch.org/downloads/unicall/libunicall-%{version}pre1.tgz
Patch0:		libunicall-linkage_fix.diff
BuildRequires:	autoconf2.5
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	tiff-devel >= 3.6.1-3mdk
BuildRequires:	spandsp-devel
BuildRequires:	audiofile-devel
BuildRequires:	libxml2-devel
BuildRequires:	jpeg-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libunicall is an interface independance library for telephony call control.

%package -n	%{libname}
Summary:	Steve's SpanDSP library for telephony spans
Group:          System/Libraries

%description -n	%{libname}
libunicall is an interface independance library for telephony call control.

%package -n	%{develname}
Summary:	Header files and libraries needed for development with libunicall
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname unicall 0 -d}

%description -n	%{develname}
This package includes the header files and libraries needed for developing
programs using libunicall.

%prep

%setup -q
%patch0 -p0

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf; automake --add-missing --copy

%configure2_5x

make CFLAGS="%{optflags} -fPIC"

%install
rm -rf %{buildroot}

%makeinstall_std

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-, root, root)
%dir %{_includedir}/unicall
%{_includedir}/unicall/*.h
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
