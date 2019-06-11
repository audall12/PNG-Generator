import os
import random
import struct
import sys
import zlib


MAX_HEIGHT = 2000
MAX_WIDTH = 2000


# ERROR CHECKING ARGUMENTS
# check for 2 command line arguments

if len(sys.argv) != 3:
    print("Usage: randompic.py width height")
    for arg in sys.argv:
        print(arg)
    exit()
    
# check dimensions are between 0 and max dimensions

elif int(sys.argv[1]) > MAX_WIDTH or int(sys.argv[2]) > MAX_HEIGHT:
    print(f"Error: Dimensions must be less than height: {MAX_HEIGHT}pixels and width: {MAX_WIDTH}pixels")
    exit()
elif int(sys.argv[1]) < 0 or int(sys.argv[2]) < 0:
    print("Error: Dimensions must be 0 pixels or above")
    exit()

# check arguments are integers and assign them to variables

try:
    int(sys.argv[1])
    int(sys.argv[2])
    width = int(sys.argv[1])
    height = int(sys.argv[2])
except ValueError:
    print("Error: arguments must be integers")
    exit()

# prompt user for black & white or colour image

valid = False
while not valid:
    response = input('Would you like the image in colour? [Y/N] \n')
    if response == 'Y' or response == 'y':
        valid = True
        colour = True
    elif response == 'N' or response == 'n':
        valid = True
        colour = False

print ('OK, here you go \n')

# create header and IHDR

signature = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

IHDRname = 'IHDR'.encode('ascii')
IHDRdata = struct.pack('!I', width & (2**32-1)) + struct.pack('!I', height & (2**32-1))
IHDRdata += b'\x08'  # bitdepth
if colour:
    IHDRdata += b'\x02' # colour type 2 RGB
else:
    IHDRdata += b'\x00' # colour type 0 black and white
IHDRdata += b'\x00'  # compression
IHDRdata += b'\x00'  # filter
IHDRdata += b'\x00'  # interlace
IHDRcrc = struct.pack('!I', zlib.crc32(IHDRname + IHDRdata) & (2**32-1))
IHDRsize = struct.pack('!I', len(IHDRdata) & (2**32-1))
ihdr = signature + IHDRsize + IHDRname + IHDRdata +IHDRcrc

# create IDAT

if colour:  # 3 bytes per pixel for colour type 2
    width *= 3
    
image = b''
for i in range(height):
    image += b'\0'
    for j in range(width):
        image += struct.pack('!B', random.randint(0, 254) & (2**8-1))
        

compressor = zlib.compressobj()
IDATdata = compressor.compress(image)
IDATdata += compressor.flush()
IDATsize = struct.pack('!I', len(IDATdata) & (2**32-1))
IDATname = 'IDAT'.encode('ascii')
IDATcrc = struct.pack('!I', zlib.crc32(IDATname + IDATdata) & (2**32-1))
idat = IDATsize + IDATname + IDATdata + IDATcrc

# create IEND

IENDsize = struct.pack('!I', 0 & (2**32-1))
IENDname = 'IEND'.encode('ascii')
IENDcrc = struct.pack('!I', zlib.crc32(IENDname) & (2**32-1))
iend = IENDsize + IENDname + IENDcrc

# concatenate all data to write to file

png = ihdr + idat + iend

# create new outfile
# increment number in filename
if not os.path.exists('picture.png'):
    with open("picture.png", "bw") as outfile:
        outfile.write(png)
elif not os.path.exists('picture0.png'):
    with open("picture0.png", "bw") as outfile:
        outfile.write(png)
else:
    i = 0
    while os.path.exists('picture%s.png' % i):
        i += 1
    with open(f'picture{i}.png', 'bw') as outfile:
        outfile.write(png)

    

    

