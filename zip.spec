%define name zip
%define version 2.32
%define release %mkrel 1
%define filever %(echo %version|sed s/\\\\\.//)

Name: %{name}
Summary: A file compression and packaging utility compatible with PKZIP
Version: %{version}
Release: %{release}
Source0: ftp://ftp.uu.net/pub/archiving/zip/src/%{name}%{filever}.tar.bz2
Source1: ftp.uu.net:/pub/archiving/zip/src/zcrypt29-exportable.tar.bz2
Patch0: zip-2.3-unforce-cflags.patch
Patch1: zip-2.3-noninteractivepassword+testencrypedfile.patch
URL: http://www.info-zip.org/pub/infozip/
License: BSD-like
Group: Archiving/Compression
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The zip program is a compression and file packaging utility.  Zip is
analogous to a combination of the UNIX tar and compress commands and is
compatible with PKZIP (a compression and file packaging utility for
MS-DOS systems).

Install the zip package if you need to compress files using the zip
program.

This version support crypto encryption.

%prep
%setup -q -a 1
%patch0 -p1 -b .cflags
%patch1 -p1 -b .pass

%build
make -ef unix/Makefile prefix=%{prefix} CC="gcc $RPM_OPT_FLAGS" generic_gcc

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_bindir
mkdir -p $RPM_BUILD_ROOT/%_mandir/man1

%makeinstall -f unix/Makefile MANDIR=$RPM_BUILD_ROOT%_mandir/man1 INSTALL=install
#CC="gcc $RPM_OPT_FLAGS -I. -DUNIX -DUTIL"
cd %buildroot%_mandir/man1
ln -s zip.1 zipcloak.1
ln -s zip.1 zipnote.1
ln -s zip.1 zipsplit.1

%clean
rm -fr $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc BUGS CHANGES INSTALL MANUAL README TODO WHATSNEW WHERE LICENSE
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*


