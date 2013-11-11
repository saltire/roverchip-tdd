from roverchip.level import Level


class RescueRover(Level):
    def check_for_success(self):
        """Return true if the player is in an Exit cell and all Rovers are following."""
        return any((player.get_cell_type() == 'Exit' and
                    self.sprites['Rover'] <= player.followers)
                   for player in self.sprites['Player'])


    def check_for_failure(self):
        """Return true if no players are alive in the level."""
        return not self.sprites['Player']
