from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

import os, sys

# vars
path = "test/"

# Read or Write files (https://docs.python.org/2/library/os.html)
dirs = os.listdir(path)

def enhancer():
  # import files from folder
  for image in dirs:
    if os.path.isfile(path+image):
      source = Image.open(path+image)
      f, e = os.path.splitext(path+image)

      #
      # Two image source inputs filter separately with DETAIL and
      # FIND_EDGES filters.
      #
      # http://pillow.readthedocs.io/en/3.4.x/reference/ImageFilter.html
      #
      filter1 = source.filter(ImageFilter.DETAIL)
      filter2 = source.filter(ImageFilter.FIND_EDGES)

      #
      # One image with DETAIL filtered and the second image with FIND_EDGES
      # filtered. Two filtered image blends together with alpha 0.1 overlays.
      # http://pillow.readthedocs.io/en/3.4.x/reference/Image.html?highlight=blend#PIL.Image.blend
      #
      compose = Image.blend(filter1, filter2, alpha=.1)

      #
      # Taking from the first image blend (compose) and blend it again with the
      # SMOOTH filter as a new image source input. Alpha is 0.1 overlays.
      #
      filter3 = source.filter(ImageFilter.SMOOTH)
      blend = Image.blend(compose, filter3, alpha=.1)

      #
      # The final blending (blend) is move to enhancing stage.
      # This stage is to enhance the image COLOR with value 1.5 (0.0).
      # IMAGE > enhanced > COLOR
      #
      # http://pillow.readthedocs.io/en/3.4.x/reference/ImageEnhance.html?highlight=ImageEnhance#PIL.ImageEnhance.Color
      #
      imageColor = ImageEnhance.Color(blend)
      renderStage1 = imageColor.enhance(1.5)

      #
      # This stage is to enhance the image CONTRAST with value 1.1 (0.0).
      # IMAGE(color) > enhanced > CONTRAST
      #
      # http://pillow.readthedocs.io/en/3.4.x/reference/ImageEnhance.html?highlight=ImageEnhance#PIL.ImageEnhance.Contrast
      #
      imageContrast = ImageEnhance.Contrast(renderStage1)
      renderStage2 = imageContrast.enhance(1.1)

      #
      # This stage is to enhance the image CONTRAST with value 1.1 (0.0).
      # IMAGE(contrast) > enhanced > BRIGHTNESS
      #
      # http://pillow.readthedocs.io/en/3.4.x/reference/ImageEnhance.html?highlight=ImageEnhance#PIL.ImageEnhance.Brightness
      #
      imageBrightness = ImageEnhance.Brightness(renderStage2)
      renderFinal = imageBrightness.enhance(1.1)

      #
      # Final, write to a new image file
      # File Format is JPEG with Quality 100
      renderFinal.save(f + '_enhanced.jpg', 'JPEG', quality=100)

enhancer()