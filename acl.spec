Summary: Access control list utilities.
Name: acl
Version: 2.2.23
Release: 5
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: libattr-devel >= 2.4.1
Source: http://acl.bestbits.at/current/tar/acl-%{version}.src.tar.gz
Patch0: acl-2.2.3-multilib.patch
BuildRequires: autoconf, libtool >= 1.5, gettext
License: GPL
Group: System Environment/Base
URL: http://acl.bestbits.at/

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support.
Copyright: LGPL
Group: System Environment/Libraries
Prereq: /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Access control list static libraries and headers.
Copyright: LGPL
Group: Development/Libraries
Requires: libacl, libattr-devel

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch0 -p1 -b .multilib
autoconf

%build
touch .census
# acl abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make LIBTOOL="libtool --tag=CC"

%install
rm -rf $RPM_BUILD_ROOT
DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB
make install DIST_MANIFEST="$DIST_INSTALL" PKG_DOC_DIR=%{_docdir}/acl-%{version}
make install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
make install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"

# Buahhh, ugly hack, but it works.
perl -pi -e 's|^f 644|f 755|' $DIST_INSTALL_LIB
chmod 755 $RPM_BUILD_ROOT/lib/*

files()
{
	sort | uniq | awk ' 
$1 == "d" { 
	    if (match ($6, "/usr/include/acl"))
		printf ("%%%%dir %%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $5); } 
$1 == "f" { if (match ($6, "/usr/share/man") || match ($6, "/usr/share/doc/acl"))
		printf ("%%%%doc ");
	    if (match ($6, "/usr/share/man"))
		printf ("%%%%attr(%s,%s,%s) %s*\n", $2, $3, $4, $6);
	    else
		printf ("%%%%attr(%s,%s,%s) %s\n", $2, $3, $4, $6); }
$1 == "l" { if (match ($3, "/usr/share/man") || match ($3, "/usr/share/doc/acl"))
		printf ("%%%%doc ");
	    if (match ($3, "/usr/share/man"))
		printf ("%%%%attr(0777,root,root) %s*\n", $3);
	    else
		printf ("%%%%attr(0777,root,root) %s\n", $3); }'
}
set +x
files < "$DIST_INSTALL" > files.rpm
files < "$DIST_INSTALL_DEV" > filesdevel.rpm
files < "$DIST_INSTALL_LIB" > fileslib.rpm
set -x

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f files.rpm
%defattr(-,root,root)
%doc %{_docdir}/acl-%{version}

%files -n libacl-devel -f filesdevel.rpm
%defattr(-,root,root)
/usr/include/acl

%files -n libacl -f fileslib.rpm

%changelog
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
