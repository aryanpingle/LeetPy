from typing import TypedDict, List


class QuestionMetadata(TypedDict):
    difficulty: str
    id: int
    is_paid_only: bool
    title: str
    title_slug: str
    topics: List[str]
    description: str
