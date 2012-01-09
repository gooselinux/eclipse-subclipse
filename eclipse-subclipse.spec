%if 0%{?rhel} >= 6
%global debug_package %{nil}
%endif

%global eclipse_name       eclipse
%global eclipse_base       %{_libdir}/%{eclipse_name}
%global install_loc        %{_datadir}/eclipse/dropins
%global javahl_plugin_name org.tigris.subversion.clientadapter.javahl_1.6.4.1


Name:           eclipse-subclipse
Version:        1.6.5
Release:        6%{?dist}
Summary:        Subversion Eclipse plugin

Group:          Development/Tools
License:        EPL and CC-BY
URL:            http://subclipse.tigris.org/
Source0:        subclipse-%{version}.tgz
# Script to fetch the source code
Source10:       subclipse-fetch.sh
Patch0:         eclipse-subclipse-1.6.0-dependencies.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} >= 6
ExclusiveArch: i686 x86_64
%else
BuildArch: noarch
%endif

BuildRequires:          ant
BuildRequires:          jpackage-utils >= 0:1.6
BuildRequires:          coreutils
BuildRequires:          eclipse-pde
BuildRequires:          eclipse-gef
Requires:               eclipse-platform

BuildRequires:          eclipse-svnkit >= 1.2.2
Requires:               eclipse-svnkit >= 1.2.2
BuildRequires:          subversion-javahl >= 1.6
Requires:               subversion-javahl >= 1.6

Obsoletes:              eclipse-subclipse-book < 1.4

%description
Subclipse is an Eclipse plugin that adds Subversion integration to the Eclipse
IDE.

%package graph
Summary:        Subversion Revision Graph
Group:          Development/Tools

Requires:               %{name} = %{version}
Requires:               eclipse-gef

%description graph
Subversion Revision Graph for Subclipse.


%prep
%setup -q -n subclipse-%{version}
%patch0 -p1

# remove javahl sources
rm -rf org.tigris.subversion.clientadapter.javahl/src/org/tigris/subversion/javahl
ln -s %{_javadir}/svn-javahl.jar org.tigris.subversion.clientadapter.javahl

# fixing wrong-file-end-of-line-encoding warnings
sed -i 's/\r//' org.tigris.subversion.subclipse.graph/icons/readme.txt


%build
%{eclipse_base}/buildscripts/pdebuild            \
  -f org.tigris.subversion.clientadapter.feature 
%{eclipse_base}/buildscripts/pdebuild                   \
  -f org.tigris.subversion.clientadapter.javahl.feature 
%{eclipse_base}/buildscripts/pdebuild                   \
  -f org.tigris.subversion.clientadapter.svnkit.feature \
  -d svnkit
%{eclipse_base}/buildscripts/pdebuild \
  -f org.tigris.subversion.subclipse  
%{eclipse_base}/buildscripts/pdebuild              \
  -f org.tigris.subversion.subclipse.graph.feature \
  -d gef


%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{install_loc}

installBase=$RPM_BUILD_ROOT%{install_loc}
install -d -m 755 $installBase

# installing features
install -d -m 755 $installBase/subclipse-clientadapter
unzip -q -d $installBase/subclipse-clientadapter build/rpmBuild/org.tigris.subversion.clientadapter.feature.zip
install -d -m 755 $installBase/subclipse-clientadapter-javahl
unzip -q -d $installBase/subclipse-clientadapter-javahl build/rpmBuild/org.tigris.subversion.clientadapter.javahl.feature.zip
install -d -m 755 $installBase/subclipse-clientadapter-svnkit
unzip -q -d $installBase/subclipse-clientadapter-svnkit build/rpmBuild/org.tigris.subversion.clientadapter.svnkit.feature.zip
install -d -m 755 $installBase/subclipse
unzip -q -d $installBase/subclipse build/rpmBuild/org.tigris.subversion.subclipse.zip
install -d -m 755 $installBase/subclipse-graph
unzip -q -d $installBase/subclipse-graph build/rpmBuild/org.tigris.subversion.subclipse.graph.feature.zip

