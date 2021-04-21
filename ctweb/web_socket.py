import logging
import base64
import os
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
import glob
import cv2
from PIL import Image
import numpy as np

define("port", default=8001, help="run on the given port", type=int)

class MainHandler(tornado.websocket.WebSocketHandler):
    count = 0
    def check_origin(self, origin):
        return True

    def open(self):
        print("connected")
        self.frames = []
        logging.info("A client connected.")

    def on_close(self):
        img_array = []
        for filename in glob.glob('Images/*.png'):
            #print(filename)
            img = cv2.imread(filename)
            #height, width, layers = img.shape
            #size = (width, height)
            #nparr = np.fromstring(base64.b64decode(frame), np.uint8)
            #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_array.append(img)

        out = cv2.VideoWriter('Images/test_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (600,450))
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        logging.info("A client disconnected")

    def on_message(self, message):
        #from main.detect import get_face_detect_data
        #image_data = get_face_detect_data(message)
        #print("received",message)
        #print(message)
        image_data = message[22:]#cropping header
        name = 'Images/check'+ str(MainHandler.count) +'.png'
        image = open(name, 'wb')
        image.write(base64.b64decode((image_data)))
        #self.frames.append(image_data)
        image.close()
        MainHandler.count += 1
        if not image_data:
            image_data = message
        self.write_message(image_data)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/websocket", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    print("yes")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctweb.settings")
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()