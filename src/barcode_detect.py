from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import cv2
import zbar
from PIL import Image

# Debug mode
DEBUG = True
if len(sys.argv) > 1:
	DEBUG = sys.argv[-1] == 'DEBUG'

# Configuration options
FULLSCREEN = not DEBUG
if not DEBUG:
    RESOLUTION = (800, 480)
else:
	RESOLUTION = (480, 270)

# Initialise Raspberry Pi camera
camera = PiCamera()
camera.resolution = RESOLUTION
#camera.framerate = 10
camera.vflip = True
camera.hflip = True
#camera.color_effects = (128, 128)
# set up stream buffer
rawCapture = PiRGBArray(camera, size=RESOLUTION)
# allow camera to warm up
time.sleep(0.1)
print ("PiCamera ready")

# Initialise OpenCV window
if FULLSCREEN:
	cv2.namedWindow("#cheqout", cv2.WND_PROP_FULLSCREEN)
	cv2.setWindowProperty("#cheqout", cv2.WND_PROP_FULLSCREEN, 1)
else:
	cv2.namedWindow("#cheqout")

print ("OpenCV version: %s" % (cv2.__version__))
print ("Press q to exit ...")

scanner = zbar.ImageScanner()
#scanner.parse_config('enable')

# Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # as raw NumPy array
    output = frame.array.copy()

    # raw detection code
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY, dstCn=0)
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()

    #camera.capture('image.jpg')
    #time.sleep(0.5)
    #image = Image.open('image.jpg')
    codes = scanner.scan(raw, width, height, 'Y800')
    print(codes)
    #time.sleep(0.5)
    # create a reader
    #image = zbar.Images()
    #scanner.scan(image)
    #image = scanner.scan(width, height, 'Y800', raw)
    # extract results
    #for symbol in image:
        # do something useful with results
        #print ('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)

    # show the frame
    cv2.imshow("#cheqout", output)

    # clear stream for next frame
    rawCapture.truncate(0)

    # Wait for the magic key
    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord('q'):
    	break

# When everything is done, release the capture
camera.close()
cv2.destroyAllWindows()
