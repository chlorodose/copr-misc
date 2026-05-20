Name:           bootc-save-machine-id
Version:        0.1.0
Release:        1%{?dist}
Summary:        Persist systemd machine-id via EFI variables for bootc systems

License:        Apache-2.0
URL:            https://github.com/chlorodose/bootc-save-machine-id
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

Requires:       dracut
Requires:       systemd
Requires:       bootc

BuildRequires:  systemd

%description
bootc-save-machine-id provides an initrd dracut module and a systemd
service to persist the systemd machine-id across bootc-based system
deployments using EFI variables.

During initrd, the machine-id is read from the EFI variable
SystemdMachineId and bind-mounted to /etc/machine-id, ensuring the
same machine-id is used across reboots. A systemd service commits
a newly generated machine-id to the EFI variable on first boot.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build

%install
# Dracut module
install -Dpm 0644 usr/lib/dracut/modules.d/90bootc-save-machine-id/module-setup.sh \
    %{buildroot}%{_prefix}/lib/dracut/modules.d/90bootc-save-machine-id/module-setup.sh
install -Dpm 0644 usr/lib/dracut/modules.d/90bootc-save-machine-id/initrd-prepare-machine-id-efi.service \
    %{buildroot}%{_prefix}/lib/dracut/modules.d/90bootc-save-machine-id/initrd-prepare-machine-id-efi.service

# Scripts
install -Dpm 0755 usr/libexec/initrd-prepare-machine-id-efi \
    %{buildroot}%{_libexecdir}/initrd-prepare-machine-id-efi
install -Dpm 0755 usr/libexec/commit-machine-id-efi \
    %{buildroot}%{_libexecdir}/commit-machine-id-efi

# Systemd unit
install -Dpm 0644 usr/lib/systemd/system/commit-machine-id-efi.service \
    %{buildroot}%{_unitdir}/commit-machine-id-efi.service

# Systemd preset
install -Dpm 0644 usr/lib/systemd/system-preset/10-commit-machine-id-efi.conf \
    %{buildroot}%{_presetdir}/10-commit-machine-id-efi.conf

%post
%systemd_post commit-machine-id-efi.service

%preun
%systemd_preun commit-machine-id-efi.service

%postun
%systemd_postun_with_restart commit-machine-id-efi.service

%files
%license LICENSE
%{_prefix}/lib/dracut/modules.d/90bootc-save-machine-id/
%{_libexecdir}/initrd-prepare-machine-id-efi
%{_libexecdir}/commit-machine-id-efi
%{_unitdir}/commit-machine-id-efi.service
%{_presetdir}/10-commit-machine-id-efi.conf

%changelog
* Wed May 20 2026 chlorodose <chlorodose@github.com> - 0.1.0-1
- Initial packaging
