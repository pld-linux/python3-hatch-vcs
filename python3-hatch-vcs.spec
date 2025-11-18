#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	hatch-vcs
Summary:	Hatch plugin for versioning with your preferred VCS
Summary(pl.UTF-8):	Wtyczka Hatcha do wersjonowania ulubionym VCS
Name:		python3-%{module}
Version:	0.5.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/hatch-vcs/
Source0:	https://files.pythonhosted.org/packages/source/h/hatch-vcs/hatch_vcs-%{version}.tar.gz
# Source0-md5:	9a22a9f7203783e526959d34510a9672
URL:		https://pypi.org/project/hatch-vcs/
BuildRequires:	python3-build
BuildRequires:	python3-hatchling >= 1.1.0
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools_scm >= 8.2.0
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.9
Obsoletes:	python3-hatch_vcs < 0.4.0-10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This provides a plugin for Hatch that uses your preferred version
control system (like Git) to determine project versions.

%description -l pl.UTF-8
Ten pakiet zawiera wtyczkę Hatcha, wykorzystującą ulubiony system
kontroli wersji (np. Git) do określania wersji pakietów.

%prep
%setup -q -n hatch_vcs-%{version}

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt HISTORY.md README.md
%{py3_sitescriptdir}/hatch_vcs
%{py3_sitescriptdir}/hatch_vcs-%{version}.dist-info
