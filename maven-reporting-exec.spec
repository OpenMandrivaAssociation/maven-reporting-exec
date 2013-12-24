%_javapackages_macros
Name:           maven-reporting-exec
Version:        1.1
Release:        5.0%{?dist}
BuildArch:      noarch
Summary:        Classes to manage report plugin executions with Maven 3

License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-reporting-exec/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/reporting/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildRequires:  maven-local
BuildRequires:  aether-api >= 1:0
BuildRequires:  aether-util >= 1:0
BuildRequires:  aether-transport-wagon >= 1:0
BuildRequires:  sisu-plexus >= 1:0
BuildRequires:  maven-invoker-plugin
BuildRequires:  maven-surefire-plugin
BuildRequires:  plexus-containers-component-metadata

Patch0001:      0001-Port-to-Maven-3.1.0-Eclipse-Aether-and-Eclipse-Sisu.patch

Requires:       java

%description
Classes to manage report plugin executions with Maven 3. Contains classes for
managing and configuring reports and their execution.

%package javadoc
Summary:        API documentation for %{name}

%description javadoc
The API documentation of %{name}.



%prep
%setup -qn %{name}-%{version}
%patch0001 -p1

# convert CR+LF to LF
sed -i 's/\r//g' pom.xml src/main/java/org/apache/maven/reporting/exec/*

%pom_remove_plugin org.apache.maven.plugins:maven-enforcer-plugin

%build
# Test are skipped because there are errors with PlexusLogger
# More info possibly here:
# https://docs.sonatype.org/display/AETHER/Using+Aether+in+Maven+Plugins?focusedCommentId=10485782#comment-10485782
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE



%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-4
- Port to Maven 3.1.0, Eclipse Aether and Eclipse Sisu
- Resolves: rhbz#985706

* Mon Jun 10 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-3
- Remove unused source

* Mon May 06 2013 Tomas Radej <tradej@redhat.com> - 1.1-2
- Removed aether BR

* Mon Apr 22 2013 Tomas Radej <tradej@redhat.com> - 1.1-1
- Updated to latest upstream version
- Building with maven-local

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.2-3
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Tomas Radej <tradej@redhat.com> - 1.0.2-1
- Updated to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 12 2011 tradej <tradej@redhat.com> 1.0.1-3
- Added dist macro to release

* Thu Aug 11 2011 tradej <tradej@redhat.com> 1.0.1-2
- Changed BuildArch to noarch

* Wed Aug 10 2011 tradej <tradej@redhat.com> 1.0.1-1
- Initial release (thanks to akurtakov, jcapik and the GULaG team for help)

