import pygame


class Font:
    def __init__(self, spritepath, charsize, mono=False, spacewidth=None):
        """Given a sprite that is a grid of characters, and the dimensions
        of each character, slice it into a dict of surfaces mapped to each
        character in ASCII sequence, starting at 0."""
        self.sprite = pygame.image.load(spritepath)
        cw, ch = charsize
        sw, sh = self.sprite.get_width() / cw, self.sprite.get_height() / ch
        spacewidth = spacewidth if spacewidth is not None else cw * .4

        self.height = ch

        self.chars = {}
        for y in range(sh):
            for x in range(sw):
                char = chr(x + y * sw)
                charimg = self.sprite.subsurface((x * cw, y * ch, cw, ch))

                # crop characters to their actual width, unless monospaced
                if not mono:
                    cwidth = (charimg.get_bounding_rect()[2]
                              if char != ' ' else spacewidth)
                    charimg = charimg.subsurface((0, 0, cwidth, ch))

                self.chars[char] = charimg


    def render(self, text, charheight=None, lineheight=None, tracking=0, color=None):
        """Return a surface containing a graphical rendering of the text.
        If charheight is passed, scale the characters to that height.
        Lineheight affects the vertical spacing of multiline strings.
        Tracking is relative to base font size before scaling.
        Color will replace all colours, keeping alpha unchanged.
        Takes a string or a list of strings (formatting the characters once)."""
        chars = self._format_chars(text if isinstance(text, basestring) else ''.join(text),
                                   charheight, tracking, color)

        if isinstance(text, basestring):
            # render a string
            return self._render_text(text, chars, charheight, lineheight)

        else:
            # format all characters at once and render multiple strings
            return [self._render_text(t, chars, charheight, lineheight) for t in text]


    def _format_chars(self, text, charheight, tracking, color):
        """Return the glyphs for each unique character in a string."""
        chars = {char: self.chars[char] for char in set(text.replace('\n', ''))}

        for char, charimg in chars.iteritems():
            if color is not None:
                # replace RGB channels with those from color
                pix = pygame.surfarray.pixels3d(charimg)
                pix[:, :, 0], pix[:, :, 1], pix[:, :, 2] = color
                del(pix)

            if tracking > 0:
                # replace the character surface with a larger one
                chars[char] = pygame.Surface((charimg.get_width() + tracking, charimg.get_height()),
                                             pygame.SRCALPHA)
                chars[char].blit(charimg, (0, 0))

            if charheight is not None:
                # scale character to the given height
                charwidth = int(chars[char].get_width() * float(charheight) / self.height)
                chars[char] = pygame.transform.scale(chars[char], (charwidth, int(charheight)))

        return chars


    def _render_text(self, text, chars, charheight, lineheight):
        """Render a block of text using the given glyphs."""
        text = text.split('\n')
        width = max(sum(chars[char].get_width() for char in line) for line in text)
        lineheight = (lineheight if lineheight is not None else
                      charheight if charheight is not None else self.height)
        height = len(text) * lineheight
        canvas = pygame.Surface((width, height), pygame.SRCALPHA)

        for y, line in enumerate(text):
            x = 0
            for char in line:
                canvas.blit(chars[char], (x, y * lineheight))
                x += chars[char].get_width()

        return canvas



