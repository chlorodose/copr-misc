outdir ?= $(CURDIR)
spec ?= pam-gnupg.spec
commit := $(shell sed -n 's/^%global commit //p' $(spec))
archive := pam-gnupg-$(commit).tar.gz

.PHONY: srpm deps
srpm: deps $(archive)
	rpmbuild -bs $(spec) --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)"

deps:
	dnf install -y rpm-build curl tar gzip

$(archive): | deps
	curl -fL --retry 3 -o $@.tmp https://github.com/cruegge/pam-gnupg/archive/$(commit)/$(archive)
	mv $@.tmp $@
