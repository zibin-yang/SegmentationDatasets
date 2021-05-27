# Reconstruct the original dataset as the desired structure

import os
import shutil
from PIL import Image
import numpy as np

# return a list of file
def load_file_to_list(fileDir, listDir, listName) -> [] :
    assert os.path.isdir(fileDir)
    assert os.path.isdir(listDir)
    listFile = os.path.join(listDir, listName)

    print("reading filenames at {} to list {}".format(fileDir, listFile))
    # listdir does not sort according to filenames
    filenameList = sorted(os.listdir(fileDir))
    fileList = []
    #
    '''
    suffix = ""
    if filenameList[0].find('.jpg'):
        suffix = '.jpg'
    elif filenameList[0].find('.png'):
        suffix = '.png'
    '''
    #
    prevId = -1
    with open(listFile, 'w') as f:
        for i in range(0, len(filenameList)):
            suffix = filenameList[i].split('.')[1]
            if suffix not in ['jpg', 'png']:
                print("Info: [{}] {} is not a valid image, skip".format(i, filenameList[i]))
                continue
            id = filenameList[i].split('.')[0].strip('_Combine')
            if id != prevId:
                fileList.append(id)
                f.write('%s\n' % id)
                prevId = id
            #
    '''    
    fileList.sort()
    for i in range(1, len(fileList)):
        if fileList[i-1] == fileList[i]:
            print("Error! found duplicates {}[{}] {}[{}]".format(fileList[i-1], i-1, fileList[i], i))

    '''

    return fileList

def copy_helper_(imgDir, targetImgDir, targetMaskDir, imgList):

    assert os.path.isdir(imgDir)
    assert os.path.isdir(targetImgDir)
    assert os.path.isdir(targetMaskDir)
    #
    imgDupList = []
    maskDupList = []

    imgCounter_ = 0
    maskCounter_ = 0
    for id in imgList:
        # reconstruct filename for image and mask
        imgName = str(id) + '.jpg'
        maskName = str(id) + '.png'
        #
        targetImgFile = os.path.join(targetImgDir, imgName)
        targetMaskFile = os.path.join(targetMaskDir, maskName)
        # copy image file, skip if already in target directory
        if os.path.exists(targetImgFile):
            imgDupList.append(targetImgFile)
        else:
            imgFile = os.path.join(imgDir, imgName)
            #assert os.path.isfile(imgFile)
            if not os.path.isfile(imgFile):
                print("Error [{}] {} is not a valid image file.".format(imgCounter_, imgFile))
            else:
                shutil.copy(imgFile, targetImgDir)
                imgCounter_ += 1
        # copy mask file, skip if already in target directory
        if os.path.exists(targetMaskFile):
            maskDupList.append(targetMaskFile)
        else:
            maskFile = os.path.join(imgDir, maskName)
            #assert os.path.isfile(maskFile)
            if not os.path.isfile(maskFile):
                print("Error [{}] {} is not a valid image file.".format(imgCounter_, maskFile))
            else:
                shutil.copy(maskFile, targetMaskDir)
                maskCounter_ += 1


    print("{} images copied from {} to {} with {} skipped due to duplicates ".format(
        imgCounter_, imgDir, targetImgDir,len(imgDupList)))
    print("{} masks copied from {} to {} with {} skipped due to duplicates ".format(
        maskCounter_, imgDir, targetMaskDir,len(maskDupList)))


def copy_img_to_target(datasetDir, imgDir, maskDir, segDir, segFile):

    print(datasetDir)

    assert os.path.isdir(datasetDir)
    assert os.path.isdir(imgDir)
    assert os.path.isdir(maskDir)
    assert os.path.isdir(segDir)
    #assert os.path.isfile(segFile)

    print("copying both images and masks from {} to img:{} mask:{} and list them to {}".format(
        datasetDir, imgDir, maskDir, segDir
    ))
    #
    imgList = []
    if segFile == 'test.txt':
        originImgDir = datasetDir + '/face-3965'
        imgList = load_file_to_list(originImgDir, segDir, segFile)
        copy_helper_(originImgDir, imgDir, maskDir, imgList)
    elif segFile == 'train.txt':
        originImgDir = datasetDir + '/face-6046'
        imgList = load_file_to_list(originImgDir, segDir, segFile)
        copy_helper_(originImgDir, imgDir, maskDir, imgList)
    elif segFile == 'trainval.txt':
        #
        originImgDir = datasetDir + '/face-3965'
        imgList = load_file_to_list(originImgDir, segDir, segFile)
        copy_helper_(originImgDir, imgDir, maskDir, imgList)
        #
        originImgDir = datasetDir + '/face-6046'
        imgList = load_file_to_list(originImgDir, segDir, segFile)
        copy_helper_(originImgDir, imgDir, maskDir, imgList)
    else:
        print("segFile should be in [test.txt, train.txt, trainval.txt], not {}".format(segFile))
        return

def main():
    dataset_name = 'ClassinSeg'
    root = '../../' + dataset_name
    print(root)
    #
    dataset_dir = os.path.join(root, 'data/Classin_10011')
    #
    target_dataset_dir = os.path.join(root, 'data/ClassinSeg')
    target_images_dir = os.path.join(target_dataset_dir, 'images')
    target_masks_dir = os.path.join(target_dataset_dir, 'masks')
    target_segmentation_dir = os.path.join(target_dataset_dir, 'segmentation')
    print(target_images_dir)
    print(target_masks_dir)
    print(target_segmentation_dir)
    #
    print("Starting copy_img_to_target..")
    copy_img_to_target(dataset_dir, target_images_dir, target_masks_dir, target_segmentation_dir, 'train.txt')
    copy_img_to_target(dataset_dir, target_images_dir, target_masks_dir, target_segmentation_dir, 'test.txt')
    copy_img_to_target(dataset_dir, target_images_dir, target_masks_dir, target_segmentation_dir, 'trainval.txt')

if __name__ == "__main__":
    main()