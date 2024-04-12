class PyRevealError(Exception):
    """Base exception for PyReveal."""

    pass


class InvalidThemeError(PyRevealError):
    """Raised when an invalid theme is set."""

    pass


class InvalidTransitionError(PyRevealError):
    """Raised when an invalid transition is set."""

    pass


class EmptySlideContentError(PyRevealError):
    """Raised when trying to add a slide with empty content."""

    pass


class SlideGroupNotFoundError(PyRevealError):
    """Raised when a slide is added to a non-existent group."""

    def __init__(self, group_name):
        super().__init__(f"Slide group '{group_name}' not found.")


class DuplicateSlideTitleError(PyRevealError):
    """Raised when two slides have the same title."""

    def __init__(self, title):
        super().__init__(
            f"Duplicate slide title '{title}' found. Slide titles must be unique."
        )
