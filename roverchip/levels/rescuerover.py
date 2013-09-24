from roverchip.level import Level


class RescueRover(Level):
    def check_for_success(self):
        """Return true if the player is in an Exit cell and Rover is following."""
        player = self.sprites['Player'].pop()
        return (player.get_cell_type() == 'Exit' and
                self.sprites['Rover'] <= player.followers)


    def check_for_failure(self):
        """Return true if the player is not active, i.e. dead."""
        return not self.sprites['Player'].pop().is_active
