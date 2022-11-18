from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from panda3d.bullet import *
from headers.Controls import *
from headers.Camera import *



loadPrcFile("config_file.prc")


class MainApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #self.disableMouse()
        
        # ---------------------------- Setup Debug Mode ------------------------------
        self.debugNode = BulletDebugNode('Debug')
        self.debugNode.showWireframe(True)
        self.debugNode.showConstraints(False)
        self.debugNode.showBoundingBoxes(True)
        self.debugNode.showNormals(False)
        self.debugNP = self.render.attachNewNode(self.debugNode)
        

        # ------------------------- Create Physics World -----------------------------
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.world.setDebugNode(self.debugNP.node())


        # -------------------------------Create Models--------------------------------

        # ------------------ Vehicle :

        self.ChassisGeomNodes = self.loader.loadModel("../assets/untitled.bam").findAllMatches('**/+GeomNode')
        self.ChassisGeomNode = self.ChassisGeomNodes.getPath(0).node()
        self.ChassisGeom = self.ChassisGeomNode.getGeom(0)
        self.ChassisShape = BulletTriangleMesh()
        self.ChassisShape.addGeom(self.ChassisGeom)
        self.ChassisTS = TransformState.makePos(Point3(0, 0, 0))
        self.ChassisTS = self.ChassisTS.setHpr(Point3(0, 0, 0))
        
        self.ChassisNP = self.render.attachNewNode(BulletRigidBodyNode('Vehicle'))
        self.ChassisNP.setPos(0, 0, 1)
        self.ChassisNP.setCollideMask(BitMask32.allOn())
        self.ChassisNP.node().addShape(BulletTriangleMeshShape(self.ChassisShape, dynamic=True), self.ChassisTS)
        self.ChassisNP.node().setCcdMotionThreshold(1e-3)
        self.ChassisNP.node().setCcdSweptSphereRadius(0.10)
        self.ChassisNP.node().setMass(1500.0)
        self.ChassisNP.node().setDeactivationEnabled(False)
        self.loader.loadModel('../assets/nissan.bam').reparentTo(self.ChassisNP)
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
        


        # ------ Heightfield Terrain :

        TerrainScale = [4, 3, 2]
        TerrainPos = [0, 0, 0]

        self.BTerrainNP = self.render.attachNewNode(BulletRigidBodyNode('Terrain'))
        self.BTerrainNP.setPos(TerrainPos[0],
                  TerrainPos[1],
                  TerrainPos[2])
        self.BTerrainNP.setScale(TerrainScale[0],
                     TerrainScale[1],
                     TerrainScale[2])
        self.BTerrainNP.node().addShape(BulletHeightfieldShape(PNMImage(Filename('../assets/tex/output_COP301.png')), 10, ZUp))
        self.world.attachRigidBody(self.BTerrainNP.node())



        self.HeightfieldTex = self.loader.loadTexture("../assets/tex/output_COP30.png")
        self.HeightfieldTex.wrap_u = SamplerState.WM_clamp
        self.HeightfieldTex.wrap_v = SamplerState.WM_clamp
        self.Terrain = ShaderTerrainMesh()
        self.Terrain.heightfield = self.HeightfieldTex
        self.Terrain.target_triangle_width = 10.0
        self.Terrain.generate()

        self.TerrainNP = self.render.attachNewNode(self.Terrain)
        self.TerrainNP.setScale(128*TerrainScale[0], 128*TerrainScale[1], 10*TerrainScale[2])          # 128 is .png's width and height
        self.TerrainNP.setPos(-64*TerrainScale[0]+TerrainPos[0], -64*TerrainScale[1]+TerrainPos[1], -5*TerrainScale[2]+TerrainPos[2])

        self.TerrainShader = Shader.load(Shader.SL_GLSL, "../assets/tex/terrain.vert.glsl", "../assets/tex/terrain.frag.glsl")
        self.TerrainNP.setShader(self.TerrainShader)
        self.TerrainNP.setShaderInput("camera", self.camera)


        # ------------------- Ground :

        self.Geometry = self.loader.loadModel("../assets/circuit.egg").findAllMatches('**/+GeomNode').getPath(0).node().getGeom(0)
        self.GroundMesh = BulletTriangleMesh()
        self.GroundMesh.addGeom(self.Geometry)

        self.GroundNP = self.render.attachNewNode(BulletRigidBodyNode('Ground'))
        self.GroundNP.setPos(0, 0, -1)
        self.GroundNP.setCollideMask(BitMask32.allOn())
        self.GroundNP.setScale(5, 5, 5)
        self.GroundNP.node().addShape(BulletTriangleMeshShape(self.GroundMesh, dynamic=False))
        self.loader.loadModel("../assets/circuit.egg").reparentTo(self.GroundNP)
        self.world.attachRigidBody(self.GroundNP.node())


        # ------------------------------Set Lighting----------------------------------

        self.SunLight = DirectionalLight('Sun')
        self.SunLight.setColor((.8, .8, .8, 1))
        self.SunLightNP = self.render.attachNewNode(self.SunLight)
        self.SunLightNP.setHpr(0, -20, 0)
        self.render.setLight(self.SunLightNP)

        # --------------------Initiate Keyboard Event Listener------------------------

        Controls.__init__(self)
        Camera.__init__(self)

        # ----------------------------Configure Tasks---------------------------------

        self.taskMgr.add(self.update, "update")







    def update(self, task):
        self.dt = globalClock.getDt()
        self.world.doPhysics(self.dt)

        # ------------------------Setup and Update Controls----------------------------



        Controls.Update(self)
        self.Vehicle.setSteeringValue(self.Steering, 0)
        self.Vehicle.setSteeringValue(self.Steering, 1)
        self.Vehicle.applyEngineForce(self.engineForce, 2)
        self.Vehicle.applyEngineForce(self.engineForce, 3)
        self.Vehicle.setBrake(self.brakeForce, 2)
        self.Vehicle.setBrake(self.brakeForce, 3)


        # -------------------Update Camera Position and Rotation----------------------
        print(self.Vehicle.getCurrentSpeedKmHour())
        Camera.Update(self)

        return task.cont



            

app = MainApp()
app.run()




# TODO : Add UI
# TODO : Refactor Vehicle's Wheels definition
# TODO : Fix sudden cam jump when car crashes