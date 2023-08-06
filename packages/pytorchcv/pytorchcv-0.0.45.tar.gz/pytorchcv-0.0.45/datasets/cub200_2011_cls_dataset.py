"""
    CUB-200-2011 dataset.
"""

import os
import numpy as np
import pandas as pd
from PIL import Image
import torch.utils.data as data


class CUB200_2011(data.Dataset):
    """
    Load the CUB-200-2011 classification dataset.

    Refer to :doc:`../build/examples_datasets/imagenet` for the description of
    this dataset and how to prepare it.

    Parameters
    ----------
    root : str, default '~/.torch/datasets/CUB_200_2011'
        Path to the folder stored the dataset.
    train : bool, default True
        Whether to load the training or validation set.
    transform : function, default None
        A function that takes data and transforms it.
    target_transform : function, default None
        A function that takes label and transforms it.
    """
    def __init__(self,
                 root=os.path.join("~", ".torch", "datasets", "CUB_200_2011"),
                 train=True,
                 transform=None,
                 target_transform=None):
        super(CUB200_2011, self).__init__()

        root_dir_path = os.path.expanduser(root)
        assert os.path.exists(root_dir_path)

        images_file_name = "images.txt"
        images_file_path = os.path.join(root_dir_path, images_file_name)
        if not os.path.exists(images_file_path):
            raise Exception("Images file doesn't exist: {}".format(images_file_name))

        class_file_name = "image_class_labels.txt"
        class_file_path = os.path.join(root_dir_path, class_file_name)
        if not os.path.exists(class_file_path):
            raise Exception("Image class file doesn't exist: {}".format(class_file_name))

        split_file_name = "train_test_split.txt"
        split_file_path = os.path.join(root_dir_path, split_file_name)
        if not os.path.exists(split_file_path):
            raise Exception("Split file doesn't exist: {}".format(split_file_name))

        images_df = pd.read_csv(
            images_file_path,
            sep="\s+",
            header=None,
            index_col=False,
            names=["image_id", "image_path"],
            dtype={"image_id": np.int32, "image_path": np.unicode})
        class_df = pd.read_csv(
            class_file_path,
            sep="\s+",
            header=None,
            index_col=False,
            names=["image_id", "class_id"],
            dtype={"image_id": np.int32, "class_id": np.uint8})
        split_df = pd.read_csv(
            split_file_path,
            sep="\s+",
            header=None,
            index_col=False,
            names=["image_id", "split_flag"],
            dtype={"image_id": np.int32, "split_flag": np.uint8})
        df = images_df.join(class_df, rsuffix="_class_df").join(split_df, rsuffix="_split_df")
        split_flag = 1 if train else 0
        subset_df = df[df.split_flag == split_flag]

        self.image_ids = subset_df["image_id"].values.astype(np.int32)
        self.class_ids = subset_df["class_id"].values.astype(np.int32) - 1
        self.image_file_names = subset_df["image_path"].values.astype(np.unicode)

        images_dir_name = "images"
        self.images_dir_path = os.path.join(root_dir_path, images_dir_name)
        assert os.path.exists(self.images_dir_path)

        self._transform = transform
        self._target_transform = target_transform

    def __getitem__(self, index):
        image_file_name = self.image_file_names[index]
        image_file_path = os.path.join(self.images_dir_path, image_file_name)
        img = Image.open(image_file_path).convert("RGB")
        label = int(self.class_ids[index])

        if self._transform is not None:
            img = self._transform(img)
        if self._target_transform is not None:
            label = self._target_transform(label)

        return img, label

    def __len__(self):
        return len(self.image_ids)
