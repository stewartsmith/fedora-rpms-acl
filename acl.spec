Summary: Access control list utilities.
Name: acl
Version: 2.2.3
Release: 1
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: libattr-devel
Source: http://acl.bestbits.at/current/tar/acl-%{version}.src.tar.gz
Patch: acl-2.2.3-multilib.patch
BuildRequires: autoconf
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
Requires: libacl

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch -p1 -b .multilib
autoconf

%build
touch .census
# acl abuses libexecdir
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make

%install
rm -rf $RPM_BUILD_ROOT
DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB
make install DIST_MANIFEST="$DIST_INSTALL"
make install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
make install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"

chmod +x ${RPM_BUILD_ROOT}/%{_lib}/libacl.so.*

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

%files -n libacl-devel -f filesdevel.rpm

%files -n libacl -f fileslib.rpm

%changelog
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
