import ctypes,win32con
from materialyoucolor.utils.theme_utils import themeFromSourceColor, getDefaultTheme, getDominantColors, customColor
from materialyoucolor.utils.string_utils import argbFromRgb, hexFromArgb
import darkdetect
class ThemeBuilder():
    dark_default = {'primary': [182, 196, 255], 'primaryContainer': [41, 64, 147], 'onPrimary': [10, 39, 123],
            'onPrimaryContainer': [220, 225, 255], 'inversePrimary': [67, 89, 172], 'secondary': [194, 197, 221],
            'secondaryContainer': [66, 70, 89], 'onSecondary': [44, 47, 66], 'onSecondaryContainer': [222, 225, 249],
            'tertiary': [228, 186, 217], 'tertiaryContainer': [92, 60, 86], 'onTertiary': [67, 39, 63],
            'onTertiaryContainer': [255, 214, 246], 'surface': [18, 19, 24], 'surfaceDim': [18, 19, 24],
            'surfaceBright': [56, 57, 63], 'surfaceContainerLowest': [13, 14, 19], 'surfaceContainerLow': [26, 27, 33],
            'surfaceContainer': [31, 31, 37], 'surfaceContainerHigh': [41, 42, 48],
            'surfaceContainerHighest': [52, 52, 58], 'surfaceVariant': [69, 70, 79], 'onSurface': [227, 225, 233],
            'onSurfaceVariant': [198, 197, 207], 'inverseSurface': [227, 225, 233], 'inverseOnSurface': [47, 48, 54],
            'background': [18, 19, 24], 'onBackground': [227, 225, 233], 'error': [255, 180, 169],
            'errorContainer': [147, 0, 6], 'onError': [104, 0, 3], 'onErrorContainer': [255, 218, 212],
            'outline': [144, 144, 153], 'outlineVariant': [69, 70, 79], 'shadow': [0, 0, 0],
            'surfaceTint': [182, 196, 255], 'scrim': [0, 0, 0]}
    light_default = {'primary': [67, 89, 172], 'primaryContainer': [220, 225, 255], 'onPrimary': [255, 255, 255],
             'onPrimaryContainer': [0, 19, 86], 'inversePrimary': [182, 196, 255], 'secondary': [90, 93, 113],
             'secondaryContainer': [222, 225, 249], 'onSecondary': [255, 255, 255],
             'onSecondaryContainer': [23, 27, 44], 'tertiary': [118, 84, 111], 'tertiaryContainer': [255, 214, 246],
             'onTertiary': [255, 255, 255], 'onTertiaryContainer': [44, 18, 41], 'surface': [250, 248, 255],
             'surfaceDim': [219, 217, 224], 'surfaceBright': [250, 248, 255], 'surfaceContainerLowest': [255, 255, 255],
             'surfaceContainerLow': [245, 243, 251], 'surfaceContainer': [239, 237, 244],
             'surfaceContainerHigh': [233, 231, 238], 'surfaceContainerHighest': [227, 225, 233],
             'surfaceVariant': [226, 225, 236], 'onSurface': [26, 27, 33], 'onSurfaceVariant': [69, 70, 79],
             'inverseSurface': [47, 48, 54], 'inverseOnSurface': [242, 240, 248], 'background': [250, 248, 255],
             'onBackground': [26, 27, 33], 'error': [186, 27, 27], 'errorContainer': [255, 218, 212],
             'onError': [255, 255, 255], 'onErrorContainer': [65, 0, 1], 'outline': [118, 118, 127],
             'outlineVariant': [198, 197, 207], 'shadow': [0, 0, 0], 'surfaceTint': [67, 89, 172], 'scrim': [0, 0, 0]}
    current_theme = [light_default, dark_default]

    def __init__(self):
        self.source_image = self.getWallpaper()
        self.current_theme = self.generateMaterialYou(self.source_image)

    def getWallpaper(self):
        ubuf = ctypes.create_unicode_buffer(512)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_GETDESKWALLPAPER,len(ubuf),ubuf,0)
        return ubuf.value
    def generateMaterialYou(self, image):
        try:
            argbs = getDominantColors(image, quality=10, default_chunk=128)

            argb = argbs[0]
            color = themeFromSourceColor(argb)
            dark = color['schemes']['dark'].props
            light = color['schemes']['light'].props
            return [light, dark]
        except Exception as e:
            print(e)
            print("Using default theme")
            dark = {'primary': [182, 196, 255], 'primaryContainer': [41, 64, 147], 'onPrimary': [10, 39, 123], 'onPrimaryContainer': [220, 225, 255], 'inversePrimary': [67, 89, 172], 'secondary': [194, 197, 221], 'secondaryContainer': [66, 70, 89], 'onSecondary': [44, 47, 66], 'onSecondaryContainer': [222, 225, 249], 'tertiary': [228, 186, 217], 'tertiaryContainer': [92, 60, 86], 'onTertiary': [67, 39, 63], 'onTertiaryContainer': [255, 214, 246], 'surface': [18, 19, 24], 'surfaceDim': [18, 19, 24], 'surfaceBright': [56, 57, 63], 'surfaceContainerLowest': [13, 14, 19], 'surfaceContainerLow': [26, 27, 33], 'surfaceContainer': [31, 31, 37], 'surfaceContainerHigh': [41, 42, 48], 'surfaceContainerHighest': [52, 52, 58], 'surfaceVariant': [69, 70, 79], 'onSurface': [227, 225, 233], 'onSurfaceVariant': [198, 197, 207], 'inverseSurface': [227, 225, 233], 'inverseOnSurface': [47, 48, 54], 'background': [18, 19, 24], 'onBackground': [227, 225, 233], 'error': [255, 180, 169], 'errorContainer': [147, 0, 6], 'onError': [104, 0, 3], 'onErrorContainer': [255, 218, 212], 'outline': [144, 144, 153], 'outlineVariant': [69, 70, 79], 'shadow': [0, 0, 0], 'surfaceTint': [182, 196, 255], 'scrim': [0, 0, 0]}
            light = {'primary': [67, 89, 172], 'primaryContainer': [220, 225, 255], 'onPrimary': [255, 255, 255], 'onPrimaryContainer': [0, 19, 86], 'inversePrimary': [182, 196, 255], 'secondary': [90, 93, 113], 'secondaryContainer': [222, 225, 249], 'onSecondary': [255, 255, 255], 'onSecondaryContainer': [23, 27, 44], 'tertiary': [118, 84, 111], 'tertiaryContainer': [255, 214, 246], 'onTertiary': [255, 255, 255], 'onTertiaryContainer': [44, 18, 41], 'surface': [250, 248, 255], 'surfaceDim': [219, 217, 224], 'surfaceBright': [250, 248, 255], 'surfaceContainerLowest': [255, 255, 255], 'surfaceContainerLow': [245, 243, 251], 'surfaceContainer': [239, 237, 244], 'surfaceContainerHigh': [233, 231, 238], 'surfaceContainerHighest': [227, 225, 233], 'surfaceVariant': [226, 225, 236], 'onSurface': [26, 27, 33], 'onSurfaceVariant': [69, 70, 79], 'inverseSurface': [47, 48, 54], 'inverseOnSurface': [242, 240, 248], 'background': [250, 248, 255], 'onBackground': [26, 27, 33], 'error': [186, 27, 27], 'errorContainer': [255, 218, 212], 'onError': [255, 255, 255], 'onErrorContainer': [65, 0, 1], 'outline': [118, 118, 127], 'outlineVariant': [198, 197, 207], 'shadow': [0, 0, 0], 'surfaceTint': [67, 89, 172], 'scrim': [0, 0, 0]}
            return [light, dark]

    def get_theme_style(self):
        if darkdetect.isDark():
            return "Dark"
        else:
            return "Light"
    def get_theme(self):
        if darkdetect.isDark():
            return self.current_theme[1]
        else:
            return self.current_theme[0]

    def rgb2hex(self, hex):
        return "#{:02x}{:02x}{:02x}".format(hex[0], hex[1], hex[2])
    def get_color(self, name):
        return self.rgb2hex(self.get_theme()[name])