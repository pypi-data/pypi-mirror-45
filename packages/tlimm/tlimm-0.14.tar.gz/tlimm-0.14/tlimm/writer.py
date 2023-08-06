import json
from pathlib import Path


class ImageAndAttributeWriter:
    def __init__(self, image_output_path, annotation_output_path):
        self.image_output_path = Path(image_output_path)
        self.annotation_output_path = Path(annotation_output_path)

        if not self.image_output_path.exists():
            self.image_output_path.mkdir(0o755, parents=True)

        if not self.annotation_output_path.exists():
            self.annotation_output_path.mkdir(0o755, parents=True)

    def write(self, image, box, label, name):
        img_name = '{}/{}.jpg'.format(self.image_output_path, name)
        annotation_name = '{}/{}.json'.format(self.annotation_output_path, name)
        image.save(img_name)
        obj = {"box": box, 'label': label}
        with open(annotation_name, 'w') as f:
            json.dump(obj, f)

