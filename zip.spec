%define filever %(echo -n %{version} |cut -d. -f1-2 |sed -e 's,\\.,,')d%(echo -n %{version} |cut -d. -f3)_s%(echo -n %{version} |cut -d. -f4)

Name:		zip
Summary:	A file compression and packaging utility compatible with PKZIP
Version:	3.1.34.3
Release:	1
License:	BSD-like
Group:		Archiving/Compression
Url:		http://www.info-zip.org/pub/infozip/
Source0:	http://antinode.info/ftp/info-zip/zip%{filever}.zip
Source100:	%{name}.rpmlintrc
Patch0:		zip-2.3-unforce-cflags.patch
BuildRequires:	bzip2-devel

%description
The zip program is a compression and file packaging utility. Zip is analogous
to a combination of the UNIX tar and compress commands and is compatible with
PKZIP (a compression and file packaging utility for MS-DOS systems).

Install the zip package if you need to compress files using the zip program.

This version support crypto encryption.

%prep

%setup -qn %{name}%(echo -n %{filever} |cut -d_ -f1)
%patch0 -p1 -b .cflags

%build
make -ef unix/Makefile prefix=%{prefix} CC="%{__cc} %{optflags} -D_FILE_OFFSET_BITS=64" CPP="%{__cc} -E" LDFLAGS="%{ldflags}" PREFIX=%{_prefix} generic

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall -f unix/Makefile MANDIR=%{buildroot}%{_mandir}/man1 PREFIX=%{buildroot}%{_prefix} INSTALL=install

%files
%doc BUGS CHANGES INSTALL README TODO WHATSNEW WHERE LICENSE
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*

