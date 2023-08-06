from . import process_image
from . import reader
from . import writer
from . import tlimm


class Cut(tlimm.Cut):
    def __init__(self,
                 image_input_dir,
                 annotation_input_dir,
                 image_output_dir,
                 annotation_output_dir,
                 size=(300, 300),
                 internal=True):
        super().__init__(image_input_dir,
                         annotation_input_dir,
                         image_output_dir,
                         annotation_output_dir,
                         size=(300, 300),
                         internal=True)

