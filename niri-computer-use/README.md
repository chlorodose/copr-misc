# niri-computer-use

Fedora/COPR packaging for <https://github.com/ayagmar/niri-computer-use>.

Generate an SRPM through the repository's COPR entry point (the dependency
installation step requires root):

```sh
make -f .copr/Makefile srpm spec=niri-computer-use/niri-computer-use.spec
```

The Makefile downloads the tagged source and vendors the dependencies from its
`Cargo.lock`. RPM builds use the vendor archive offline and require Rust 1.99 or
newer. To update, change `Version` in the spec and add a changelog entry; review
the dependency license summary for the new version.

## Setup

Inside your niri session, check readiness:

```sh
niri-computer-use status
```

Upstream supports desktop actions on niri 26.04. Other major/minor versions
operate in read-only mode. The server uses `grim` for screenshots and `loginctl`
for session checks. The recommended `libnotify` package provides `notify-send`
for optional lease confirmation.

Configure your MCP client to run `/usr/bin/niri-computer-use` with the argument
`serve`. Bind the stop key in your niri configuration:

```kdl
binds {
    Mod+Shift+Escape allow-inhibiting=false allow-when-locked=true hotkey-overlay-title="Stop the AI agent (niri-computer-use)" {
        spawn "/usr/bin/niri-computer-use" "stop";
    }
}
```

Use `niri-computer-use resume` to allow actions again after stopping.

The RPM installs the upstream skill in
`/usr/share/niri-computer-use/skills/niri-computer-use`. To expose it to clients
that discover skills in `~/.agents/skills`:

```sh
mkdir -p ~/.agents/skills
ln -s /usr/share/niri-computer-use/skills/niri-computer-use ~/.agents/skills/niri-computer-use
```

The optional Noctalia plugin is in
`/usr/share/niri-computer-use/noctalia/niri-computer-use`. With a compatible
Noctalia version (upstream requires 5.4 or newer, plugin API 36), link and enable
it:

```sh
mkdir -p "${XDG_DATA_HOME:-$HOME/.local/share}/noctalia/plugins"
ln -s /usr/share/niri-computer-use/noctalia/niri-computer-use \
    "${XDG_DATA_HOME:-$HOME/.local/share}/noctalia/plugins/niri-computer-use"
noctalia msg plugins enable ayagmar/niri-computer-use
```

The package leaves MCP registration, skill/plugin activation and niri bindings
to the user. See the [upstream documentation](https://ayagmar.github.io/niri-computer-use/)
for policy configuration and the full client setup instructions.
