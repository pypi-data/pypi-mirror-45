# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PIL import Image
import re
from thumbor.filters import BaseFilter, filter_method

class Filter(BaseFilter):
    @filter_method(
        BaseFilter.PositiveNonZeroNumber,
        BaseFilter.Boolean,
        BaseFilter.Boolean,
        BaseFilter.PositiveNumber,
        BaseFilter.PositiveNumber,
        BaseFilter.PositiveNumber
    )
    def draw_focal_points(self, line_width=3, show_heatmap=True, show_labels=True, r=0, g=255, b=0):
        img = np.array(self.engine.image)
        class_label_regex = re.compile('DNN Object Detection \(class: ([a-z ]+)\)')
        for focal_point in self.context.request.focal_points:
            width = int(focal_point.width)
            height = int(focal_point.height)
            left = int(focal_point.x - (width / 2))
            top = int(focal_point.y - (height / 2))
            right = left + width
            bottom = top + height

            # A 🔥 heat map 🔥 from white (0% confidence) to green (100% confidence)
            weight = focal_point.weight
            if show_heatmap:
                r = int(255 * (1 - weight))
                g = 255
                b = int(255 * (1 - weight))

            # Draw class labels
            match = class_label_regex.match(focal_point.origin)
            if show_labels and match:
                # one-tenth the height of the box
                label_height = height / 10
                # the font is *about* 30 pixels tall
                scale = label_height / 30
                class_label = match.groups(1)[0]
                cv2.putText(
                    img,
                    ' {} ({})'.format(class_label, weight),
                    (left, top + label_height),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    scale,
                    (r, g, b),
                    line_width
                )
            cv2.rectangle(img, (left, top), (right, bottom), (r, g, b), line_width)
            self.engine.image = Image.fromarray(img)
