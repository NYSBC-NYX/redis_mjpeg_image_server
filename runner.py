import threading
import redis
from PIL import Image
import time
import subprocess
import datetime

def send_image_to_redis():
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
    while True:
        data = redis_client.get('bzoom:RAW')
        if data:
            original_image = Image.frombuffer("RGB", (1224, 1024), data)
            resized_image = original_image.resize((640,512))
            out_string = resized_image.tobytes()
            redis_client.set('bzoom:RESIZED', out_string)
        time.sleep(1/20)


def run_uwsgi_server():
    callCommand = ['uwsgi' ,'--socket', '192.168.1.201:3909', '--protocol' ,'http' ,'--master' ,'-p' ,'5' ,'-w' ,'wsgi:app','--logto', './uwsgi_server.log'] 
    with open('uwsgi_server.log', 'a') as uwsgi_log:
        dt_string = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        uwsgi_log.write('UWSGI flask server started at time: {} \n'.format(dt_string))
        subprocess.run(callCommand)


def main():
    uwsgi_server_thread = threading.Thread(target=run_uwsgi_server)
    image_resizing_thread = threading.Thread(target=send_image_to_redis)
    image_resizing_thread.start()
    uwsgi_server_thread.start()
    print('threads running...')
    uwsgi_server_thread.join()




if __name__ == "__main__":
    main()
