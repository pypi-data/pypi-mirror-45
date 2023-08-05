class BaseTransform(object):
    """An abstract class representing a Transform.

    All other transform should subclass it. All subclasses should override
    ``__call__`` which performs the transform.

    """

    def __call__(self, data):
        raise NotImplementedError

    def __repr__(self):
        head = self.__class__.__name__
        content = [f"{key} = {val}" for key, val in self.__dict__.items()]
        body = ", ".join(content)
        return f"{head}({body})"


class Compose(BaseTransform):
    """Composes several transforms together.

    Args:
        transforms (list of ``Transform`` objects): list of transforms to compose.
    Example:
        >>> transforms.Compose([
        >>>     transforms.ZeroMean(),
        >>>     transforms.ToTensor(),
        >>> ])

    """

    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, wav):
        for t in self.transforms:
            wav = t(wav)
        return wav

    def __repr__(self):
        format_string = self.__class__.__name__ + '('
        for t in self.transforms:
            format_string += '\n'
            format_string += '    {0}'.format(t)
        format_string += '\n)'
        return format_string
