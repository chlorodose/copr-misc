.PHONY: srpm
srpm: kanidm-fedora
	dnf install -y rpkg
	rpkg srpm --outdir kanidm-fedora --spec kanidm-fedora/kanidm.spec
	cp kanidm-fedora/*.src.rpm "$(outdir)"

kanidm-fedora:
	dnf install -y git rpmdevtools
	git clone https://github.com/jcrawfordor/kanidm-fedora.git --depth 1
	sed -i '1i %global debug_package %{nil}' kanidm-fedora/kanidm.spec
	cd kanidm-fedora && spectool -g kanidm.spec
