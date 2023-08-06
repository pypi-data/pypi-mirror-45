# tlimm
Too Large Image for My Model

## purpose
Object Detection Algorithms sometimes cannot recognize some small pieces.  
There might be some solutions, though I don't know well...

By using this codes, you can crop the images with annotations.
It leads increasing your data, and the reducing the computing resources.

## install
```bash
pip install tlimm
```

## requirements
- pillow
- numpy


# usage

```python
import tlimm

width, height = 100, 50
tlimm.Cut(
    image_input_dir="./input_img_path",
    annotation_input_dir="./input_annotation_path",
    image_output_dir="./output_img_path",
    annotation_output_dir="./output_annotation_path",
    size=(width, height),
    internal=True,
)
``` 

This Library will crop the given image in two ways.
First Crop
![First Crop](imgs/description_1.png)

Second Crop
![Second Crop](imgs/description_2.png)

# args
### image_input_dir
the image you want to crop.
the Image should be jpg, in current version.

### annotation input dir
corresponding annotation to the above image.
the format MUST BE json.
See the example shown below.

### image_output_dir
the output directory you want to export the images

### annotation_output_dir
the output directory you want to export the annotations

### size
Cropping size.
Should be tuple with `(height, width)`

### internal
See the figures shown below or `in_cur_picture` method in `process_image.py`.

Red Boxes are regarded as corresponding annotation.
If internal is settled True:
![Internal_True](imgs/internal_true.png)

If internal is settled False:
![Internal_False](imgs/internal_false.png)




## CAUTION
currently, the supported annotation type is strictly limited.
I will support more types in the future, though not yet.

# supported annotation data type
The Annotation file has some limitations.
It should be json, and the file name should be pair with the image name.
Just change the extension name from jpg to json.
the json should be like 
```javascript
{
  {
    "category": 1, 
    "box2d": {
      "x1": 1, 
      "x2": 2, 
      "y1": 1, 
      "y2": 2
    }
  }
}
```

output annotation file is has same format as the input json.
Though, the coordinates in `box2d` is suited for the generated image.

In the future, I'm planning to support COCO, and VOC data formats.

# LICENSE
MIT License.
See detail for the license tab.
I do not fix anything from the github's original license.


 
