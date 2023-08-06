from pathlib import Path
from .process_image import Processor
from .reader import ImageAndAttributeReader
from .writer import ImageAndAttributeWriter


class Cut:
    def __init__(self,
                 image_input_dir,
                 annotation_input_dir,
                 image_output_dir,
                 annotation_output_dir,
                 size=(300, 300),
                 internal=True):
        self.image_input_dir = image_input_dir
        self.annotation_input_dir = annotation_input_dir
        self.image_output_dir = image_output_dir
        self.annotation_output_dir = annotation_output_dir

        self.size = size
        self.internal = internal
        self.load_materials()

    def load_materials(self):
        input_images = sorted(Path(self.image_input_dir).glob('*.jpg'))
        input_annotations = sorted(Path(self.annotation_input_dir).glob('*.json'))
        reader = ImageAndAttributeReader(input_images, input_annotations)
        writer = ImageAndAttributeWriter(self.image_output_dir, self.annotation_output_dir)

        for count, (image, boxes, labels) in enumerate(reader.parse()):
            p = Processor(image, boxes, labels, internal=True, cut_size=self.size)
            for count_in_image, (i, b, l) in enumerate(p.cut_image_with_info):
                filename = '{}-{}'.format(count, count_in_image)
                writer.write(i, b, l, filename)

                if count_in_image > 30:
                    break
            break


if __name__ == "__main__":
    # size = (1000, 1000)
    Cut(
        image_input_dir="./demo/imgs",
        annotation_input_dir="./demo/annotations",
        image_output_dir="./demo/output_imgs",
        annotation_output_dir="./demo/output_annotations",
    )
