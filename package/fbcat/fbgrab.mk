################################################################################
#
# fbgrab
#
################################################################################

FBCAT_VERSION =  99a9aaedf643b800df63b3ac76b0e2071db95372
FBCAT_SITE = git://github.com/jwilk/fbcat
FBCAT_LICENSE = GPL-2.0
FBCAT_LICENSE_FILES = COPYING

define FBCAT_BUILD_CMDS
	$(TARGET_CONFIGURE_OPTS) $(MAKE) -C $(@D)
endef

define FBCAT_INSTALL_TARGET_CMDS
	$(INSTALL) -m 0755 -D $(@D)/fbcat $(TARGET_DIR)/usr/bin/fbcat
endef

$(eval $(generic-package))
