# Reconstruct the original dataset as the desired structure

import os
import shutil

from pathlib import Path

def load_file_list(fileDir, listDir, listName):

    #print(fileDir)
    #print(listFile)
    assert os.path.isdir(fileDir)
    assert os.path.isdir(listDir)
    imgListfile = os.path.join(listDir, listName)

    print("Reading filenames from {}, and put them in {}".format(fileDir, imgListfile))

    if os.path.exists(imgListfile):
        print("file {} already exists, abort for now".format(imgListfile))
        return

    counter = 0
    #nameList = []
    idList = []
    #
    filenameList = os.listdir(fileDir)
    #
    idStart = filenameList[0].find('gt')
    if idStart == 0: # gt3_1.jpg
        idStart += 2 # len(gt)
    else:           # original3_1.jpg
        idStart = filenameList[0].find('original')
        idStart += 8 # len(original)

    print("idStart: {}".format(idStart))
    for filename in filenameList:
        id = filename[idStart: filename.find('.')]
        print(id)
        idList.append(id)
    #
    idList.sort()

    with open(imgListfile, 'w') as f:
        for id in idList:
            f.write('%s\n' % id)
            counter += 1

    print("load file list complete with len {}".format(counter))

def copy_img_to_target(imgDir, targetDir, listDir, listName):
    print("Moving images from {} to {}, referencing list {}".format(imgDir, targetDir, listName))
    nameList =[]

    #
    assert os.path.isdir(imgDir)
    assert os.path.isdir(targetDir)
    assert os.path.isdir(listDir)
    imgListfile = os.path.join(listDir, listName)
    #
    imgType = targetDir.find('mask')
    if imgType != -1:
        prefix = 'gt'
    else:# images
        prefix = 'original'

    counter = 0
    dupList = []
    with open(imgListfile, 'r') as lines:
        for line in lines:
            #print(line)
            imgName = prefix + line.strip('\n') + '.jpg'
            #print(imgName)


            # check if target image already in target dir
            # skip if already exists
            targetFile = os.path.join(targetDir, imgName)
            if os.path.exists(targetFile):
                dupList.append(targetFile)
                continue
            # find the original image file
            imgFile = os.path.join(imgDir, imgName)
            assert os.path.isfile(imgFile)
            #print(imgFile)

            shutil.copy(imgFile, targetDir)
            counter += 1

    print("{} images copied from {} to {}, skipped {}(image already exisits)".format(counter, imgDir, targetDir, len(dupList)))
    return counter


def main():
    dataset_name = 'ConferenceVideoSeg'
    root = '../../' + dataset_name + '/'
    print(root)

    # Load original dataset directories
    origin_dataset_dir = os.path.join(root, 'data/ConferenceVideoSegmentationDataset')
    print(origin_dataset_dir)

    origin_train_img_dir = os.path.join(origin_dataset_dir, 'original_training')
    origin_test_img_dir = os.path.join(origin_dataset_dir, 'original_testing')
    origin_train_mask_dir = os.path.join(origin_dataset_dir, 'ground_truth_training')
    origin_test_mask_dir = os.path.join(origin_dataset_dir, 'ground_truth_testing')


    # Create target dataset directories
    target_dataset_dir = os.path.join(root, 'data/target_dataset')
    target_images_dir = os.path.join(target_dataset_dir, 'images')
    target_masks_dir = os.path.join(target_dataset_dir, 'masks')
    target_segmentation_dir = os.path.join(target_dataset_dir, 'segmentation')

    '''
    Path(target_dataset_dir).mkdir(parents=True, exist_ok=True)
    Path(target_images_dir).mkdir(parents=True, exist_ok=True)
    Path(target_masks_dir).mkdir(parents=True, exist_ok=True)
    Path(target_segmentation_dir).mkdir(parents=True, exist_ok=True)
    '''
    #load_file_list(origin_test_img_dir, os.path.join(target_segmentation_dir, 'test.txt'))
    #load_file_list(origin_train_img_dir, os.path.join(target_segmentation_dir, 'train.txt'))
    load_file_list(origin_test_img_dir, target_segmentation_dir, 'test.txt')
    load_file_list(origin_train_img_dir, target_segmentation_dir, 'train.txt')

    # testing
    copy_img_to_target(origin_test_img_dir, target_images_dir, target_segmentation_dir, 'test.txt')
    copy_img_to_target(origin_test_mask_dir, target_masks_dir, target_segmentation_dir, 'test.txt')
    # training
    copy_img_to_target(origin_train_img_dir, target_images_dir, target_segmentation_dir, 'train.txt')
    copy_img_to_target(origin_train_mask_dir, target_masks_dir, target_segmentation_dir, 'train.txt')

if __name__ == "__main__":
    main()