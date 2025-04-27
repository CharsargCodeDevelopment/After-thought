import OpenEXR
from PIL import Image
import numpy as np
def BlenderDefultNaming(location,index,name,extension):

    indexName = str(index)
    indexName = "".join(["0"]*(4-len(indexName)))+indexName
    #print(indexName)
    return f"{location}/{name}{indexName}{extension}"


def LoadEXRFile(location,index,name,extension = ".exr",namingConvention = BlenderDefultNaming,PixelFormat = "RGBA"):
    
    with OpenEXR.File(namingConvention(location,index,name,extension)) as infile:
        RGB = infile.channels()[PixelFormat].pixels
        height, width, _ = RGB.shape
        data = {"width":width,"height":height,"data":[]}
        for y in range(height):
            for x in range(width):
                pixel = tuple(RGB[y, x])
                #print(f"pixel[{y}][{x}]={pixel}")
                data["data"].append(pixel)
    return data


location = "Render"
fileIndex = ""


print(BlenderDefultNaming(location,1,"Depth",".png"))






def LoadPickFile(location,index):
    pickFileData = LoadEXRFile(location,index,"Pick")
    objectPixels = (set(pickFileData["data"]))
    objectPixelToObjectID = {}
    for i,objectPixel in enumerate(objectPixels):
        objectPixelToObjectID[objectPixel]=i
    print(objectPixelToObjectID)


    objectBuffer = {"width":pickFileData["width"],"height":pickFileData["height"],"data":[],"objectPixelToObjectID":objectPixelToObjectID}


    i = 0
    for y in range(pickFileData["height"]):
        for x in range(pickFileData["width"]):
            pixel = pickFileData["data"][i]
            objectBuffer["data"].append(objectPixelToObjectID[pixel])
            i+=1
    return objectBuffer


def LoadPositionFile(location,index,name="Position",extension=".png",namingConvention = BlenderDefultNaming):

    with Image.open(namingConvention(location,index,name,extension)) as im:
        positionBuffer = {"width":im.size[0],"height":im.size[1],"data":[]}
        for y in range(positionBuffer["height"]):
            for x in range(positionBuffer["width"]):
                pixel = im.getpixel((x,y))
                position = [((pixel[i]/255)*2)-1 for i in range(3)]
                #position = [pixel[i]/255 for i in range(3)]
                #if pixel[3] > 128:
                #    position = [-pixel[i] for i in range(3)]
                #else:
                #    position = [pixel[i] for i in range(3)]
                #position = [max(0,-position[i]) for i in range(3)]
                #position = [min(1,position[i]) for i in range(3)]
                #print(position)
                positionBuffer["data"].append(position)
    return positionBuffer

def LoadImageFile(location,index,name="Image",extension=".png",namingConvention = BlenderDefultNaming):

    with Image.open(namingConvention(location,index,name,extension)) as im:
        imageBuffer = {"width":im.size[0],"height":im.size[1],"data":[]}
        for y in range(imageBuffer["height"]):
            for x in range(imageBuffer["width"]):
                pixel = im.getpixel((x,y))
                pixel = [pixel[i]/255 for i in range(3)]
                #if pixel[3] > 128:
                #    position = [-pixel[i] for i in range(3)]
                #else:
                #    position = [pixel[i] for i in range(3)]
                #position = [max(0,-position[i]) for i in range(3)]
                #position = [min(1,position[i]) for i in range(3)]
                #print(position)
                imageBuffer["data"].append(pixel)
    return imageBuffer


def LoadUVFile(location,index):
    pickFileData = LoadEXRFile(location,index,"Uv")


    objectBuffer = {"width":pickFileData["width"],"height":pickFileData["height"],"data":[]}


    i = 0
    for y in range(pickFileData["height"]):
        for x in range(pickFileData["width"]):
            pixel = pickFileData["data"][i]
            objectBuffer["data"].append(pixel)
            i+=1
    return objectBuffer


def LoadViewDirFile(location,index):
    pickFileData = LoadEXRFile(location,index,"View_Dir")


    objectBuffer = {"width":pickFileData["width"],"height":pickFileData["height"],"data":[]}


    i = 0
    for y in range(pickFileData["height"]):
        for x in range(pickFileData["width"]):
            pixel = pickFileData["data"][i]
            objectBuffer["data"].append(pixel)
            i+=1
    return objectBuffer


