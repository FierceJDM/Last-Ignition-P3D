from direct.showbase.ShowBase import ShowBase
import panda3d
from panda3d.core import *
from panda3d.bullet import *

keyMap = {
    "f1" : False,
    "w" : False,
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
        self.debugNode = BulletDebugNode('Debug')
        self.debugNode.showWireframe(True)
        self.debugNode.showConstraints(False)
        self.debugNode.showBoundingBoxes(True)
        self.debugNode.showNormals(False)
        self.debugNP = render.attachNewNode(self.debugNode)


        # Setup physics world
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())



        # Create the ground
        self.geomNodes = loader.loadModel("aterrain.egg").findAllMatches('**/+GeomNode')
        self.geomNode = self.geomNodes.getPath(0).node()
        self.geom = self.geomNode.getGeom(0)
        
        self.GroundMesh = BulletTriangleMesh()
        self.GroundMesh.addGeom(self.geom)
        self.GroundShape = BulletTriangleMeshShape(self.GroundMesh, dynamic=False)
        self.GroundNode = BulletRigidBodyNode('Ground')
        self.GroundNode.addShape(self.GroundShape)
        self.GroundNP = render.attachNewNode(self.GroundNode)
        self.GroundNP.setPos(0, 0, -1)
        self.world.attachRigidBody(self.GroundNode)
        self.GroundModel = self.loader.loadModel("aterrain.egg")
        self.GroundModel.reparentTo(self.GroundNP)

        # Create a smiley face
        self.SmileyModel = self.loader.loadModel("models/smiley.egg")
        self.SmileyShape = BulletSphereShape(1)
        self.SmileyNode = BulletRigidBodyNode('Smiley')
        self.SmileyNode.setMass(1.0)
        self.SmileyNode.addShape(self.SmileyShape)
        self.SmileyNP = render.attachNewNode(self.SmileyNode)
        self.SmileyNP.setPos(0, 0, 9)
        self.SmileyNP.setScale(0.1, 0.1, 0.1)
        self.world.attachRigidBody(self.SmileyNode)
        self.SmileyModel.reparentTo(self.SmileyNP)

        # Initiate keyboard event listener
        self.accept("f1", updateKeyMap, ["f1", True])
        self.accept("f1-up", updateKeyMap, ["f1", False])
        self.accept("w", updateKeyMap, ["w", True])
        self.accept("w-up", updateKeyMap, ["w", False])
        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])
        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])
        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])
    
        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)

        # Update smiley face's position
        SmileyPos = self.SmileyNP.getPos()
        SmileyVel = self.SmileyNode.getLinearVelocity()
        if keyMap["w"]:
            SmileyPos.z = 1
            SmileyPos.x = 0
            SmileyPos.y = 0
            self.SmileyNode.setLinearVelocity(LVector3(0, 0, 0))
            self.SmileyNode.setAngularVelocity(LVector3(0, 0, 0))
            self.SmileyNP.setPos(SmileyPos)
        if keyMap["left"]:
            self.SmileyNode.setLinearVelocity(LVector3(SmileyVel.getX()-0.1, SmileyVel.getY(), SmileyVel.getZ()))
        if keyMap["right"]:
            self.SmileyNode.setLinearVelocity(LVector3(SmileyVel.getX()+0.1, SmileyVel.getY(), SmileyVel.getZ()))
        if keyMap["up"]:
            self.SmileyNode.setLinearVelocity(LVector3(SmileyVel.getX(), SmileyVel.getY()+0.1, SmileyVel.getZ()))
        if keyMap["down"]:
            self.SmileyNode.setLinearVelocity(LVector3(SmileyVel.getX(), SmileyVel.getY()-0.1, SmileyVel.getZ()))

        if keyMap["f1"]:
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()


        return task.cont



            

app = MyApp()
app.run()