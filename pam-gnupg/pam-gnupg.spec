%global commit 3be7745e859a63ea6dc7ebd7d4f1915307289d8b

Name:           pam-gnupg
Version:        0.1^20230117git3be7745
Release:        1%{?dist}
Summary:        Unlock GnuPG keys with the login password
License:        GPL-3.0-only
URL:            https://github.com/cruegge/pam-gnupg
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pam-devel
BuildRequires:  gnupg2
Requires:       gnupg2
Requires:       pam

%description
A PAM module that passes the login password to gpg-agent. Users opt in by
listing keygrips in ~/.pam-gnupg and enabling allow-preset-passphrase in
~/.gnupg/gpg-agent.conf. The GnuPG passphrase must match the login password.
This package does not change PAM configuration automatically.

%prep
%autosetup -n %{name}-%{commit}
autoreconf -fiv

%build
%configure --with-moduledir=%{_libdir}/security
%make_build

%install
%make_install

%check
%make_build check
test -f %{buildroot}%{_libdir}/security/pam_gnupg.so
test -x %{buildroot}%{_libexecdir}/pam_gnupg_helper

%files
%license LICENSE
%doc README.md
%{_libdir}/security/pam_gnupg.so
%{_libexecdir}/pam_gnupg_helper

%changelog
* Mon Nov 09 2026 chlorodose - 0.1^20230117git3be7745-1
- Package pinned upstream snapshot with Fedora PAM and libexec paths
