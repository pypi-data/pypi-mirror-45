import json
from PIL import Image


class ImageAndAttributeReader:
    def __init__(self, imgs, annotations):
        self.image_path = sorted(imgs)
        self.annotation_path = sorted(annotations)
        self.parse()

    def parse(self):
        for i, a in zip(self.image_path, self.annotation_path):
            boxes, labels = self.parse_annotation(a)
            image = Image.open(i)
            yield image, boxes, labels

    @staticmethod
    def parse_annotation(annotation):
        with open(annotation, 'r') as f:
            j = json.load(f)
        boxes = []
        labels = []
        for l in j['labels']:
            b = l['box2d']
            c = l['category']
            boxes.append([b['x1'], b['x2'], b['y1'], b['y2']])
            labels.append(c)
        return boxes, labels

