from base64 import b64encode

from .core import BaseString


class MainLanguageSongString(BaseString):

    DEFAULT_FONT = 'HelveticaNeueLTStd-BlkEx'

    # Specific RTF properties
    formatted_text = ('\\f0\\b\\fs160 \\cf1 \\outl0\\strokewidth-80 '
                      '\\strokec2 \\uc0\\u8232 '
                      '{text}')

    def __init__(self, attributes={}, text=None):
        super(MainLanguageSongString, self).__init__(attributes)

        if text:
            self.add_text(text)

    def prepare_rtf(self, text):
        base = self.base_rtf()

        text = '\\\n'.join(text)

        return base.format(text=text)

    def add_text(self, text):
        text = [self.rtf_encode(line) for line in text]

        text = self.prepare_rtf(text)
        text = b64encode(text.encode('utf-8'))
        self.add_text_to_root(text)


class SecondaryLanguageSongString(MainLanguageSongString):

    # Specific RTF properties
    formatted_text = ('\\f0\\b\\fs130 \\cf1 \\outl0\\strokewidth-80 '
                      '\\strokec2 \\uc0\\u8232 '
                      '{text}')
