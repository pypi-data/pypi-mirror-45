import cv2
import numpy as np
import os
from thumbor.detectors import BaseDetector
from thumbor.point import FocalPoint
from thumbor.utils import logger
from thumbor_extras.detectors import coco_classes

class Detector(BaseDetector):
    def __init__(self, context, index, detectors):
        super(Detector, self).__init__(context, index, detectors)
        this_dir = os.path.dirname(os.path.abspath(__file__))
        self.net = cv2.dnn.readNet(
            # these are downloaded during setup.py egg_info
            os.path.join(this_dir, 'model_files/frozen_inference_graph.pb'),
            os.path.join(this_dir, 'model_files/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')
        )

    def detect(self, callback):
        engine = self.context.modules.engine
        try:
            img = np.array(engine.image)
            self.net.setInput(cv2.dnn.blobFromImage(img, size=(300, 300), swapRB=True))
            detections = self.net.forward()
        except Exception as e:
            logger.exception(e)
            logger.warn('Error during feature detection; skipping to next detector')
            self.next(callback)
            return

        confidence_threshold = 0.2
        if detections.shape[2] > 0:
            for detection in detections[0, 0, :, :]:
                confidence = float(detection[2])
                if confidence < confidence_threshold:
                    continue
                class_id = int(detection[1]) - 1 # make it zero-indexed
                class_name = coco_classes[class_id]
                left = int(detection[3] * img.shape[1])
                top = int(detection[4] * img.shape[0])
                right = int(detection[5] * img.shape[1])
                bottom = int(detection[6] * img.shape[0])
                width = right - left
                height = bottom - top
                # If the detection is of a person,
                # and the person is vertically oriented,
                # use the upper 1/4 of the box - focus on the face.
                # In the case the person is upside down, it would focus on the feet.
                # But consider - whoever is publishing a picture of an upside down person
                # might appreciate that it focuses on the feet.
                if class_name == 'person' and height > width:
                    height = int(height * 0.25)
                self.context.request.focal_points.append(
                    FocalPoint.from_dict({
                        'x'      : left + (width / 2),
                        'y'      : top + (height / 2),
                        'width'  : width,
                        'height' : height,
                        'z'      : confidence,
                        'origin' : 'DNN Object Detection (class: {})'.format(class_name)
                    })
                )
            callback()
        else:
            self.next(callback)
