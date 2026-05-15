.PHONY: srpm
srpm: zfs.spec
	dnf install -y rpkg
	rpkg srpm --outdir . --spec zfs.spec
	[ "$(outdir)" -ef . ] || cp *.src.rpm "$(outdir)"

version := 2.4.2
zfs.spec: zfs.tar.gz
	dnf install -y tar gzip
	tar -xavf zfs.tar.gz --strip-components=3 zfs-$(version)/rpm/generic/zfs.spec.in
	cat zfs.spec.in | \
	    sed -e 's/@RELEASE@/1/g' -e 's/@VERSION@/$(version)/g' -e 's/@PACKAGE@/zfs/g' -e 's/@ZFS_META_LICENSE@/CDCL/g' | \
		grep -v kmod \
		>zfs.spec
	rm zfs.spec.in


zfs.tar.gz:
	dnf install -y wget
	wget https://github.com/openzfs/zfs/releases/download/zfs-$(version)/zfs-$(version).tar.gz
	ln -s zfs-$(version).tar.gz zfs.tar.gz
