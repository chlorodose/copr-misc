.PHONY: srpm
srpm: regreet.spec
	dnf install -y rpkg
	rpkg srpm --outdir . --spec regreet.spec
	[ "$(outdir)" -ef . ] || cp *.src.rpm "$(outdir)"

regreet.spec: regreet.crate regreet.license
	dnf install -y rust2rpm
	git config user.name || git config --global user.name placeholder
	git config user.email || git config --global user.email placeholder@nomail.com
	rust2rpm --path $$(realpath regreet.crate) --vendor auto regreet
	rm -f regreet.spec
	sed -i '1i %global debug_package %{nil}'                    rust-regreet.spec
	sed -i '/^License/s/# FIXME/INSERT_ME_WITH_LICENSE/g'       rust-regreet.spec
	sed -i "s/INSERT_ME_WITH_LICENSE/$$(cat regreet.license)/g" rust-regreet.spec
	mv rust-regreet.spec regreet.spec

regreet.crate: ReGreet regreet.license
	dnf install -y cargo
	cd ReGreet && cargo package --no-verify
	rm -f regreet.crate
	cp ReGreet/target/package/regreet-*.crate .
	ln -s regreet-*.crate regreet.crate

ReGreet:
	dnf install -y git
	rm -rf ReGreet
	git clone https://github.com/rharish101/ReGreet.git -b 0.3.0 --depth 1

regreet.license: ReGreet
	dnf install -y cargo cargo2rpm
	cd ReGreet && cargo vendor
	mkdir -p ReGreet/.cargo && cat vendor.config.toml >>ReGreet/.cargo/config.toml
	cd ReGreet && cargo2rpm license-summary | grep '^# .*' | cut -b3- | awk '{ print "AND ( " $$0 " )" }' | tr '\n' ' ' | cut -b5- >../regreet.license
	cd ReGreet && git restore . && git clean -xdf
