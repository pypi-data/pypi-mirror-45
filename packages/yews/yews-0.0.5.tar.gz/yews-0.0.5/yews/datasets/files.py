import numpy as np

from .base import PathDataset

__all__ = [
    'FileDataset',
    'DatasetArray',
]


class FileDataset(PathDataset):
    """An abstract class representing a Dataset in a file.

    Args:
        path (object): File of the file.
        sample_transform (callable, optional): A function/transform that takes
            a sample and returns a transformed version.
        target_transform (callable, optional): A function/transform that takes
            a target and transform it.

    Attributes:
        samples (list): List of samples in the dataset.
        targets (list): List of targets in teh dataset.

    """

    def is_valid(self):
        return self.root.is_file()

    def handle_invalid(self):
        raise ValueError(f"{self.root} is not a file.")


class DatasetArray(FileDataset):
    """A generic data loader for ``.npy`` file where samples are arranged is
    the following way: ::

        array = [
            [sample0, target0],
            [sample1, target1],
            ...
        ]

    where both samples and targets can be arrays.

    Args:
        path (object): Path to the ``.npy`` file.
        sample_transform (callable, optional): A function/transform that takes
            a sample and returns a transformed version.
        target_transform (callable, optional): A function/transform that takes
            a target and transform it.

    Attributes:
        samples: List of samples in the dataset.
        targets: List of targets in teh dataset.

    """

    def build_dataset(self):
        """Returns samples and targets.

        """
        data = np.load(self.root, allow_pickle=True)
        return data[:, 0], data[:, 1]
