# SegmentationDatasets

This Project Aims to provide an example of constructing a Dataset for Training and Validating Algorithms for Video Object Segmentation.

The structure of the project follows the popular Pascal VOC Dataset (http://host.robots.ox.ac.uk/pascal/VOC/voc2012/)

The structure of the Dataset is as follows:
Structures:


	VidConData
		|	
		|----Main:
		|		|	
		|		|------person_train.txt
		|		|------person_trainval.txt
		|
		|----Annotations:
		|		|
		|		|-----2008__000213.xml
		|		|-----2008__000215.xml
		|		|-----2008__000217.xml
		|
		|----ImageSet:
		|		|
		|		|-----2008__000213.jpg
		|		|-----2008__000215.jpg
		|		|-----2008__000217.jpg
		|
		|----Segmented:
				|
				|-----2008__000213.png
				|-----2008__000215.png
				|-----2008__000217.png

The person_train.txt and person_trainval.txt contains the filename of the specific images.
For example, for image with name "2008__00213", without the file extension, points to the 
    
    1. annotation xml file under Annotations folder       
                    : 2008__000213.xml

    2. original .jpg image under ImageSet folder          
                    : 2008__000213.jpg

    3. the labeled/segmented ground truth .png image under Segmented folder    
                    : 2008__000213.png     

The Segmented ground truth image is pixel-level labeled with foreground and background,
with foreground being the human portion and background being the rest of the image.

The exact coloring of the segmented foreground and background is not strictly specified, but should be consistent throughout the whole dataset.