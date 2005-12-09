Summary: Access control list utilities.
Name: acl
Version: 2.2.32
Release: 2.1.1
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libattr-devel >= 2.4.1
Source: ftp://oss.sgi.com/projects/xfs/cmd_tars/acl-%{version}.src.tar.gz
Patch0: acl-2.2.3-multilib.patch
Patch1: acl-2.2.32-build.patch
BuildRequires: autoconf, libtool >= 1.5, gettext
License: GPL
Group: System Environment/Base
URL: http://acl.bestbits.at/

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support.
License: LGPL
Group: System Environment/Libraries
Prereq: /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Access control list static libraries and headers.
License: LGPL
Group: Development/Libraries
Requires: libacl, libattr-devel

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch0 -p1 -b .multilib
%patch1 -p1 -b .build
autoconf

%build
touch .census
# acl abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make LIBTOOL="libtool --tag=CC"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# get rid of libacl.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libacl.la

# fix links to shared libs and permissions
rm -f $RPM_BUILD_ROOT/%{_libdir}/libacl.so
ln -s /%{_lib}/libacl.so $RPM_BUILD_ROOT/%{_libdir}/libacl.so
chmod 0755 $RPM_BUILD_ROOT/%{_lib}/libacl.so.*.*.*

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl
%{_datadir}/doc/acl-%{version}
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man5/acl.5*

%files -n libacl-devel
%defattr(-,root,root)
/%{_lib}/libacl.so
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_libdir}/libacl.*
%{_mandir}/man3/acl_*

%files -n libacl
%defattr(-,root,root)
/%{_lib}/libacl.so.*

%changelog
* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.2.32-2.1
- fixed permissions of libacl

* Tue Dec  6 2005 Thomas Woerner <twoerner@redhat.com> 2.2.32-2
- spec file cleanup
- mark po files as lang specific

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 2.2.32

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.2.31-1
- update to 2.2.31

* Wed Sep 28 2005 Than Ngo <than@redhat.com> 2.2.23-9
- get rid of *.la files
- remove duplicate doc files

* Wed Feb  9 2005 Stephen C. Tweedie <sct@redhat.com> 2.2.23-6
- Rebuild

* Thu Sep 16 2004 Jeremy Katz <katzj@redhat.com> - 2.2.23-5
- make the libs executable so that we find their dependencies (#132696)

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.23-4
- libacl-devel Requires: libattr-devel for libattr.la

* Fri Sep 10 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.23-3
- Requires libtool >= 1.5 for building

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.2.23-2
- Make libacl.so.* executable.

* Thu Aug 19 2004 Phil Knirsch <pknirsch@redhat.com> 2.2.23-1
- Update to latest upstream version.

* Sun Aug  8 2004 Alan Cox <alan@redhat.com> 2.2.7-7
- Close bug #125300 (Steve Grubb: build requires libtool,gettext)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 31 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.7-5
- Add missing %defattr

* Tue Mar 30 2004 Stephen C. Tweedie <sct@redhat.com> 2.2.7-3
- Add /usr/include/acl to files manifest
- Fix location of doc files, add main doc dir to files manifest

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Aug  5 2003 Elliot Lee <sopwith@redhat.com> 2.2.7-2
- Fix libtool invocation

* Tue Jun  3 2003 Stephen C. Tweedie <sct@redhat.com> 2.2.7-1
- Update to acl-2.2.7

* Wed Mar 26 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.3-2
- include patch from Jay Berkenbilt to print better error messages

* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 2.2.3-1
- udpate/rebuild

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.0.11-7
- set execute bits on library so that requires are generated.

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.11-5
- Correct patch in previous fix so that shared libraries go in /lib* 
  instead of /usr/lib*

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.11-4
- Fix multilibbing

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 2.0.11-3
- Added fix to install libs in correct directory on 64bit machine

* Thu Aug 08 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.11-2
- Made the package only own the one directory that is unique to it:
  /usr/include/acl

* Mon Jun 24 2002 Michael K. Johnson <johnsonm@redhat.com> 2.0.11-1
- Initial Red Hat package
  Made as few changes as possible relative to upstream packaging to
  make it easier to maintain long-term.  This means that some of
  the techniques used here are definitely not standard Red Hat
  techniques.  If you are looking for an example package to fit
  into Red Hat Linux transparently, this would not be the one to
  pick.
- acl-devel -> libacl-devel
