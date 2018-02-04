from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import sys
import cv2
import zbar
from PIL import Image

def get_barcode(display=False):

    # Debug mode
    display = False
    if len(sys.argv) > 1:
        display = sys.argv[-1] == 'display'

    # Configuration options
    RESOLUTION = (300, 160)

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
    #print ("PiCamera ready")

    # Initialise OpenCV window
    if display:
        cv2.namedWindow("#cheqout")

    #print ("OpenCV version: %s" % (cv2.__version__))
    #print ("Press q to exit ...")

    scanner = zbar.ImageScanner()

    first = None
    second = None
    third = None

    # Capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # as raw NumPy array
        output = frame.array.copy()

        # raw detection code
        gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY, dstCn=0)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tobytes()

        codes = scanner.scan(raw, width, height, 'Y800')

        if len(codes) > 0:
            if first is None:
                first = codes
            elif second is None:
                second = codes
            elif third is None:
                third = codes
        
        cv2.imshow("#cheqout", output)

        # clear stream for next frame
        rawCapture.truncate(0)

        # Wait for the magic key
        if display:
            keypress = cv2.waitKey(1) & 0xFF

        if third is not None:
            if first == second and second == third:
                (third[0])
                break;
            else:
                first = None
                second = None
                third = None

    # When everything is done, release the capture
    camera.close()
    if display:
        cv2.destroyAllWindows()

    return third[0]
