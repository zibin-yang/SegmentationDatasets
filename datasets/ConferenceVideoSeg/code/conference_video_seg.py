

import numpy as np
import os
import torch.utils.data as data
from torchvision.transforms import ToTensor, Normalize
from PIL import Image
import torch

class ConfereceVideoSeg(data.Dataset):
    CLASSES = [
        'background', 'foreground'
    ]

    def __init__(self, root, train=True, transform=None):
        self.root = root
        _list_dir = os.path.join(self.root, 'segmentation')
        self.transform = transform
        self.train = train

        if self.train:
            _list_file = os.path.join(_list_dir, 'train.txt')
        else:
            _list_file = os.path.join(_list_dir, 'val.txt')

        self.images = []
        self.masks = []

        # Normalizations
        self.normalize = Normalize(mean=[0.485, 0.456, 0.406],
                                   std=[0.229, 0.224, 0.225])

        self.denormalize = Normalize(mean=[-0.485 / 0.229, -0.456 / 0.224, -0.406 / 0.225],
                                     std=[1 / 0.229, 1 / 0.224, 1 / 0.225])
        #
        with open(_list_file, 'r') as lines:
            for line in lines:
                _image = self.root + "/images/" + line.strip('\n') + ".jpg"
                _mask = self.root + "/masks/" + line.strip('\n') + "png"
                #
                assert os.path.isfile(_image)
                assert os.path.isfile(_mask)
                #
                self.images.append(_image)
                self.masks.append(_mask)

    def __getitem__(self, index):
        _img = Image.open(self.images[index]).convert('RGB')
        _img_origin = _img
        _target = Image.open(self.masks[index])

        if self.transform is not None:
            for augmentFun in self.transform:
                _img, _target = augmentFun(_img, _target)
        # base transform
        _img, _target = self._transform(_img, _target)

        #
        if self.train:
            return _img, _target
        else:
            _img_origin, _ = self._transform(_img_origin)
            return _img, _target, _img_origin, self.images[index].strip(self.root + "/images/")


    def __len__(self):
        return len(self.images)

    def _transform(self, image, label=None):
        """
           :param image: PIL image, (512, 512, 3)
           :param label: PIL image, (512, 512)
           :return:
           image: floatTensor, (3, 512, 512)
           label: longTensor, (512, 512)
        """
        # concat
        image = ToTensor()(image)

        # normalize
        image = self.normalize(image)

        if label is not None:
            label = torch.LongTensor(np.array(label))

        return image, label



if __name__ == "__main__":

    root = "../data/ConferenceVideoSegmentation"
    conferenceVideoSeg = ConfereceVideoSeg(root, train=True)

    for i in range(20):
        image, label  = conferenceVideoSeg[i]

        print("-----------[{}]-------".format(i))
        print("image.shape is {}".format(image.shape))
        print("label.shape is {}".format(label.shape))
        print("label unique is {}".format(np.unique(label)))
        print("")
