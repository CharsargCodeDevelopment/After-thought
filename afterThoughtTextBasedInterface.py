from afterThought import *
from PIL import *


from tkinter import filedialog as fd

depth_filename = 'MouthTestTexture.png'

depth_filename = fd.askopenfilename()
image_texture_filename = fd.askopenfilename()

#input_folder = fd.askopenfilenames()
location = fd.askdirectory()

frame_count = int(input("How many frames do you have?: "))
frame_start = int(input("Enter the start frame: "))
"""
depth_filename = 'MouthTestTexture.png'

response = ""

while response not in list("yn"):
    response = input("Select File? (Current Selection: MouthTestTexture.png) (y/n):")


print(response)
if response == "y":
    print("select File")
    depth_filename = fd.askopenfilename()
    print("File Selected")

"""

# Load your image with Pillow
depthImage = Image.open(depth_filename).convert('L')   # or .png, etc.
depthImage = depthImage.transpose(Image.FLIP_TOP_BOTTOM)


# Convert the Pillow Image to a NumPy array
depthMap = np.array(depthImage).astype(np.float32) / 255.0



texture = LoadTextureFile(".",1,"MouthTestTexture",namingConvention = SingleImageTextureNamingConvention)
imageTexture = Image.open(image_texture_filename)   # or .png, etc.

#import afterThoughtPreviewMatPlot as AFP
import afterThoughtPreview as AFP
#AFP.previewPickFile(objectBuffer)


for frameIndex in range(frame_start,frame_start+frame_count):

    objectBuffer = LoadPickFile(location,frameIndex)
    UVBuffer = LoadUVFile(location,frameIndex)
    View_dir = LoadViewDirFile(location,frameIndex)
    print("Drawing")
    #AFP.viewPngBuffer(UVBuffer,res = 32,doTracer=False)
    print("Applying UV")
    imageBuffer = ApplyUVToImage(UVBuffer,imageTexture)
    #AFP.viewPngBuffer(imageBuffer,res = 8,doTracer=False,SupressErrors = False)

    print("Masking Background")
    backgroundMask = MaskObject(objectBuffer,0)
    #AFP.viewPngBuffer(backgroundMask,res = 8,doTracer=False,SupressErrors = False)


    print("Parralxing")
    UVBuffer = ApplyParralaxMapping(UVBuffer,depthMap,View_dir)
    #AFP.viewPngBuffer(UVBuffer,res = 4,doTracer=False,SupressErrors = False)



    print("Applying UV")
    imageBuffer = ApplyUVToImage(UVBuffer,imageTexture)
    #AFP.viewPngBuffer(imageBuffer,res = 8,doTracer=False,SupressErrors = True)


    print("Loading Source Image")
    sourceImage = LoadImageFile(location,frameIndex)
    output = BlendBetweenBuffersWithMask(sourceImage,imageBuffer,backgroundMask)
    print("saving image")
    SaveBuffer(output,filename = f"output/{frameIndex}.png")
    print("Drawing")
    #AFP.viewPngBuffer(output,res = 32,doTracer=False,SupressErrors = False)
    #AFP.viewPngBuffer(output,res = 4,doTracer=False,SupressErrors = False)

    #AFP.viewPngBuffer(output,res = 2,doTracer=False,SupressErrors = False)
