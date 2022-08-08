from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
loadPrcFile("config_file.prc")


keyMap = {
    "f1" : False,
    "w" : False,
    "up" : False,
    "down" : False,
    "left" : False,
    "right" : False,
    "y" : False,
    "g" : False,
    "h" : False,
    "j" : False
}
def updateKeyMap(key, state):
    keyMap[key] = state



class MainApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # ----------------- Setup Debug Mode -----------------
        self.debugNode = BulletDebugNode('Debug')
        self.debugNode.showWireframe(True)
        self.debugNode.showConstraints(False)
        self.debugNode.showBoundingBoxes(True)
        self.debugNode.showNormals(False)
        self.debugNP = render.attachNewNode(self.debugNode)


        # ---------------- Create Physics World -----------------
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())



        # --------------------Create Models----------------------

        self.ChassisGeomNodes = loader.loadModel("../assets/PorscheChassis.egg").findAllMatches('**/+GeomNode')
        self.ChassisGeomNode = self.ChassisGeomNodes.getPath(0).node()
        self.ChassisGeom = self.ChassisGeomNode.getGeom(0)
        self.ChassisShape = BulletTriangleMesh()
        self.ChassisShape.addGeom(self.ChassisGeom)
        self.ChassisTS = TransformState.makePos(Point3(0, 0, 0))
        self.ChassisTS = self.ChassisTS.setHpr(Point3(-90, 90, 90))
        
        self.ChassisNP = render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.ChassisNP.setPos(0, 0, 1)
        self.ChassisNP.setCollideMask(BitMask32.allOn())
        self.ChassisNP.node().addShape(BulletTriangleMeshShape(self.ChassisShape, dynamic=True), self.ChassisTS)
        self.ChassisNP.node().setCcdMotionThreshold(1e-3)
        self.ChassisNP.node().setCcdSweptSphereRadius(0.10)
        self.ChassisNP.node().setMass(800.0)
        self.ChassisNP.node().setDeactivationEnabled(False)
        self.loader.loadModel('../assets/PorscheChassis.egg').reparentTo(self.ChassisNP)
        self.world.attachRigidBody(self.ChassisNP.node())

        self.Vehicle = BulletVehicle(self.world, self.ChassisNP.node())
        self.Vehicle.setCoordinateSystem(ZUp)
        self.world.attachVehicle(self.Vehicle)


        self.WheelsList = {
            'Wheel1NP' : None,
            'Wheel2NP' : None, 
            'Wheel3NP' : None, 
            'Wheel4NP' : None, 
            'Wheel1' : None, 
            'Wheel2' : None, 
            'Wheel3' : None, 
            'Wheel4' : None
            }

        for i in range(4):
            self.WheelsList[i] = self.loader.loadModel('../assets/PorscheWheel.egg')
            self.WheelsList[i].reparentTo(self.render)
            self.WheelsList[i+4] = self.Vehicle.createWheel()
            self.WheelsList[i+4].setNode(self.WheelsList[i].node())
            if i == 0:
                self.WheelsList[i+4].setChassisConnectionPointCs(Point3(0.75, 1.2, 0.0))
                self.WheelsList[i+4].setFrontWheel(True)
            elif i == 1:
                self.WheelsList[i+4].setChassisConnectionPointCs(Point3(-0.75, 1.2, 0.0))
                self.WheelsList[i+4].setFrontWheel(True)
            elif i == 2:
                self.WheelsList[i+4].setChassisConnectionPointCs(Point3(0.75, -1.15, 0.0))
            else:
                self.WheelsList[i+4].setChassisConnectionPointCs(Point3(-0.75, -1.15, 0.0))
            self.WheelsList[i+4].setWheelDirectionCs(Vec3(0, 0, -1))
            self.WheelsList[i+4].setWheelAxleCs(Vec3(1, 0, 0))
            self.WheelsList[i+4].setWheelRadius(0.5)
            self.WheelsList[i+4].setMaxSuspensionTravelCm(10.0)
            self.WheelsList[i+4].setSuspensionStiffness(40.0)
            self.WheelsList[i+4].setWheelsDampingRelaxation(2.3)
            self.WheelsList[i+4].setWheelsDampingCompression(4.4)
            self.WheelsList[i+4].setFrictionSlip(100.0)
            self.WheelsList[i+4].setRollInfluence(0.1)
        






        self.geomNodes = loader.loadModel("../assets/aterrain.egg").findAllMatches('**/+GeomNode')
        self.geomNode = self.geomNodes.getPath(0).node()
        self.geom = self.geomNode.getGeom(0)
        self.GroundMesh = BulletTriangleMesh()
        self.GroundMesh.addGeom(self.geom)

        self.GroundNP = render.attachNewNode(BulletRigidBodyNode('Ground'))
        self.GroundNP.setPos(0, 0, -1)
        self.GroundNP.setCollideMask(BitMask32.allOn())
        self.GroundNP.setScale(3, 3, 3)
        self.GroundNP.node().addShape(BulletTriangleMeshShape(self.GroundMesh, dynamic=False))
        self.loader.loadModel("../assets/aterrain.egg").reparentTo(self.GroundNP)
        self.world.attachRigidBody(self.GroundNP.node())








        self.geomNodes1 = loader.loadModel("models/smiley.egg").findAllMatches('**/+GeomNode')
        self.geomNode1 = self.geomNodes1.getPath(0).node()
        self.geom1 = self.geomNode1.getGeom(0)
        self.GroundMesh1 = BulletTriangleMesh()
        self.GroundMesh1.addGeom(self.geom1)

        self.SmileyNP = render.attachNewNode(BulletRigidBodyNode('Smiley'))
        self.SmileyNP.setPos(0, 0, 20)
        self.SmileyNP.setCollideMask(BitMask32.allOn())
        self.SmileyNP.setScale(0.1, 0.1, 0.1)
        self.SmileyNP.node().setMass(0.5)
        self.SmileyNP.node().setRestitution(0.0001)
        self.SmileyNP.node().addShape(BulletTriangleMeshShape(self.GroundMesh1, dynamic=True))
        self.SmileyNP.node().setCcdMotionThreshold(1e-3)
        self.SmileyNP.node().setCcdSweptSphereRadius(0.10)
        self.loader.loadModel("models/smiley.egg").reparentTo(self.SmileyNP)
        self.world.attachRigidBody(self.SmileyNP.node())



        # --------------------Initiate Keyboard Event Listener------------------------

        self.accept("f1", updateKeyMap, ["f1", True])
        self.accept("w", updateKeyMap, ["w", True])
        self.accept("arrow_up", updateKeyMap, ["up", True])
        self.accept("arrow_down", updateKeyMap, ["down", True])
        self.accept("arrow_left", updateKeyMap, ["left", True])
        self.accept("arrow_right", updateKeyMap, ["right", True])
        self.accept("y", updateKeyMap, ["y", True])
        self.accept("g", updateKeyMap, ["g", True])
        self.accept("h", updateKeyMap, ["h", True])
        self.accept("j", updateKeyMap, ["j", True])

        self.accept("f1-up", updateKeyMap, ["f1", False])
        self.accept("w-up", updateKeyMap, ["w", False])
        self.accept("arrow_up-up", updateKeyMap, ["up", False])
        self.accept("arrow_down-up", updateKeyMap, ["down", False])
        self.accept("arrow_left-up", updateKeyMap, ["left", False])
        self.accept("arrow_right-up", updateKeyMap, ["right", False])
        self.accept("y-up", updateKeyMap, ["y", False])
        self.accept("g-up", updateKeyMap, ["g", False])
        self.accept("h-up", updateKeyMap, ["h", False])
        self.accept("j-up", updateKeyMap, ["j", False]) 
    
        # ----------------------------Configure Tasks---------------------------------

        self.taskMgr.add(self.update, "update")







    def update(self, task):
        dt = globalClock.getDt()
        self.world.doPhysics(dt)

        # --------------------------Setup Keyboard Tasks------------------------------

        steering = 0.0
        steeringClamp = 45.0
        steeringIncrement = 10000.0
        engineForce = 0.0
        brakeForce = 0.0
        SmileyPos = self.ChassisNP.getPos()
        SmileyVel = self.ChassisNP.node().getLinearVelocity()
        SmileyHPR = self.ChassisNP.getHpr()



        if keyMap["w"]:
            SmileyPos.z = 5
            SmileyPos.x = -6
            SmileyPos.y = -8
            self.ChassisNP.node().setLinearVelocity(LVector3(0, 0, 0))
            self.ChassisNP.node().setAngularVelocity(LVector3(0, 0, 0))
            self.ChassisNP.setPos(SmileyPos)
            self.ChassisNP.setHpr(0, 0, 0)
            self.SmileyNP.node().setLinearVelocity(LVector3(0, 0, 0))
            self.SmileyNP.node().setAngularVelocity(LVector3(0, 0, 0))
            self.SmileyNP.setPos(SmileyPos)
            self.SmileyNP.setHpr(0, 0, 0)

        if keyMap["f1"]:
            if self.debugNP.isHidden():
                self.debugNP.show()
            else:
                self.debugNP.hide()

        if keyMap["up"]:
            engineForce = 2000.0
            brakeForce = 0.0
        
        if keyMap["down"]:
            engineForce = 0.0
            brakeForce = 50.0
        
        if keyMap["left"]:
            steering += dt * steeringIncrement
            steering = min(steering, steeringClamp)
        
        if keyMap["right"]:
            steering -= dt * steeringIncrement
            steering = max(steering, -steeringClamp)
        


        self.Vehicle.setSteeringValue(steering, 0)
        self.Vehicle.setSteeringValue(steering, 1)
        self.Vehicle.applyEngineForce(engineForce, 2)
        self.Vehicle.applyEngineForce(engineForce, 3)
        self.Vehicle.setBrake(brakeForce, 2)
        self.Vehicle.setBrake(brakeForce, 3)




        # -------------------------Create Bouncing Force-------------------------

        result = self.world.contactTestPair(self.SmileyNP.node(), self.GroundNP.node())
        if result.getNumContacts() > 0:
            self.SmileyNP.node().setLinearVelocity(LVector3(SmileyVel.getX(), SmileyVel.getY(), 10))



        return task.cont



            

app = MainApp()
app.run()