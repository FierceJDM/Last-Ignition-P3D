from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *


keyMap = {
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False
}
def updateKeyMap(key, state):
    keyMap[key] = state




class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Setup physics world
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Create the ground
        self.GroundShape = BulletPlaneShape(Vec3(0, 0, 1), 1)
        self.GroundNode = BulletRigidBodyNode('Ground')
        self.GroundNode.addShape(self.GroundShape)
        self.GroundNP = render.attachNewNode(self.GroundNode)
        self.GroundNP.setPos(0, 0, -1)
        self.world.attachRigidBody(self.GroundNode)
        self.GroundModel = self.loader.loadModel("aterrain.egg")
        self.GroundModel.reparentTo(self.GroundNP)

        # Create a smiley face
        self.SmileyShape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.SmileyNode = BulletRigidBodyNode('Smiley')
        self.SmileyNode.setMass(1.0)
        self.SmileyNode.addShape(self.SmileyShape)
        self.SmileyNP = render.attachNewNode(self.SmileyNode)
        self.SmileyNP.setPos(-0.002, 0, 2)
        self.world.attachRigidBody(self.SmileyNode)
        self.SmileyModel = self.loader.loadModel("models/smiley.egg")
        self.SmileyModel.setScale(0.5, 0.5, 0.5)
        self.SmileyModel.reparentTo(self.SmileyNP)

        # Initiate keyboard event listener
        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])
    
        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()

        self.world.doPhysics(dt)

        # Update smiley face's position
        SmileyPos = self.SmileyNP.getPos()
        if keyMap["up"]:
            SmileyPos.z += 1
        self.SmileyNP.setPos(SmileyPos)

        return task.cont



            

app = MyApp()
app.run()