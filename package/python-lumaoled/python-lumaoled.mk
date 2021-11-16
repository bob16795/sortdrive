################################################################################
#
# python-lumaoled
#
################################################################################

PYTHON_LUMAOLED_VERSION = 3.4.0
PYTHON_LUMAOLED_SOURCE = luma.oled-$(PYTHON_LUMAOLED_VERSION).tar.gz
PYTHON_LUMAOLED_SITE = https://files.pythonhosted.org/packages/a3/44/a5d370d3d1a117db2e99334e5b05bd4a11ae99e32036006134ec22c6bd2c
PYTHON_LUMAOLED_SETUP_TYPE = setuptools
PYTHON_LUMAOLED_LICENSE = MIT
PYTHON_LUMAOLED_LICENSE_FILES = LICENSE.rst

$(eval $(python-package))