def parallax_mapping(tex_coords, view_dir, depth_map, height_scale):
    """
    Simulates parallax mapping.
    
    Parameters:
    - tex_coords: np.array([u, v]) -- texture coordinates
    - view_dir: np.array([x, y, z]) -- view direction vector
    - depth_map: 2D numpy array or function that takes (u, v) and returns depth (height)
    - height_scale: float -- scale for height

    Returns:
    - np.array([new_u, new_v]) -- new texture coordinates
    """
    # Assuming depth_map is a 2D numpy array and tex_coords are normalized (0-1)
    height = depth_map_sample(depth_map, tex_coords)
    p = (view_dir[:2] / view_dir[2]) * (height * height_scale)
    return tex_coords - p

def depth_map_sample(depth_map, tex_coords):
    """
    Sample the depth map at given texture coordinates.
    Assumes depth_map is a numpy array with values between 0 and 1.
    """
    h, w = depth_map.shape
    u = np.clip(tex_coords[0], 0.0, 1.0) * (w - 1)
    v = np.clip(tex_coords[1], 0.0, 1.0) * (h - 1)
    u_int, v_int = int(u), int(v)
    return depth_map[v_int, u_int]


def ApplyParralaxMapping(UVBuffer,depth_map,viewDir,height_scale = 1):
    i = 0
    newUV = UVBuffer.copy()
    newUV["data"] = []
    for y in range(UVBuffer["height"]):
        for x in range(UVBuffer["width"]):
            pixel = UVBuffer["data"][i]
            
            tex_coords = np.array([pixel[0],pixel[1]])
            view_dir = np.array(viewDir["data"][i])
            
            tex_coords = parallax_mapping(tex_coords,view_dir,depth_map,height_scale = 1)
            
            newUV["data"].append((tex_coords[0],tex_coords[1],0))
            i+=1
    return newUV


def ApplyUVToTexture(UVBuffer,texture):
    i = 0
    newImage = UVBuffer.copy()
    h = texture["height"]
    w = texture["width"]
    #(texture.size)
    newImage["data"] = []
    for y in range(UVBuffer["height"]):
        for x in range(UVBuffer["width"]):
            uv = UVBuffer["data"][i]
            #print(uv)
            if not False in [np.isfinite(uv[j]) for j in range(2)]:
                u = int(uv[1]*h) #y
                v = int(uv[0]*w) # x
                index = u*w + x #y*w + x
                #print(texture)
                textureValue = texture["data"][index]
                newImage["data"].append(textureValue)
                #print(texture[int(uv[1]*h), int(uv[0]*w)])
            else:
                newImage["data"].append([0,0,0])
            
            i+=1
    return newImage
def ApplyUVToImage(UVBuffer,image):
    i = 0
    newImage = UVBuffer.copy()
    h = image.size[1]
    w = image.size[0]
    #(texture.size)
    newImage["data"] = []
    for y in range(UVBuffer["height"]):
        for x in range(UVBuffer["width"]):
            uv = UVBuffer["data"][i]
            #print(uv)
            if not False in [np.isfinite(uv[j]) for j in range(2)]:
                u = int(uv[1]*h) #y
                v = int(uv[0]*w) # x
                index = u*w + x #y*w + x
                #print(texture)
                textureValue = image.getpixel((v%h,u%w))
                newImage["data"].append([textureValue[j]/255 for j in [0,1,2]])
                #print(texture[int(uv[1]*h), int(uv[0]*w)])
            else:
                newImage["data"].append([0,0,0])
            
            i+=1
    return newImage


def LoadTextureFile(location,index,name,extension = ".png",namingConvention=BlenderDefultNaming):
    with Image.open(namingConvention(location,index,name,extension)) as im:
        positionBuffer = {"width":im.size[0],"height":im.size[1],"data":[]}
        for y in range(positionBuffer["height"]):
            for x in range(positionBuffer["width"]):
                pixel = im.getpixel((x,y))
                pixel = [pixel[i]/255 for i in range(3)]
                #position = [pixel[i]/255 for i in range(3)]
                #if pixel[3] > 128:
                #    position = [-pixel[i] for i in range(3)]
                #else:
                #    position = [pixel[i] for i in range(3)]
                #position = [max(0,-position[i]) for i in range(3)]
                #position = [min(1,position[i]) for i in range(3)]
                #print(position)
                positionBuffer["data"].append(pixel)
    return positionBuffer

