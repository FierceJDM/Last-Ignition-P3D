from PIL import Image

def FilterRGB(close_list, ref_rgb):
    temp_list = []
    step = 5
    if len(close_list) == 1:
        return close_list[0]
    while len(close_list) > 1:
        if step > 1:
            step -= 1
        for i in range(len(close_list)-1):
            if close_list[i][0]-step < ref_rgb[0] < close_list[i][0]+step:
                    if close_list[i][1]-step < ref_rgb[1] < close_list[i][1]+step:
                        if close_list[i][2]-step < ref_rgb[2] < close_list[i][2]+step:
                            temp_list.append(close_list[i])
        if len(temp_list) == 1:
            return temp_list[0]
        elif len(temp_list) == 0:
            return close_list[0]
        else:
            close_list = temp_list

class Map():
    def GetElevation(ref_rgb):
        # ---------------- Pick Close RGB values in colorindex.png

        close_list = []
        index_image = Image.open("../../assets/colorindex.png")
        pixels = index_image.load()
        for i in range(index_image.height):
            if pixels[0, i][0]-10 < ref_rgb[0] < pixels[0, i][0]+10:
                if pixels[0, i][1]-10 < ref_rgb[1] < pixels[0, i][1]+10:
                    if pixels[0, i][2]-10 < ref_rgb[2] < pixels[0, i][2]+10:
                        close_list.append(pixels[0, i])

        # ----------------- Filter Current List and keep Closest Possible RGB value --------------

        closest_rgb = FilterRGB(close_list, ref_rgb)

        # ------------------------- Find Elevation from RGB value --------------------------------

        for i in range(index_image.height):
            if pixels[0, i] == closest_rgb
                fake_elevation = i

        # ------------------------- Transform fake elevation to real -----------------------------
        # TODO: render elevation

    def Update():
        map_image = Image.open("../../assets/map.png")
        pixels = map_image.load()
        # elevation = GetElevation((r,g,b,a))
        
        # TODO: add data block to .egg file

Map.GetElevation((161,66,0,255))