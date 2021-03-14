from NPC import NPC
from Animal import Animal
from Worlds import City
from pygame import display
from pygame import FULLSCREEN
class Groups():
    def __init__(self,north):

        self.north1_block = north
        self.init_commands()
        self.init_NPCs()
        # self.init_commands()

    def init_NPCs(self):
        self.NPC_groupA = []
        self.NPC_groupB = []
        self.NPC_groupC = []
        self.NPC_groupD = []
        self.NPC_groupE = []
        self.NPC_groupF = []
        self.NPC_groupG = []
        self.NPC_groupH = []
        self.NPC_groupI = []
        self.NPC_groupK = []
        self.NPC_groupJ = []
        self.NPC_list = self.NPC_groupA + self.NPC_groupB + self.NPC_groupC + self.NPC_groupD + \
                        self.NPC_groupE + self.NPC_groupF + self.NPC_groupG + self.NPC_groupH + self.NPC_groupI + \
                        self.NPC_groupK + self.NPC_groupJ
    def init_commands(self):
        self.command_hash = {}

    def commands(self):
        self.i = 0
        for NPC in self.NPC_list:
            cmd = self.command_hash.get(str((NPC.x, NPC.y)))
            if cmd != None:
                NPC.move(cmd)

    def move_all(self, x, y):
        for NPC in self.NPC_list:
            NPC.block = NPC.block.move(x, y)
