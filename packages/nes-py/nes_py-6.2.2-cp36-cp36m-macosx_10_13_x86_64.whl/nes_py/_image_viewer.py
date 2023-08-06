"""A simple class for viewing images using pyglet."""
from pyglet.window import Window
from pyglet.image import ImageData


class ImageViewer(object):
    """A simple class for viewing images using pyglet."""

    def __init__(self, caption, height, width):
        """
        Initialize a new image viewer.

        Args:
            caption (str): the caption/title for the window
            height (int): the height of the window
            width (int): the width of the window

        Returns:
            None
        """
        self.caption = caption
        self.height = height
        self.width = width
        self._window = None

    def __repr__(self):
        """Return an executable string representing this object."""
        template = '{}(caption={}, height={}, width={})'
        return template.format(self.caption, self.height, self.width)

    def __del__(self):
        """Close any open windows and delete this object."""
        self.close()

    @property
    def is_open(self):
        """Return a boolean determining if this window is open."""
        return self._window is not None

    def open(self):
        """Open the window."""
        self._window = Window(
            caption=self.caption,
            height=self.height,
            width=self.width,
            vsync=False,
            resizable=True,
        )

    def show(self, frame):
        """
        Show an array of pixels on the window.

        Args:
            frame (numpy.ndarray): the frame to show on the window

        Returns:
            None
        """
        # check that the frame has the correct dimensions
        if len(frame.shape) != 3:
            raise ValueError('frame should have shape with only 3 dimensions')
        # open the window if it isn't open already
        if not self.is_open:
            self.open()
        # prepare the window for the next frame
        self._window.clear()
        self._window.switch_to()
        self._window.dispatch_events()
        # create an image data object
        image = ImageData(
            frame.shape[1],
            frame.shape[0],
            'RGB',
            frame.tobytes(),
            pitch=frame.shape[1]*-3
        )
        # send the image to the window
        image.blit(0, 0, width=self._window.width, height=self._window.height)
        self._window.flip()

    def close(self):
        """Close the window."""
        if self.is_open:
            self._window.close()
            self._window = None


# explicitly define the outward facing API of this module
__all__ = [ImageViewer.__name__]
