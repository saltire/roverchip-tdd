from level import Level


class RoverLevel(Level):
    def check_for_success(self):
        """Return true if the player is in an Exit cell and Rover is following."""
        player = self.sprites['Player'].pop()
        return (player.get_cell_type() == 'Exit' and
                self.sprites['Rover'] <= player.followers)
