Name:           niri-computer-use
Version:        0.1.8
Release:        1%{?dist}
Summary:        MCP server for observing and controlling a niri Wayland desktop
# Upstream is MIT; the linked niri-ipc crate is GPL-3.0-or-later.
# Additional bundled dependency licenses are reviewed with cargo_license_summary.
License:        MIT AND GPL-3.0-or-later AND Apache-2.0 AND Unicode-3.0
URL:            https://github.com/ayagmar/niri-computer-use
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Generated from the upstream Cargo.lock by the SRPM Makefile.
Source1:        %{name}-%{version}-vendor.tar.xz
Source2:        README.md

BuildRequires:  rust >= 1.99
BuildRequires:  cargo >= 1.99
BuildRequires:  rust-packaging
BuildRequires:  gcc
BuildRequires:  pkgconfig(xkbcommon)
# The installer tests exercise interactive prompts through script(1).
BuildRequires:  /usr/bin/script
# Protocol tests launch a private accessibility bus.
BuildRequires:  /usr/bin/dbus-daemon
BuildRequires:  curl
BuildRequires:  tar
BuildRequires:  gzip
BuildRequires:  /usr/bin/hardlink
Requires:       niri >= 26.04
Requires:       grim
Requires:       systemd
Recommends:     libnotify

%description
An MCP server that lets AI agents observe and control a niri Wayland desktop
through niri IPC, screenshots, accessibility, keyboard and pointer tools.
Desktop actions are gated by a lease and a user-controlled stop key.

Includes the upstream agent skill and optional Noctalia plugin in the shared
data directory. See README.fedora.md for setup.

%prep
%autosetup -a 1
%cargo_prep -v vendor
cp %{SOURCE2} README.fedora.md

%build
# The workspace also contains a development harness; only ship the server.
%cargo_build -- -p %{name}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
%cargo_vendor_manifest
mkdir -p bundled-licenses
find vendor -type f \( -iname 'LICENSE*' -o -iname 'COPYING*' -o -iname 'NOTICE*' \) \
    -exec cp --parents -t bundled-licenses {} +

%install
install -Dpm0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}/{skills,noctalia}
cp -a skills/%{name} %{buildroot}%{_datadir}/%{name}/skills/
cp -a noctalia/%{name} %{buildroot}%{_datadir}/%{name}/noctalia/
rm -rf %{buildroot}%{_datadir}/%{name}/noctalia/%{name}/tests
mkdir -p %{buildroot}%{_licensedir}/%{name}
cp -a LICENSE LICENSE.dependencies cargo-vendor.txt bundled-licenses \
    %{buildroot}%{_licensedir}/%{name}/
# Preserve every crate's notices while sharing identical license texts.
hardlink -c %{buildroot}%{_licensedir}/%{name}

%check
%cargo_test -- -p %{name}
NCU_PROTOCOL_MODE=shared %cargo_test -- -p %{name} --test protocol
target/release/%{name} --version

%files
%license %{_licensedir}/%{name}/
%doc README.md README.fedora.md CHANGELOG.md
%{_bindir}/%{name}
%{_datadir}/%{name}/

%changelog
* Tue Nov 10 2026 lilith - 0.1.8-1
- Initial package
