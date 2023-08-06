%define name              ligo-lvalert
%define version           1.5.6
%define unmangled_version 1.5.6
%define release           1

Summary:   LVAlert Client Tools
Name:      %{name}
Version:   %{version}
Release:   %{release}%{?dist}
Source0:   %{name}-%{unmangled_version}.tar.gz
License:   GPLv2+
Group:     Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:    %{_prefix}
Vendor:    Tanner Prestegard <tanner.prestegard@ligo.org>, Alexander Pace <alexander.pace@ligo.org>, Leo Singer <leo.singer@ligo.org>
Url:       https://wiki.ligo.org/DASWG/LVAlert

BuildArch: noarch
BuildRequires: rpm-build
BuildRequires: epel-rpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros
BuildRequires: python-setuptools
BuildRequires: python%{python3_pkgversion}-setuptools

%description
LVAlert is an XMPP-based alert system. This package provides client
tools for interacting with the LVAlert jabber server.


# -- python2-ligo-lvalert

%package -n python2-%{name}
Summary:  %{summary}
Provides: %{name}
Obsoletes: %{name}
Requires: python-six
Requires: python2-ligo-common
Requires: pyxmpp
Requires: python-sleekxmpp

%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
LVAlert is an XMPP-based alert system. This package provides client
tools for interacting with the LVAlert jabber server.


# -- python-3X-ligo-lvalert

%package -n python%{python3_pkgversion}-%{name}
Summary:  %{summary}
Requires: python%{python3_pkgversion}-six
Requires: python%{python3_pkgversion}-ligo-common
Requires: python%{python3_pkgversion}-sleekxmpp

%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}

%description -n python%{python3_pkgversion}-%{name}
LVAlert is an XMPP-based alert system. This package provides client
tools for interacting with the LVAlert jabber server.

# -- build steps

%prep
%setup -n %{name}-%{unmangled_version}

%build
# build python3 first
%py3_build
# so that the scripts come from python2
%py2_build

%install
%py3_install
%py2_install

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python2-%{name}
%license COPYING
%{_bindir}/lvalert
%{_bindir}/lvalert_*
%{python2_sitelib}/*
%exclude %{python_sitelib}/ligo/lvalert/*pyo

%files -n python%{python3_pkgversion}-%{name}
%license COPYING
%{python3_sitelib}/*
