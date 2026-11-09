# pam-gnupg

Fedora/COPR packaging for <https://github.com/cruegge/pam-gnupg>.
The spec pins the full upstream commit; no network is needed during RPM builds.

Generate an SRPM (dependency installation requires root):

```sh
make -f .copr/Makefile srpm spec=pam-gnupg/pam-gnupg.spec
```

The package installs `/usr/lib64/security/pam_gnupg.so` on x86_64 and
`/usr/libexec/pam_gnupg_helper`. It does not edit PAM configuration.
For login services, run `auth optional pam_gnupg.so store-only` after password
authentication, then `session optional pam_gnupg.so` after `pam_systemd.so`.
Account for `sufficient` rules that may skip later modules; Fedora's `postlogin`
include runs after the `system-auth`/`password-auth` substack in login and SDDM.

Enable `allow-preset-passphrase` in `~/.gnupg/gpg-agent.conf`, and put the desired
keygrips from `gpg -K --with-keygrip` into `~/.pam-gnupg`, one per line. The
GnuPG passphrase must match the password entered at login. Automatic login and
passwordless authentication cannot provide a passphrase.