# replacing jar with links to system libraries
rm $installBase/subclipse-clientadapter-javahl/eclipse/plugins/%{javahl_plugin_name}/svn-javahl.jar
ln -s %{_javadir}/svn-javahl.jar $installBase/subclipse-clientadapter-javahl/eclipse/plugins/%{javahl_plugin_name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%{install_loc}/subclipse
%{install_loc}/subclipse-clientadapter*
%doc org.tigris.subversion.subclipse.graph/icons/readme.txt


%files graph
%defattr(-,root,root)
%{install_loc}/subclipse-graph


%changelog
* Fri Feb 12 2010 Andrew Overholt <overholt@redhat.com> 1.6.5-6
- Don't build debuginfo if building arch-specific packages.

* Thu Jan 21 2010 Andrew Overholt <overholt@redhat.com> 1.6.5-5
- Make arch-dependent (x86 and x86_64).

* Mon Dec 14 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-4
- Exclude arch different from x86 and x86_64.

* Sun Nov 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-3
- Fix typo.

* Sun Nov 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-2
- Do not pass non-existing folders to pdebuild -o.
- Switch to using %%global instead of %%define.

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.5-1
- Update to upstream 1.6.5.

* Mon Aug 10 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.4-1
- Update to upstream 1.6.4.

* Mon Jul 27 2009 Alexander Kurtakov <akurtako@redhat.com> 1.6.2-1
- Update to upstream 1.6.2.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 26 2009 Robert Marcano <robert@marcanoonline.com> 1.6.0-1
- Update to upstream 1.6.0

* Mon Mar 23 2009 Alexander Kurtakov <akurtako@redhat.com> 1.4.7-4
- Rebuild to not ship p2 context.xml.

* Tue Feb 24 2009 Robert Marcano <robert@marcanoonline.com> 1.4.7-3
- Update to upstream 1.4.7
- eclipse-subclipse-book is obsoleted, not provided upstream
- New eclipse-subclipse-graph subpackage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 13 2008 Alexander Kurtakov <akurtako@redhat.com> - 1.2.4-12
- Bump revision.

* Mon Oct 13 2008 Alexander Kurtakov <akurtako@redhat.com> - 1.2.4-11
- Fix build with eclipse 3.4.
- Rediff plugin-classpath.patch.

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.2.4-10
- Fix Patch0:/%%patch mismatch.

* Fri Apr 04 2008 Robert Marcano <robert@marcanoonline.com> 1.2.4-9
- Fix Bug 440818: changed links to svn-javahl.jar

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.4-7
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-6
- Build for all supported arquitectures

* Fri Oct 19 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-3
- Disable ppc64 build for f8, see Bug #298071

* Wed Sep 19 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-2
- Fix wrong applied classpath patch, fixing error: An error occurred while
automatically activating bundle org.tigris.subversion.subclipse.core

* Mon Sep 10 2007 Robert Marcano <robert@marcanoonline.com> 1.2.4-1
- Update to upstream 1.2.4
- Build for all supported arquitectures

* Sun Sep 09 2007 Robert Marcano <robert@marcanoonline.com> 1.2.2-6
- Change MANIFEST.MF patch to be applied on prep stage

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.2-4
- Rebuild for selinux ppc32 issue.

* Wed Jun 20 2007 Robert Marcano <robert@marcanoonline.com> 1.2.2-2
- Update to upstream 1.2.2
- Dependency changed from javasvn to svnkit
- Patch to support EPEL5 sent by Rob Myers

* Thu Dec 21 2006 Robert Marcano <robert@marcanoonline.com> 1.1.9-2
- Update to upstream 1.1.9
- Removed patch that added source attribute to the javac ant task
- Using the "eclipse" launcher

* Wed Nov 08 2006 Robert Marcano <robert@marcanoonline.com> 1.1.8-2
- Update to upstream 1.1.8

* Mon Aug 28 2006 Robert Marcano <robert@marcanoonline.com> 1.1.5-2
- Rebuild

* Mon Aug 21 2006 Robert Marcano <robert@marcanoonline.com> 1.1.5-1
- Update to upstream 1.1.5
- svnClientAdapter documentation files added. Subclipse includes an eclipse
  based documentation for the plugins

* Sat Aug 06 2006 Robert Marcano <robert@marcanoonline.com> 1.1.4-1
- Update to upstream 1.1.4
- License changed to EPL
- svnClientAdapter-1.1.4-javac-target.patch added fix to svnClientAdapter ant
  script

* Tue Jul 04 2006 Andrew Overholt <overholt@redhat.com> 1.0.3-2
- Use versionless pde.build.
- Remove strict SDK version requirement due to above.

* Sun Jul 02 2006 Robert Marcano <robert@marcanoonline.com> 1.0.3-2
- Embeeding the script that fetch the source code

* Sun Jun 25 2006 Robert Marcano <robert@marcanoonline.com> 1.0.3-1
- Update to 1.0.3
- Dependency name changed to ganymed-ssh2

* Sun Jun 11 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-6
- rpmlint fixes and debuginfo generation workaround

* Thu Jun 01 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-5
- Use package-build from eclipse SDK

* Sun May 28 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-4
- Integrated svnClientAdapter inside this package

* Tue May 23 2006 Ben Konrath <bkonrath@redhat.com> 1.0.1-3
- Rename package to eclipse-subclipse.
- Use copy-platform script for now.

* Sun May 07 2006 Robert Marcano <robert@marcanoonline.com> 1.0.1-2
- use external libraries from dependent packages

* Wed Apr 26 2006 Ben Konrath <bkonrath@redhat.com> 1.0.1-1
- initial version based on the work of Robert Marcano
