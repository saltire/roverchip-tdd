from roverchip.level import Level


class ChipsChallenge(Level):
    def __init__(self, levelfile):
        Level.__init__(self, levelfile)

        # set the # of chips required to pass, defaulting to # of chips in level
        self.chipquota = levelfile.properties.get('chipquota', len(self.sprites['Chip']))


    def check_for_success(self):
        """Return true if player is in an exit cell and carrying enough
        chips to meet the level quota."""
        player = self.sprites['Player'].pop()
        return (player.get_cell_type() == 'Exit' and
                len(player.carrying['Chip']) >= self.chipquota)


    def check_for_failure(self):
        """Return true if the player is not active, i.e. dead."""
        return not self.sprites['Player'].pop().is_active
