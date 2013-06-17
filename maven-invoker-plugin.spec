Summary:	Maven Invoker Plugin
Name:		maven-invoker-plugin
Version:	1.5
Release:	6
Group:		Development/Java
License:	ASL 2.0
Url:		http://maven.apache.org/plugins/maven-invoker-plugin/
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-invoker-plugin-1.5 maven-invoker-plugin    
# tar czf maven-invoker-plugin-1.5.tgz maven-invoker-plugin
Source0:	maven-invoker-plugin-1.5.tgz
BuildArch:	noarch

# Basic stuff
BuildRequires:	jpackage-utils
BuildRequires:	java-devel >= 0:1.6.0
# Maven and its dependencies
BuildRequires:	maven2
BuildRequires:	maven-resources-plugin
BuildRequires:	maven-plugin-plugin
BuildRequires:	maven-compiler-plugin
BuildRequires:	maven-install-plugin
BuildRequires:	maven-jar-plugin
BuildRequires:	maven-doxia
BuildRequires:	maven-doxia-tools
BuildRequires:	maven-doxia-sitetools
BuildRequires:	maven-surefire-provider-junit
BuildRequires:	maven-surefire-maven-plugin
BuildRequires:	maven-plugin-cobertura
BuildRequires:	maven-javadoc-plugin
BuildRequires:	maven-shared-invoker
# Others
BuildRequires:	groovy

Requires:	java
Requires:	groovy
Requires:	jpackage-utils
Requires:	maven2
Requires:	maven-shared-invoker
Requires:	maven-shared-reporting-api
Requires:	maven-shared-reporting-impl
Requires(post,postun):	jpackage-utils

Provides:	maven2-plugin-invoker = 1:%{version}-%{release}
Obsoletes:	maven2-plugin-invoker <= 0:2.0.8

%description
The Maven Invoker Plugin is used to run a set of Maven projects. The plugin 
can determine whether each project execution is successful, and optionally 
can verify the output generated from a given project execution.
  
%package javadoc
Group:		Development/Java
Summary:	Javadoc for %{name}
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -qn %{name}

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
	-e \
	-Dmaven.test.skip=true \
	-Dmaven2.jpp.mode=true \
	-Dmaven.repo.local=$MAVEN_REPO_LOCAL \
	install javadoc:javadoc

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
	do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins maven-invoker-plugin %{version} JPP maven-invoker-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
	%{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

