Name:           pass-secret-service
Version:        0.7.1
Release:        1%{?dist}
Summary:        Secret Service API implementation backed by a pass password store
# Upstream is GPL-3.0-only. Bundled crates use MIT, Apache-2.0 and BSD-3-Clause;
# choose MIT or Apache-2.0 where upstream offers alternative licenses.
License:        GPL-3.0-only AND MIT AND Apache-2.0 AND BSD-3-Clause
URL:            https://github.com/grimsteel/pass-secret-service
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Generated from the upstream Cargo.lock by the SRPM Makefile.
Source1:        %{name}-%{version}-vendor.tar.xz

BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  systemd-rpm-macros
Requires:       gnupg2
Recommends:     pass
%{?systemd_ordering}

%description
An implementation of the org.freedesktop.secrets D-Bus API using a pass-compatible
password store. Secrets are encrypted with GnuPG; attributes are not encrypted.
Includes a systemd user service and D-Bus session activation support.

%prep
%autosetup -a 1
%cargo_prep -v vendor

%build
%cargo_build
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest
mkdir -p bundled-licenses
find vendor -type f \( -iname 'LICENSE*' -o -iname 'COPYING*' -o -iname 'NOTICE*' \) \
    -exec cp --parents -t bundled-licenses {} +

%install
install -Dpm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm0644 systemd/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service
install -Dpm0644 systemd/org.freedesktop.secrets.service \
    %{buildroot}%{_datadir}/dbus-1/services/org.freedesktop.secrets.service

%check
%cargo_test

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%files
%license LICENSE LICENSE.dependencies cargo-vendor.txt bundled-licenses
%doc README.md
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service
%{_datadir}/dbus-1/services/org.freedesktop.secrets.service

%changelog
* Sun Nov 08 2026 chlorodose - 0.7.1-1
- Initial package
