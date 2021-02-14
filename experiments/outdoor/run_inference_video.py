import cv2
import time

from segmentation_inference import *
import models.model_1.model as Model

#cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture("/Users/michal/Movies/park.mp4")
cap = cv2.VideoCapture("/home/michal/Videos/park.mp4")

si = SegmentationInference(Model, "models/model_1/trained/", 5)

writer = None
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
writer = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480)) 


fps_smooth = 0.0
frame_skip = 20
next_frame = 0
cnt = 0

def print_video(image, text):
    x = cv2.putText(image,text,(40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1,lineType=cv2.LINE_AA)

while(True):
    ret, frame = cap.read()

    frame = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
    if cnt > next_frame:
        time_start = time.time()
        prediction_np, mask, result = si.process(frame)
        time_stop  = time.time()

        fps = 1.0/(time_stop - time_start)
        
        result = (result*255).astype(numpy.uint8)

        text  = "fps= " + str(round(fps, 1))

        im_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
        print_video(im_bgr, text)
        #cv2.imshow('frame', im_bgr)

        if writer is not None:
            writer.write(im_bgr)

        frame_skip = 25/fps
        frame_skip = int(numpy.clip(frame_skip, 1, 500))

        next_frame = cnt + frame_skip

        print(fps, frame_skip, fps*frame_skip)

    cnt+= 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
