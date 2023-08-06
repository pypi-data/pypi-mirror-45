import numpy as np
from PIL import Image, ImageDraw


class Processor:
    def __init__(self, image, boxes, labels, internal, cut_size=(300, 300), split=True):
        self.image = np.asarray(image)
        self.boxes = boxes
        self.labels = labels
        self.internal = internal
        self.cut_size = cut_size
        self.split = split

        self.cut_images, self.cut_bboxes, self.cut_labels = self.bboxes_and_labels()
        self.cis, self.cbs, self.cls = self.drop_empty_pictures()

    @property
    def cut_image_with_info(self):
        for i, _ in enumerate(self.cis):
            image = Image.fromarray(self.cis[i])
            """
            # FOR DEBUG
            for cbs in self.cbs[i]:
                draw = ImageDraw.Draw(image)
                draw.rectangle((cbs[0], cbs[2], cbs[1], cbs[3]), fill=False, outline=(255, 0, 0))
            """
            yield image, self.cbs[i], self.cls[i]

    def drop_empty_pictures(self):
        # cut images
        cis = []
        # cut bboxes
        cbs = []
        # cut labels
        cls = []
        for i, b in enumerate(self.cut_labels):
            cis.append(self.cut_images[b])
            cbs.append(self.cut_bboxes[b])
            cls.append(self.cut_labels[b])
        assert len(cls) == len(cis) == len(cbs)

        return cis, cbs, cls

    def image_cut_rules(self):
        h, w, _ = self.image.shape
        cut_h, cut_w = self.cut_size
        for dh in range((h // cut_h) - 1):
            for dw in range((w // cut_w) - 1):
                ch = dh * cut_h
                cw = dw * cut_w
                yield ch, ch + cut_h, cw, cw + cut_w

        """
        half slipped
        """
        begin_h = cut_h + cut_h // 2
        begin_w = cut_w + cut_w // 2

        if self.split:
            for dh in range((h // cut_h) - 2):
                for dw in range((w // cut_w) - 2):
                    ch = dh * cut_h + begin_h
                    cw = dw * cut_w + begin_w
                    yield ch, ch + cut_h, cw, cw + cut_w

    def bboxes_and_labels(self):
        """
        cut bboxes and labels
        TODO: should be better
        :return:
        """

        cut_img = dict()
        box = {}
        label = {}
        for count, (ch, ch_next, cw, cw_next) in enumerate(self.image_cut_rules()):

            if count not in cut_img.keys():
                cut_img[count] = []
            cut_img[count] = self.image[ch:ch_next, cw:cw_next]
            c = Image.fromarray(cut_img[count])
            c.save("./demo/imgs/{}.jpg".format(count))

            for boxes, labels in zip(self.boxes, self.labels):
                # boxes['x1'], boxes['x2'], boxes['y1'], boxes['y2']
                bx1, bx2, by1, by2 = boxes[0], boxes[1], boxes[2], boxes[3]

                """
                initialize the position of box
                """
                if self.in_cur_picture((ch, ch_next, cw, cw_next), (bx1, bx2, by1, by2)):
                    if count not in box.keys():
                        box[count] = []
                        label[count] = []
                    boxes[0] = bx1 - cw
                    boxes[1] = bx2 - cw
                    boxes[2] = by1 - ch
                    boxes[3] = by2 - ch
                    box[count].append(boxes)
                    label[count].append(labels)
                    print(boxes, ch, cw)
        return cut_img, box, label

    @staticmethod
    def between(p1, p2, target):
        return p1 <= target, p2

    def in_cur_picture(self, picture_position, bbox_coordinate):
        # CAUTION: the coordinate for picture and bbox is not the same.
        py1, py2, px1, px2 = picture_position
        bx1, bx2, by1, by2 = bbox_coordinate
        print('ppos', picture_position, 'bpos', bbox_coordinate)
        if self.internal:
            """
            (px1, py1)
            |----------------------|
            |    (bx1, by1)        |
            |         |---|        |
            |         |   |        |
            |         |   |        |
            |         |   |        |
            |         |---|        |
            |          (bx2, by2)  |
            |                      |
            |----------------------| (px2, py2)
            
            """
            if bx1 <= px1:
                return False
            if bx2 >= px2:
                return False
            if by1 <= py1:
                return False
            if by2 >= py2:
                return False

            return True
        """
        (px1, py1)
        |----------------------|
        |                      |
        |               (bx1, by1)
        |                  |-------|
        |                  |       |
        |                  |       |
        |                  |       |
        |                  |       |
        |                  |       |
        |                  |-------|
        |                      |    (bx2, by2)
        |                      |
        |----------------------| (px2, py2)
        """

        if self.between(px1, px2, bx1) and self.between(py1, py2, by1):
            return True

        if self.between(px1, px2, bx1) and self.between(py1, py2, by2):
            return True

        if self.between(px1, px2, bx2) and self.between(py1, py2, by1):
            return True

        if self.between(px1, px2, bx2) and self.between(py1, py2, by2):
            return True

        return False
