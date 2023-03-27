import random
import cv2
import numpy as np

frame_size = (640, 480)
define_gate = 0.7
nms_threshold = 0.3
fps = 10

net = cv2.dnn.readNet("yolo_v3/yolov3.weights", "yolo_v3/yolov3.cfg")

# objects to search
enabled_classes = {0: 'person', 39: 'bottle'}

object_colors = {}
random.seed(10)
# создание цветов для объектов
for key in enabled_classes.keys():
    object_colors[key] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def main():
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        (_h, _w) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, frame_size, swapRB=True, crop=False)
        net.setInput(blob)

        # detect objects
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(output_layers)

        bounding_boxes = []
        confidences = []
        class_nums = []

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_num = np.argmax(scores)
                confidence = scores[class_num]

                if enabled_classes.get(class_num) is None:
                    continue

                if confidence > define_gate:
                    box = detection[0:4] * np.array([_w, _h, _w, _h])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    bounding_boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_nums.append(class_num)

        count = cv2.dnn.NMSBoxes(bounding_boxes, confidences, define_gate, nms_threshold)

        object_rects = {}

        if count is not None:
            for index in count.flatten():
                (x, y) = (bounding_boxes[index][0], bounding_boxes[index][1])
                (w, h) = (bounding_boxes[index][2], bounding_boxes[index][3])

                if object_rects.get(class_nums[index]) is None:
                    object_rects[class_nums[index]] = list()
                object_rects[class_nums[index]].append((x, y, w, h))

                color = object_colors.get(class_nums[index])
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.2f}".format(enabled_classes.get(class_nums[index]), confidences[index])
                cv2.putText(frame, text, (x, y - 6), cv2.FONT_HERSHEY_PLAIN, 1.2, color, 2)

                calc_intersection(objects=object_rects, outer_obj_num=0, inner_obj_num=39, frame=frame)

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1000 // fps) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

# эта функция выведет на экран сообщение о том, что человек что-то пьет, когда бутылочка находится внутри области человека
def calc_intersection(objects, outer_obj_num, inner_obj_num, frame):
    if objects.get(outer_obj_num) is not None and objects.get(inner_obj_num) is not None:
        for inner in objects.get(inner_obj_num):
            ix, iy, iw, ih = inner
            for outer in objects.get(outer_obj_num):
                ox, oy, ow, oh = outer
                # истинно при нахождении внутреннего объекта внутри внешнего полностью
                if (ix > ox) and (iy > oy) and (ix + iw < ox + ow) and (iy + ih < oy + oh):
                    cv2.putText(frame, 'Drinking', ((ox + 3), (oy + 20)), cv2.FONT_HERSHEY_PLAIN, 1.2, (0, 0, 255),
                                2)


if __name__ == '__main__':
    main()
