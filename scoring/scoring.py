from __future__ import annotations

import hashlib
import logging
from typing import List, Optional


logger = logging.getLogger(__name__)


def get_score(
    phone: Optional[str] = None,
    email: Optional[str] = None,
    birthday: Optional[str] = None,
    gender: Optional[int] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> int:

    fields = [phone, email, birthday, gender, first_name, last_name]
    filled = sum(1 for f in fields if f is not None)
    score = filled * 5

    logger.info("Score calculated: %d (filled fields: %d)", score, filled)
    return score


def get_interests(client_id: str) -> List[str]:

    h = hashlib.sha256(client_id.encode("utf-8")).hexdigest()

    choices = [
        "books", "music", "sports", "tech", "food", "travel", "art", "games",
    ]
    idx = int(h[:8], 16) % len(choices)
    interests = [choices[(idx + i) % len(choices)] for i in range(3)]

    logger.info("Interests returned for client %s: %s", client_id, interests)
    return interests
