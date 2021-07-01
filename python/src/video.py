"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)
        self._flag_reason = ""
        self._is_flagged = False

    def printout(self):
            print(f"{self.title} ({self.video_id}) [", end='')
            for tag in self.tags:
                if tag == self.tags[-1]:
                    print(tag, end="")
                else:
                    print(tag, end=" ")
            print("]", end='')

    def flag(self, flag_reason=""):
        self._flag_reason = flag_reason
        self._is_flagged = True

    def allow(self):
        self._flag_reason = ""
        self._is_flagged = False

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def flag_reason(self) -> str:
        """Returns the list of flags of a video"""
        if self._flag_reason == "":
            return "Not supplied"
        else:
            return self._flag_reason

    @property
    def is_flagged(self) -> str:
        """Returns the list of flags of a video"""
        return self._is_flagged