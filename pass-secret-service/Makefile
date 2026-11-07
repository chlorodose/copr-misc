outdir ?= $(CURDIR)
spec ?= pass-secret-service.spec
version := $(shell sed -n 's/^Version:[[:space:]]*//p' $(spec))
archive := pass-secret-service-$(version).tar.gz
vendor := pass-secret-service-$(version)-vendor.tar.xz

.PHONY: srpm deps
srpm: deps $(archive) $(vendor)
	rpmbuild -bs $(spec) --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)"

deps:
	dnf install -y cargo rust-packaging systemd-rpm-macros rpm-build curl tar gzip xz

$(archive): | deps
	curl -fL --retry 3 -o $@.tmp https://github.com/grimsteel/pass-secret-service/archive/refs/tags/v$(version).tar.gz
	mv $@.tmp $@

$(vendor): $(archive) | deps
	set -eu; \
	workdir=$$(mktemp -d); \
	trap 'rm -rf "$$workdir"' EXIT; \
	tar -xzf $(archive) -C "$$workdir"; \
	cd "$$workdir/pass-secret-service-$(version)"; \
	cargo vendor --locked --versioned-dirs vendor; \
	tar -cJf "$(CURDIR)/$@.tmp" vendor
	mv $@.tmp $@
