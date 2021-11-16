################################################################################
#
# python-lumacore
#
################################################################################

PYTHON_LUMACORE_VERSION = 1.14.0
PYTHON_LUMACORE_SOURCE = luma.core-$(PYTHON_LUMACORE_VERSION).tar.gz
PYTHON_LUMACORE_SITE = https://files.pythonhosted.org/packages/65/ee/a388b6ad84d8d24d8583ca1ad5f89864789e205fbfbc5c6fb716b8573291
PYTHON_LUMACORE_SETUP_TYPE = setuptools
PYTHON_LUMACORE_LICENSE = MIT
PYTHON_LUMACORE_LICENSE_FILES = LICENSE.rst

$(eval $(python-package))
