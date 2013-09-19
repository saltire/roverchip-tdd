from level import Level


class SokobanLevel(Level):
    def check_for_success(self):
        """Return true if all crates are inside Finish cells."""
        return all(crate.get_cell_type() == 'Grate' for crate in self.sprites_by_type('Crate'))
