Name:		maven-reporting-exec
Version:	2.0.1
Release:	1
Summary:	Run Maven report plugins
Group:		Development/Java
License:	Apache-2.0
URL:		https://maven.apache.org/shared/maven-reporting-exec/
Source0:	https://github.com/apache/maven-reporting-exec/archive/refs/tags/maven-reporting-exec-%{version}.tar.gz#/maven-reporting-exec-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
# The maven RPM holds the class jars. maven-components owns the coordinates.
BuildRequires:	maven
BuildRequires:	maven-components >= 3.10.0
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.apache.maven.reporting:maven-reporting-api)
BuildRequires:	maven-reporting-api >= 1:4.0.0
Requires:	maven-reporting-api >= 1:4.0.0
BuildRequires:	mvn(org.apache.maven:maven-core)
BuildRequires:	mvn(org.apache.maven:maven-model)
BuildRequires:	mvn(org.apache.maven:maven-plugin-api)
BuildRequires:	mvn(org.apache.maven:maven-artifact)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	plexus-utils >= 3.6.2
Requires:	plexus-utils >= 3.6.2
BuildRequires:	mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:	doxia-sink-api >= 2.2.0
Requires:	doxia-sink-api >= 2.2.0
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(javax.inject:javax.inject)
# javax.inject and jakarta-inject both provide this coordinate.
BuildRequires:	javax.inject >= 1-2
Requires:	javax.inject >= 1-2
BuildRequires:	mvn(org.apache.maven.resolver:maven-resolver-api)
BuildRequires:	mvn(org.apache.maven.resolver:maven-resolver-util)
BuildRequires:	mvn(org.codehaus.plexus:plexus-classworlds)
BuildRequires:	plexus-classworlds >= 2.8.0
Requires:	plexus-classworlds >= 2.8.0
BuildRequires:	mvn(org.eclipse.sisu:org.eclipse.sisu.plexus)
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

Obsoletes:	maven-reporting-exec-javadoc < %{EVRD}

%description
Loads a Maven report plugin and runs its report goals. 2.0.1 uses
reporting API 4.0.0, Doxia sink API 2.2.0, and resolver 2.0.24.
Xpp3Dom comes from plexus-utils 3.6.2. Tests are not run.

%prep
%autosetup -n maven-reporting-exec-maven-reporting-exec-%{version}
rm -rf src/test src/it .github
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.reporting")
add(root, "artifactId", "maven-reporting-exec")
add(root, "version", "%{version}")
add(root, "name", "Apache Maven Reporting Executor")
props = ET.SubElement(root, tag("properties"))
add(props, "maven.compiler.release", "8")
add(props, "project.build.sourceEncoding", "UTF-8")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version, scope in (
    ("org.apache.maven.reporting", "maven-reporting-api", "4.0.0", ""),
    ("org.apache.maven", "maven-core", "3.10.0", "provided"),
    ("org.apache.maven", "maven-model", "3.10.0", "provided"),
    ("org.apache.maven", "maven-plugin-api", "3.10.0", "provided"),
    ("org.apache.maven", "maven-artifact", "3.10.0", "provided"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.2", ""),
    ("org.apache.maven.doxia", "doxia-sink-api", "2.2.0", ""),
    ("org.slf4j", "slf4j-api", "1.7.36", ""),
    ("javax.inject", "javax.inject", "1", ""),
    ("org.apache.maven.resolver", "maven-resolver-api", "2.0.24", ""),
    ("org.apache.maven.resolver", "maven-resolver-util", "2.0.24", ""),
    ("org.codehaus.plexus", "plexus-classworlds", "2.8.0", ""),
    ("org.eclipse.sisu", "org.eclipse.sisu.plexus", "0.9.0.M3", ""),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
    if scope:
        add(dep, "scope", scope)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
# Sisu loads @Named classes from this index. The indexer plugin is not packaged.
python - <<'PY'
import re
from pathlib import Path
root = Path("src/main/java")
names = []
for path in sorted(root.rglob("*.java")):
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*?$", "", text, flags=re.M)
    match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
    if not match:
        continue
    if "@Named" not in text[:match.start()]:
        continue
    pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
    if not pkg:
        continue
    names.append(pkg.group(1) + "." + match.group(1))
if names:
    dest = Path("src/main/resources/META-INF/sisu")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY

%files -f .mfiles
%doc LICENSE README.md
