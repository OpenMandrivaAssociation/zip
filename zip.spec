%define name zip
%define version 3.0
%define release %mkrel 3
%define filever %(echo %version|sed s/\\\\\.//)

Name: %{name}
Summary: A file compression and packaging utility compatible with PKZIP
Version: %{version}
Release: %{release}
License: BSD-like
Group: Archiving/Compression
URL: http://www.info-zip.org/pub/infozip/
Source0: http://dfn.dl.sourceforge.net/sourceforge/infozip/%{name}%{filever}.zip
Patch0: zip-2.3-unforce-cflags.patch
Patch1: zip-2.3-noninteractivepassword+testencrypedfile.patch
Patch2: zip-3.0-format_not_a_string_literal_and_no_format_arguments.diff
Patch3: zip-3.0-LDFLAGS.diff
BuildRequires: bzip2-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The zip program is a compression and file packaging utility. Zip is analogous
to a combination of the UNIX tar and compress commands and is compatible with
PKZIP (a compression and file packaging utility for MS-DOS systems).

Install the zip package if you need to compress files using the zip program.

This version support crypto encryption.

%prep

%setup -q -n %{name}%{filever}
%patch0 -p1 -b .cflags
%patch1 -p0 -b .pass
%patch2 -p0 -b .format_not_a_string_literal_and_no_format_arguments
%patch3 -p0 -b .LDFLAGS

%build
make -ef unix/Makefile prefix=%{prefix} CC="gcc %{optflags} -D_FILE_OFFSET_BITS=64" LDFLAGS="%{ldflags}" generic_gcc

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall -f unix/Makefile MANDIR=%{buildroot}%{_mandir}/man1 INSTALL=install

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS CHANGES INSTALL README TODO WHATSNEW WHERE LICENSE
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*
