%global debug_package %{nil}

Name:           maple-mono-font
Version:        7.9
Release:        %autorelease
Summary:        Maple Mono: Open source monospace font with round corner, ligatures and Nerd-Font icons for IDE and terminal, fine-grained customization options.
BuildArch:      noarch
License:        OFL-1.1
URL:            https://github.com/subframe7536/maple-font
Source0:        %{url}/releases/download/v%{version}/MapleMono-NF-CN-unhinted.zip

Requires(post):   fontconfig
Requires(postun): fontconfig

%description
%{summary}

%prep
%autosetup -c

%build
# Nothing to build.

%install
mkdir -p %{buildroot}/usr/share/fonts/maple-mono
install -m 644 -p *.ttf %{buildroot}/usr/share/fonts/maple-mono

%post
fc-cache -f -v || true

%postun
if [ $1 -eq 0 ] ; then
    fc-cache -f -v || true
fi

%files
%defattr(644, root, root, 755)
/usr/share/fonts/maple-mono
%license LICENSE.txt

%changelog
%autochangelog
