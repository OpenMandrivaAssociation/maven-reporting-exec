%{?_javapackages_macros:%_javapackages_macros}
Name:           maven-reporting-exec
Version:        1.2
Release:        2.3
Group:		Development/Java
BuildArch:      noarch
Summary:        Classes to manage report plugin executions with Maven 3

License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-reporting-exec/
Source0:        http://repo1.maven.org/maven2/org/apache/maven/reporting/%{name}/%{version}/%{name}-%{version}-source-release.zip

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  mvn(org.apache.maven:maven-aether-provider)
BuildRequires:  mvn(org.apache.maven:maven-artifact)
BuildRequires:  mvn(org.apache.maven:maven-compat)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-embedder)
BuildRequires:  mvn(org.apache.maven:maven-model)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven:maven-settings)
BuildRequires:  mvn(org.apache.maven:maven-settings-builder)
BuildRequires:  mvn(org.apache.maven.plugins:maven-invoker-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:  mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-components:pom:)
BuildRequires:  mvn(org.apache.maven.shared:maven-shared-utils)
BuildRequires:  mvn(org.apache.maven.wagon:wagon-http-lightweight)
BuildRequires:  mvn(org.apache.velocity:velocity)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-velocity)
BuildRequires:  mvn(org.eclipse.aether:aether-api)
BuildRequires:  mvn(org.eclipse.aether:aether-transport-wagon)
BuildRequires:  mvn(org.eclipse.aether:aether-util)
BuildRequires:  mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildRequires:  mvn(velocity:velocity)

Patch0001:      0001-Port-to-Maven-3.1.0-Eclipse-Aether-and-Eclipse-Sisu.patch

Requires:       java-headless

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

# Build against Maven 3.x, Eclipse Aether and Eclipse Sisu
%pom_remove_dep org.sonatype.aether:aether-api
%pom_remove_dep org.sonatype.aether:aether-util
%pom_change_dep org.sonatype.aether:aether-connector-wagon org.eclipse.aether:aether-transport-wagon
%pom_change_dep org.sonatype.sisu:sisu-inject-plexus org.eclipse.sisu:org.eclipse.sisu.plexus

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
* Thu Jul 31 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-2
- Fix javadoc package generation

* Thu Jul 03 2014 Michal Srb <msrb@redhat.com> - 1.2-1
- Update to upstream version 1.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1-7
- Use Requires: java-headless rebuild (#1067528)

* Thu Oct  3 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-6
- Update Aether to 0.9.0.M3
- Add missing BuildRequires

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


