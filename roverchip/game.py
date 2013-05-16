from leveldata import LevelData
from levels import leveltypes


class Game:
    def __init__(self, *datafiles):
        self.leveldata = (LevelData(dfile) for dfile in datafiles)
    
    
    def run(self):
        """Instantiate each level in turn and run it in a loop."""
        for ldata in self.leveldata:
            level = leveltypes[ldata.leveltype](ldata.celldata, ldata.spritedata)
            
            result = None
            while result is None:
                events = []
                result = self.run_frame(level, events)
            
        
    def run_frame(self, level, events):
        """Run one frame of the level, and return None unless the level is
        either won or lost, in which case return True or False respectively."""
        if level.check_for_failure():
            return False
        if level.check_for_success():
            return True
    
    
    
    