def SingleImageTextureNamingConvention(location,index,name,extension):
    
    #print(indexName)
    return f"{location}/{name}{extension}"

def MaskObject(objectBuffer,obj):
    i = 0
    newImage = objectBuffer.copy()
    #(texture.size)
    newImage["data"] = []
    for y in range(objectBuffer["height"]):
        for x in range(objectBuffer["width"]):
            objAtPixel = objectBuffer["data"][i]
            #print(pixel)
            if objAtPixel == obj:
                newImage["data"].append([1,1,1])
            else:
                newImage["data"].append([0,0,0])
            
            i+=1
    return newImage


def BlendBetweenBuffersWithMask(buffer1,buffer2,mask):
    i = 0
    newImage = buffer1.copy()
    #(texture.size)
    newImage["data"] = []
    for y in range(buffer1["height"]):
        for x in range(buffer1["width"]):
            pixel1 = buffer1["data"][i]
            pixel2 = buffer2["data"][i]
            #print(pixel)
            if mask["data"][i][0] > 0.5:
                newImage["data"].append(pixel1)
            else:
                newImage["data"].append(pixel2)
            
            i+=1
    return newImage

def SaveBuffer(buffer,filename = "buffer.png"):
    i = 0
    #(texture.size)
    #newImage["data"] = []
    im = Image.new(mode="RGB", size=(buffer["width"], buffer["height"]))

    for y in range(buffer["height"]):
        for x in range(buffer["width"]):
            pixel = buffer["data"][i]
            #print(pixel)
            im.putpixel((x,y),tuple([int(pixel[j]*255) for j in range(3)]))
            
            i+=1
    im.save(filename)
    #return newImage
    
    



if __name__ == '__main__':
    # Load your image with Pillow
    depthImage = Image.open('MouthTestTexture.png').convert('L')   # or .png, etc.


    depthImage = depthImage.transpose(Image.FLIP_TOP_BOTTOM)
    # Convert the Pillow Image to a NumPy array
    depthMap = np.array(depthImage).astype(np.float32) / 255.0



    texture = LoadTextureFile(".",1,"MouthTestTexture",namingConvention = SingleImageTextureNamingConvention)
    #print(len(texture))
    imageTexture = Image.open('UVGrid.png')   # or .png, etc.
    objectBuffer = LoadPickFile(location,1)
    #import afterThoughtPreviewMatPlot as AFP
    import afterThoughtPreview as AFP
    #AFP.previewPickFile(objectBuffer)


    UVBuffer = LoadUVFile(location,1)
    View_dir = LoadViewDirFile(location,1)
    #positionBuffer = LoadPositionFile(location,1)
    #AFP.viewPositionBuffer(positionBuffer)
    #AFP.viewPngBuffer(UVBuffer,res = 4,doTracer=False)
    AFP.viewPngBuffer(UVBuffer,res = 32,doTracer=False)
    print("Applying UV")
    #imageBuffer = ApplyUVToTexture(UVBuffer,texture)
    imageBuffer = ApplyUVToImage(UVBuffer,imageTexture)
    #AFP.viewPngBuffer(imageBuffer,res = 8,doTracer=False,SupressErrors = False)

    backgroundMask = MaskObject(objectBuffer,0)

    #AFP.viewPngBuffer(backgroundMask,res = 8,doTracer=False,SupressErrors = False)





    print("Parralxing")
    UVBuffer = ApplyParralaxMapping(UVBuffer,depthMap,View_dir,height_scale = -0.03)
    #AFP.viewPngBuffer(UVBuffer,res = 4,doTracer=False,SupressErrors = False)



    print("Applying UV")
    imageBuffer = ApplyUVToImage(UVBuffer,imageTexture)
    #AFP.viewPngBuffer(imageBuffer,res = 8,doTracer=False,SupressErrors = True)



    sourceImage = LoadImageFile(location,1)
    output = BlendBetweenBuffersWithMask(sourceImage,imageBuffer,backgroundMask)
    print("saving image")
    SaveBuffer(output)
    AFP.viewPngBuffer(output,res = 32,doTracer=False,SupressErrors = False)
    #AFP.viewPngBuffer(output,res = 4,doTracer=False,SupressErrors = False)

    #AFP.viewPngBuffer(output,res = 2,doTracer=False,SupressErrors = False)
