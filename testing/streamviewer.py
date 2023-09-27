import cv2
import subprocess
from PIL import Image
import redis
import time
import threading


def imagePoster(wait_time, byte_image_list):
    redis_connection = redis.Redis(host = '127.0.0.1', port='6379')
    for i in range(len(byte_image_list)-1,0,-1):
        byte_image_list[i] = byte_image_list[i-1]
    byte_image_list[0] = byte_image_list[len(byte_image_list)-1]
    redis_connection.set('bzoom:RAW', byte_image_list[0])
    time.sleep(wait_time)


def run_imagePoster_indefinitely(wait_time, byte_image_list):
    while True:
        imagePoster(wait_time, byte_image_list)

subprocess.Popen(['redis-server', '--port', '6379'])



images = []
for image_name in ['blue.jpg', 'green.jpg', 'red.jpg', 'tan.jpg']:
    img = Image.open('imagefolder/'+image_name)
    images.append(img.tobytes())
images.append(images[-1])






#EDIT THE TIME HERE
fps = 2
sleeptime = 1/fps

image_poster_thread = threading.Thread(target=run_imagePoster_indefinitely, args=(sleeptime, images))




image_poster_thread.start()






# Define the video stream
stream_url = "http://localhost:8000/video_feed2"

# Open the stream


prevcount = 0
while True:
    cap = cv2.VideoCapture(stream_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
    #time.sleep(1/fps)
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print('hi')
        break
    # Display the resulting frame
    t = time.process_time()
    cv2.imshow('frame', frame)
    x = time.process_time() - t
    print('time taken to read: {}'.format(x))
    # Break the loop on 'q' key press



    if cv2.waitKey(int((sleeptime)*1000)) & 0xFF == ord('q'):
        #print('key was pressed on: {}'.format(x))
        #currcount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #print('length of buffer: {}'.format(currcount))
        #prevcount = currcount

        input('hello')



        
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


