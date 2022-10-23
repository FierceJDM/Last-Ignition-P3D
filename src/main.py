from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
from headers.Controls import *
from math import *



loadPrcFile("config_file.prc")


class MainApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #self.disableMouse()
        self.Steering = 0.0
        self.CamOffset = 0
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

        # TODO : reduce tris count by creating a (very) low-poly collision object of the car in Blender
        self.ChassisGeomNodes = self.loader.loadModel("../assets/untitled.bam").findAllMatches('**/+GeomNode')
        self.ChassisGeomNode = self.ChassisGeomNodes.getPath(0).node()
        self.ChassisGeom = self.ChassisGeomNode.getGeom(0)
        self.ChassisShape = BulletTriangleMesh()
        self.ChassisShape.addGeom(self.ChassisGeom)
        self.ChassisTS = TransformState.makePos(Point3(0, 0, 0))
        self.ChassisTS = self.ChassisTS.setHpr(Point3(0, 0, 0))
        
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
            self.WheelsList[i+4].setWheelRadius(0.3305)
            self.WheelsList[i+4].setMaxSuspensionTravelCm(10.0)
            self.WheelsList[i+4].setSuspensionStiffness(40.0)
            self.WheelsList[i+4].setWheelsDampingRelaxation(2.3)
            self.WheelsList[i+4].setWheelsDampingCompression(4.4)
            self.WheelsList[i+4].setFrictionSlip(100.0)
            self.WheelsList[i+4].setRollInfluence(0.1)
        






        self.geomNodes = self.loader.loadModel("../assets/circuit.egg").findAllMatches('**/+GeomNode')
        self.geomNode = self.geomNodes.getPath(0).node()
        self.geom = self.geomNode.getGeom(0)
        self.GroundMesh = BulletTriangleMesh()
        self.GroundMesh.addGeom(self.geom)

        self.GroundNP = render.attachNewNode(BulletRigidBodyNode('Ground'))
        self.GroundNP.setPos(0, 0, -1)
        self.GroundNP.setCollideMask(BitMask32.allOn())
        self.GroundNP.setScale(1, 1, 1)
        self.GroundNP.node().addShape(BulletTriangleMeshShape(self.GroundMesh, dynamic=False))
        self.loader.loadModel("../assets/circuit.egg").reparentTo(self.GroundNP)
        self.world.attachRigidBody(self.GroundNP.node())






        #The Following code snippet was an object supposed to take the camera's position to see how the camera was behaving

        #self.geomNodes1 = self.loader.loadModel("../assets/PorscheChassis.egg").findAllMatches('**/+GeomNode')
        #self.geomNode1 = self.geomNodes1.getPath(0).node()
        #self.geom1 = self.geomNode1.getGeom(0)
        #self.GroundMesh1 = BulletTriangleMesh()
        #self.GroundMesh1.addGeom(self.geom1)

        #self.SmileyNP = render.attachNewNode(BulletRigidBodyNode('Smiley'))
        #self.SmileyNP.setCollideMask(BitMask32.allOff())
        #self.SmileyNP.setScale(0.5, 0.5, 0.5)
        #self.SmileyNP.node().setMass(0.5)
        #self.SmileyNP.node().setRestitution(0.0001)
        #self.SmileyNP.node().addShape(BulletTriangleMeshShape(self.GroundMesh1, dynamic=True))
        #self.SmileyNP.node().setCcdMotionThreshold(1e-3)
        #self.SmileyNP.node().setCcdSweptSphereRadius(0.10)
        #self.loader.loadModel("../assets/PorscheChassis.egg").reparentTo(self.SmileyNP)
        #self.world.attachRigidBody(self.SmileyNP.node())



        # --------------------Initiate Keyboard Event Listener------------------------

        Controls.__init__(self)
    
        # ----------------------------Configure Tasks---------------------------------

        self.taskMgr.add(self.update, "update")







    def update(self, task):
        self.dt = globalClock.getDt()
        self.world.doPhysics(self.dt)

        # --------------------------Setup Controls------------------------------

        SmileyPos = self.ChassisNP.getPos()
        SmileyVel = self.ChassisNP.node().getLinearVelocity()
        SmileyHPR = self.ChassisNP.getHpr()

        self.SteeringClamp = 35.0
        self.SteeringIncrement = 30.0
        self.engineForce = 0.0
        self.brakeForce = 0.0

        Controls.Update(self)
        self.Vehicle.setSteeringValue(self.Steering, 0)
        self.Vehicle.setSteeringValue(self.Steering, 1)
        self.Vehicle.applyEngineForce(self.engineForce, 2)
        self.Vehicle.applyEngineForce(self.engineForce, 3)
        self.Vehicle.setBrake(self.brakeForce, 2)
        self.Vehicle.setBrake(self.brakeForce, 3)


        # -------------------------Update Camera Position and Rotation----------------------------

        
        self.camera.setPos( SmileyPos.getX()  +  7.6 * Truncate(sin((SmileyHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                            SmileyPos.getY()  -  7.6 * Truncate(cos((SmileyHPR.getX()+self.CamOffset)*(pi/180)), 5)  , 
                            SmileyPos.getZ()  -  1.4 * Truncate(sin(SmileyHPR.getY()*(pi/180)), 5)+0.9
        )
        self.camera.setHpr( SmileyHPR.getX()+self.CamOffset ,
                            0 ,
                            0)





        
        #Change 2 previous functions to be on self.SmileyNP, and uncomment 2 next functions of code -> to see how camera behaves from far away
        
        #self.camera.setPos( SmileyPos.getX() - 5, 
        #                    SmileyPos.getY() - 5, 
        #                    SmileyPos.getZ())
        #
        #self.camera.setHpr(-45, 0, 0)

        # TODO : Add UI
        # TODO : Change Project Name (bruh)

        return task.cont



            

app = MainApp()
app.run()