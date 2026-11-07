# pass-secret-service

Fedora/COPR packaging for <https://github.com/grimsteel/pass-secret-service>.

Generate an SRPM using the repository's COPR entry point (the dependency
installation step requires root, as with the other packages):

```sh
make -f .copr/Makefile srpm spec=pass-secret-service/pass-secret-service.spec
```

The package Makefile downloads the tagged source and vendors the dependencies
from its `Cargo.lock` into a separate source archive. RPM builds use these
dependencies offline. To update, change `Version` in the spec and add a changelog
entry; both source archives are regenerated for the new version. Review the
dependency license summary when updating.

After installation, initialize your password store with `pass init` if needed.
The service can be started on demand through D-Bus or explicitly with
`systemctl --user start pass-secret-service.service`. Its unit is D-Bus activated
and does not need to be enabled. Another provider of `org.freedesktop.secrets`
(such as GNOME Keyring or KeePassXC) must not already own the session bus name;
configure your desktop to use the desired provider.
