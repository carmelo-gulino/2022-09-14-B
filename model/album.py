from dataclasses import dataclass


@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int
    d_media: float

    def __str__(self):
        return self.Title

    def __repr__(self):
        return self.Title

    def __hash__(self):
        return hash(self.AlbumId)
