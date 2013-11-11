from roverchip.level import Level


class ChipsChallenge(Level):
    def __init__(self, levelfile):
        Level.__init__(self, levelfile)

        # set the # of chips required to pass, defaulting to # of chips in level
        self.chipquota = levelfile.properties.get('chipquota', len(self.sprites['Chip']))


    def check_for_success(self):
        """Return true if a player is in an exit cell and carrying enough
        chips to meet the level quota."""
        return any((player.get_cell_type() == 'Exit' and
                    len(player.carrying['Chip']) >= self.chipquota)
                   for player in self.sprites['Player'])


    def check_for_failure(self):
        """Return true if no players are alive in the level."""
        return not self.sprites['Player']
