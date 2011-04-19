#-*- coding: utf-8 -*-
import os
import gettext

TRANSLATION_DOMAIN = 'rome'
LOCALE_DIR =  os.path.join(os.path.dirname(__file__), 'locale')

_ = gettext.translation(TRANSLATION_DOMAIN, LOCALE_DIR, fallback=True).ugettext
