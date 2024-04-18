%define filever %(echo %{version}|sed s/\\\\\.//)
%if %{cross_compiling}
%bcond_with pgo
%else
%bcond_without pgo
%endif

Name:		zip
Summary:	A file compression and packaging utility compatible with PKZIP
Version:	3.0
Release:	24
License:	BSD-like
Group:		Archiving/Compression
Url:		http://www.info-zip.org/pub/infozip/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/infozip/%{name}%{filever}.zip
Source100:	%{name}.rpmlintrc
Patch0:		zip-2.3-unforce-cflags.patch
Patch1:		zip-2.3-noninteractivepassword+testencrypedfile.patch
Patch2:		zip-3.0-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		zip-3.0-LDFLAGS.diff
Patch4:		https://raw.githubusercontent.com/gentoo/gentoo/master/app-arch/zip/files/zip-3.0-clang-15-configure-tests.patch
BuildRequires:	bzip2-devel

%description
The zip program is a compression and file packaging utility. Zip is analogous
to a combination of the UNIX tar and compress commands and is compatible with
PKZIP (a compression and file packaging utility for MS-DOS systems).

Install the zip package if you need to compress files using the zip program.

This version support crypto encryption.

%prep

%autosetup -p1 -n %{name}%{filever}

%build
%if %{with pgo}
make -ef unix/Makefile prefix=%{prefix} CC="%{__cc} %{optflags} -D_FILE_OFFSET_BITS=64 -fprofile-generate" CPP="%{__cc} -E" LDFLAGS="%{build_ldflags} -fprofile-generate" generic
./zip -9r __pgo_sources.zip *
./zipnote __pgo_sources.zip
llvm-profdata merge --output=zip.pgo *.profraw
make -ef unix/Makefile clean
make -ef unix/Makefile prefix=%{prefix} CC="%{__cc} %{optflags} -D_FILE_OFFSET_BITS=64 -fprofile-use=zip.pgo" CPP="%{__cc} -E" LDFLAGS="%{build_ldflags} -fprofile-use=zip.pgo" generic
%else
make -ef unix/Makefile prefix=%{prefix} CC="%{__cc} %{optflags} -D_FILE_OFFSET_BITS=64" CPP="%{__cc} -E" LDFLAGS="%{build_ldflags}" generic
%endif

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall -f unix/Makefile MANDIR=%{buildroot}%{_mandir}/man1 INSTALL=install

%files
%doc BUGS CHANGES INSTALL README TODO WHATSNEW WHERE LICENSE
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*

