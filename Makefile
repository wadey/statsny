PKG = statsny
BUILD_NUMBER ?= 0000INVALID

.PHONY: $(PKG)/_version.py

version: $(PKG)/_version.py

$(PKG)/_version.py: $(PKG)/_version.py.m4
	m4 -D__BUILD__=$(BUILD_NUMBER) $^ > $@
