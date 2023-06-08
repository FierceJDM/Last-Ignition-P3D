from panda3d.core import *
from panda3d.bullet import *
import json
from PIL import Image



class NewTerrain():
    def __init__(self, name, pos, mappath, map1pixelpath, everythingnp, world, loader, camera):
        TerrainScale = [6, 6, 3]
        self.BTerrainNP = everythingnp.attachNewNode(BulletRigidBodyNode(name))
        self.BTerrainNP.setPos(pos[0],
                               pos[1],
                               pos[2])
        self.BTerrainNP.setScale(TerrainScale[0],
                                 TerrainScale[1],
                                 TerrainScale[2])
        self.BTerrainNP.node().addShape(BulletHeightfieldShape(PNMImage(Filename(map1pixelpath)), 10, ZUp))
        world.attach(self.BTerrainNP.node())

        self.HeightfieldTex = loader.loadTexture(mappath)
        self.HeightfieldTex.wrap_u = SamplerState.WM_clamp
        self.HeightfieldTex.wrap_v = SamplerState.WM_clamp
        self.Terrain = ShaderTerrainMesh()
        self.Terrain.setChunkSize(32)
        self.Terrain.set_heightfield(self.HeightfieldTex)
        self.Terrain.set_target_triangle_width(10.0)
        self.TerrainNP = everythingnp.attachNewNode(self.Terrain)
        self.TerrainNP.setScale(128*TerrainScale[0], 128*TerrainScale[1], 10*TerrainScale[2])          # 128 is .png's width and height
        self.TerrainNP.setPos(-64*TerrainScale[0]+pos[0], -64*TerrainScale[1]+pos[1], -5*TerrainScale[2]+pos[2])
        self.TerrainNP.setShader(Shader.load(Shader.SL_GLSL, "../assets/media/terrain.vert.glsl", "../assets/media/terrain.frag.glsl"))
        self.TerrainNP.setShaderInput("camera", camera)
        self.Terrain.generate()












        #-------------------------------TODO : Texture Generation (WIP)------------------------------------------

        #-------- Make Texture --------

        TexChart = Image.open(mappath) #Change this
        RealTex = Image.new(mode="RGB", size=(128*TerrainScale[0], 128*TerrainScale[1]))
        Tile1 = Image.open("../assets/media/Tiles/Tile1.png")
        #Open all tiles of 16*16
        for x in range(128):
            for y in range(128):
                if TexChart.getpixel((x, y)) == (99, 99, 99, 255):
                    for x2 in range(6):
                        for y2 in range(6):
                            pix = Tile1.getpixel((x2, y2))
                            RealTex.putpixel((6*x+x2, 6*y+y2) ,(pix))
                #elif TexChart.getpixel((x, y)) == (255, 0, 0, 255):
                    #print tile for red

        RealTex.save("../assets/media/F.png")
        #close everything else


        #-------- Load Texture --------

        tsss = TextureStage('tsss')
        sand_tex = loader.load_texture("../assets/media/F.png")
        sand_tex.setWrapU(Texture.WMBorderColor)
        sand_tex.setWrapV(Texture.WMBorderColor)
        self.TerrainNP.setTexture(tsss, sand_tex)
        self.TerrainNP.setTexScale(tsss, 1, 1)


        #-------------------------------      Texture Generation (WIP)     ------------------------------------------






    def Unload(self, world):
        world.remove(self.BTerrainNP.node())
        self.BTerrainNP.removeNode()
        self.TerrainNP.detachNode()
















