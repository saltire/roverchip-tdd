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


    def render(self, text, charheight=None, tracking=0, leading=0, color=None):
        """Return a surface containing a graphical rendering of the text.
        If lineheight is passed, scale the characters (including leading) to that height.
        Color will replace all colours, keeping alpha unchanged.
        Takes a string or a list of strings (formatting the characters once)."""
        chars = self._format_chars(text if isinstance(text, basestring) else ''.join(text),
                                   charheight, color)

        if isinstance(text, basestring):
            # render a string
            return self._render_text(text, chars, charheight, tracking, leading)

        else:
            # format all characters at once and render multiple strings
            return [self._render_text(t, chars, charheight, tracking, leading) for t in text]


    def _format_chars(self, text, charheight, color):
        """Return the glyphs for each unique character in a string."""
        chars = {char: self.chars[char] for char in set(text.replace('\n', ''))}

        for char, charimg in chars.iteritems():
            if color is not None:
                # replace RGB channels with those from color
                pix = pygame.surfarray.pixels3d(charimg)
                pix[:, :, 0], pix[:, :, 1], pix[:, :, 2] = color
                del(pix)

            if charheight is not None:
                # scale character to the given height
                charwidth = int(chars[char].get_width() * float(charheight) / self.height)
                chars[char] = pygame.transform.scale(chars[char], (charwidth, int(charheight)))

        return chars


    def _render_text(self, text, chars, charheight, tracking, leading):
        """Render a block of text using the given glyphs."""
        text = text.split('\n')
        width = max(sum(chars[char].get_width() + tracking for char in line) - tracking
                    for line in text)
        lineheight = (charheight if charheight is not None else self.height) + leading
        height = len(text) * lineheight
        canvas = pygame.Surface((width, height), pygame.SRCALPHA)

        for y, line in enumerate(text):
            x = 0
            for char in line:
                canvas.blit(chars[char], (x, y * lineheight))
                x += chars[char].get_width() + tracking

        return canvas



