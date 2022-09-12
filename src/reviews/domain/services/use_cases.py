import uuid
from datetime import datetime
from typing import Union, List
from pathlib import Path

from domain.commands.create_videoclip import CreateVideoclip
from domain.commands.post_review import PostReview
from domain.model.videoclip import Videoclip
from domain.model.review import Review
from domain.services.errors import VideoclipNotFound
from domain.queries.download_videoclip import DownloadVideoclip
from domain.queries.get_reviews import GetReviews
from domain.queries.get_videoclips import GetVideoclips
from util.hash_id import convert_uuid_to_hashid


Result = Union[Videoclip, List[Videoclip], Review, List[Review], VideoclipNotFound]


def create_videoclip_use_case(command: CreateVideoclip, *args, **kwargs) -> Videoclip:
    id = uuid.uuid4()
    hash_id = convert_uuid_to_hashid(id)

    suffix = Path(command.filename).suffix
    destination = kwargs["file_uploader"].upload(command.file, f"{hash_id}{suffix}")

    videoclip = Videoclip(
        id=id,
        name=command.filename,
        filepath=destination,
        uploaded=datetime.now(),
        hash_id=hash_id,
        author_id=command.user.id,
    )
    kwargs["videoclip_repository"].create(videoclip)

    return videoclip


def post_review_use_case(command: PostReview, *args, **kwargs) -> Result:
    videoclip: Videoclip = kwargs["videoclip_repository"].get_one(command.videoclip_id)

    if videoclip is None:
        return VideoclipNotFound(command.videoclip_id)

    id = uuid.uuid4()
    hash_id = convert_uuid_to_hashid(id)

    suffix = Path(command.filename).suffix
    destination = kwargs["file_uploader"].upload(command.image, f"{hash_id}{suffix}")

    review = Review(
        id=id,
        imagepath=destination,
        text=command.text,
        published=datetime.now(),
        hash_id=hash_id,
        videoclip_id=videoclip.id,
        author_id=command.user.id,
    )
    videoclip.add_review(review, kwargs["review_repository"])
    return review


def get_reviews_use_case(query: GetReviews, *args, **kwargs) -> List[Review]:
    reviews: List[Review] = [
        review
        for review in kwargs["review_repository"].get_all()
        if review.videoclip_id == query.videoclip_id
    ]
    return reviews


def download_videoclip_use_case(query: DownloadVideoclip, *args, **kwargs) -> Result:
    videoclip: Videoclip = kwargs["videoclip_repository"].get_one(query.videoclip_id)

    if videoclip is None:
        return VideoclipNotFound(query.videoclip_id)

    return videoclip


def get_videoclips_use_case(query: GetVideoclips, *args, **kwargs) -> List[Videoclip]:
    videoclips: List[Videoclip] = kwargs["videoclip_repository"].get_all()

    return videoclips