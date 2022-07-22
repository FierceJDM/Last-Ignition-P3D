from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.physics import *

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
        #self.disableMouse()
        self.enableParticles()

        self.node = NodePath("PhysicsNode")
        self.node.reparentTo(self.render)
        self.an = ActorNode("jetpack-guy-physics")
        self.an.getPhysicsObject().setMass(100)
        self.anp = self.node.attachNewNode(self.an)
        self.physicsMgr.attachPhysicalNode(self.an)


        self.pandaActor = loader.loadModel("models/panda-model")
        self.pandaActor.reparentTo(self.anp)
        self.pandaActor.setScale(0.0005, 0.0005, 0.0005)
        self.pandaActor.reparentTo(self.render)
        
        self.gravityFN = ForceNode('world-forces')
        self.gravityFNP = self.render.attachNewNode(self.gravityFN)
        self.gravityForce = LinearVectorForce(0,0,-9.81) #gravity acceleration
        self.gravityFN.addForce(self.gravityForce)
        self.an.getPhysical(0).addLinearForce(self.gravityForce)


        self.scene = self.loader.loadModel("aterrain.egg")
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(0, 0, 0)
        self.scene.reparentTo(self.render)

        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])
    
        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        pandaPos = self.pandaActor.getPos()
        if keyMap["up"]:
            pandaPos.z += 10 * dt
        self.pandaActor.setPos(pandaPos)
        
        return task.cont



            

app = MyApp()
app.run()