def InitiateAllObjects(self):
    # ---------------------------- Setup Debug Mode ------------------------------
    self.DebugNP = self.EverythingNP.attachNewNode(BulletDebugNode('Debug'))
    self.DebugNP.node().showWireframe(True)
    self.DebugNP.node().showConstraints(False)
    self.DebugNP.node().showBoundingBoxes(True)
    self.DebugNP.node().showNormals(False)

    # ------------------------- Create Physics World -----------------------------
    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.world.setDebugNode(self.DebugNP.node())
    # -------------------------------Create Models--------------------------------
    # ------------------ Vehicle :
    MDFile = open("../assets/cars/nissan/metadata.json")
    self.VehicleMetadata = json.load(MDFile)
    self.ChassisGeomNodes = self.loader.loadModel("../assets/cars/nissan/untitled.bam").findAllMatches('**/+GeomNode')
    self.ChassisGeomNode = self.ChassisGeomNodes.getPath(0).node()
    self.ChassisGeom = self.ChassisGeomNode.getGeom(0)
    self.ChassisShape = BulletTriangleMesh()
    self.ChassisShape.addGeom(self.ChassisGeom)
    self.ChassisTS = TransformState.makePos(Point3(0, 0, 0))
    self.ChassisTS = self.ChassisTS.setHpr(Point3(0, 0, 0))

    self.ChassisNP = self.EverythingNP.attachNewNode(BulletRigidBodyNode('Vehicle'))
    self.ChassisNP.setPos(0, 0, 1)
    self.ChassisNP.setCollideMask(BitMask32.allOn())
    self.ChassisNP.node().addShape(BulletTriangleMeshShape(self.ChassisShape, dynamic=True), self.ChassisTS)
    self.ChassisNP.node().setCcdMotionThreshold(1e-3)
    self.ChassisNP.node().setCcdSweptSphereRadius(0.10)
    self.ChassisNP.node().setMass(1500.0)
    self.ChassisNP.node().setDeactivationEnabled(False)
    self.loader.loadModel('../assets/cars/nissan/nissan.egg').reparentTo(self.ChassisNP)
    self.world.attach(self.ChassisNP.node())
    self.Vehicle = BulletVehicle(self.world, self.ChassisNP.node())
    self.Vehicle.setCoordinateSystem(ZUp)
    self.world.attach(self.Vehicle)
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
        self.WheelsList[i] = self.loader.loadModel('../assets/cars/porsche/PorscheWheel.egg')
        self.WheelsList[i].reparentTo(self.EverythingNP)
        self.WheelsList[i+4] = self.Vehicle.createWheel()
        self.WheelsList[i+4].setNode(self.WheelsList[i].node())
        WheelsPos = self.VehicleMetadata["WheelsPos"]
        if i == 0:
            self.WheelsList[i+4].setChassisConnectionPointCs(Point3(WheelsPos["1"]["X"], WheelsPos["1"]["Y"], WheelsPos["1"]["Z"]))
            self.WheelsList[i+4].setFrontWheel(True)
        elif i == 1:
            self.WheelsList[i+4].setChassisConnectionPointCs(Point3(WheelsPos["2"]["X"], WheelsPos["2"]["Y"], WheelsPos["2"]["Z"]))
            self.WheelsList[i+4].setFrontWheel(True)
        elif i == 2:
            self.WheelsList[i+4].setChassisConnectionPointCs(Point3(WheelsPos["3"]["X"], WheelsPos["3"]["Y"], WheelsPos["3"]["Z"]))
        else:
            self.WheelsList[i+4].setChassisConnectionPointCs(Point3(WheelsPos["4"]["X"], WheelsPos["4"]["Y"], WheelsPos["4"]["Z"]))
        self.WheelsList[i+4].setWheelDirectionCs(Vec3(0, 0, -1))
        self.WheelsList[i+4].setWheelAxleCs(Vec3(1, 0, 0))
        self.WheelsList[i+4].setWheelRadius(self.VehicleMetadata["WheelsRadius"])
        self.WheelsList[i+4].setMaxSuspensionTravelCm(10.0)
        self.WheelsList[i+4].setSuspensionStiffness(40.0)
        self.WheelsList[i+4].setWheelsDampingRelaxation(2.3)
        self.WheelsList[i+4].setWheelsDampingCompression(4.4)
        self.WheelsList[i+4].setFrictionSlip(100)
        self.WheelsList[i+4].setRollInfluence(0.1)


    # ------------------- Terrain :
    self.TerrainsStatus = 0
    self.Terrain2 = None
    self.Terrain1 = NewTerrain('Terrain1', [0, 0, 0], "../assets/media/output_COP30.png", "../assets/media/output_COP301.png", self.EverythingNP, self.world, self.loader, self.camera)


    # ------------------------------Set Lighting----------------------------------
    self.SunLight = DirectionalLight('Sun')
    self.SunLight.setColor((.8, .8, .8, 1))
    self.SunLightNP = self.EverythingNP.attachNewNode(self.SunLight)
    self.SunLightNP.setHpr(0, -20, 0)
    self.EverythingNP.setLight(self.SunLightNP)