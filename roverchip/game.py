from levels import leveltypes


class Game:
    def __init__(self, eventhandler, renderer, leveldata):
        self.eventhandler = eventhandler
        self.renderer = renderer
        self.level = leveltypes[leveldata.leveltype](*leveldata.get_data())
    
    
    def run_frame(self, elapsed, events):
        """Run one frame of the level, and return None unless the level is
        either won or lost, in which case return True or False respectively."""
        for event in events:
            etype, args = event[0], event[1:]
            self.level.handle_event(etype, args)
            
        self.level.update_level(elapsed)
        
        if self.level.check_for_failure():
            return False
        if self.level.check_for_success():
            return True
    
    
    
    