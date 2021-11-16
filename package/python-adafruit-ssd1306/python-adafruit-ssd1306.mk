################################################################################
#
# python-adafruit-ssd1306
#
################################################################################

PYTHON_ADAFRUIT_SSD1306_VERSION = 1.6.2
PYTHON_ADAFRUIT_SSD1306_SOURCE = Adafruit_SSD1306-$(PYTHON_ADAFRUIT_SSD1306_VERSION).tar.gz
PYTHON_ADAFRUIT_SSD1306_SITE = http://files.pythonhosted.org/packages/fc/de/0a176512f6fab96eb3e6adde2b267bab843b3b541d8b83a3783d79c6ff43
PYTHON_ADAFRUIT_SSD1306_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_SSD1306_LICENSE = MIT

$(eval $(python-package))
