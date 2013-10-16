%define version 3.0
%define filever %(echo %version|sed s/\\\\\.//)

Name:		zip
Summary:	A file compression and packaging utility compatible with PKZIP
Version:	%{version}
Release:	9
License:	BSD-like
Group:		Archiving/Compression
URL:		http://www.info-zip.org/pub/infozip/
Source0:	http://dfn.dl.sourceforge.net/sourceforge/infozip/%{name}%{filever}.zip
Patch0:		zip-2.3-unforce-cflags.patch
Patch1:		zip-2.3-noninteractivepassword+testencrypedfile.patch
Patch2:		zip-3.0-format_not_a_string_literal_and_no_format_arguments.diff
Patch3:		zip-3.0-LDFLAGS.diff
BuildRequires:	bzip2-devel

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
make -ef unix/Makefile prefix=%{prefix} CC="%{__cc} %{optflags} -D_FILE_OFFSET_BITS=64" LDFLAGS="%{ldflags}" generic_gcc

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall -f unix/Makefile MANDIR=%{buildroot}%{_mandir}/man1 INSTALL=install

%files
%doc BUGS CHANGES INSTALL README TODO WHATSNEW WHERE LICENSE
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0-5mdv2011.0
+ Revision: 671958
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0-4mdv2011.0
+ Revision: 608286
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0-3mdv2010.1
+ Revision: 519086
- rebuild

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-2mdv2009.1
+ Revision: 317973
- fix build with -Werror=format-security (P2)
- use %%ldflags (P3)

* Mon Aug 18 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0-1mdv2009.0
+ Revision: 273212
- 3.0
- rediffed P1
- drop S1, zcrypt is included
- fix url

* Mon Feb 25 2008 Olivier Blin <oblin@mandriva.com> 2.32-2mdv2008.1
+ Revision: 174802
- build with _FILE_OFFSET_BITS=64 (#37178)
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill packager tag


* Thu Nov 16 2006 Olivier Blin <oblin@mandriva.com> 2.32-1mdv2007.0
+ Revision: 85007
- fix patchlevel
- rediff patch1
- 2.32
- bunzip2 sources
- Import zip

* Sat Dec 31 2005 Stefan van der Eijk <stefan@eijk.nu> 2.31-2mdk
- %%mkrel
- rebuild
- comment out Packager tag

* Tue Jun 07 2005 Götz Waschk <waschk@mandriva.org> 2.31-1mdk
- drop patch 2, CAN-2004-1010 was fixed upstream
- new version

* Wed Dec 15 2004 Götz Waschk <waschk@linux-mandrake.com> 2.3-13mdk
- add man page symlinks

* Sun Nov 28 2004 Olivier Blin <blino@mandrake.org> 2.3-12mdk
- security update for CAN-2004-1010

* Tue Sep 14 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 2.3-11mdk
- Rebuilt.

