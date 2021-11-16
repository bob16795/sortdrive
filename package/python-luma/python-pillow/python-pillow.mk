################################################################################
#
# python-pillow
#
################################################################################

PYTHON_PILLOW_VERSION = 7.1.2
PYTHON_PILLOW_SOURCE = Pillow-$(PYTHON_PILLOW_VERSION).tar.gz
PYTHON_PILLOW_SITE = https://files.pythonhosted.org/packages/ce/ef/e793f6ffe245c960c42492d0bb50f8d14e2ba223f1922a5c3c81569cec44
PYTHON_PILLOW_SETUP_TYPE = setuptools
PYTHON_PILLOW_LICENSE = Historical Permission Notice and Disclaimer (HPND)
PYTHON_PILLOW_LICENSE_FILES = LICENSE docs/COPYING Tests/icc/LICENSE.txt Tests/fonts/LICENSE.txt

$(eval $(python-package))
