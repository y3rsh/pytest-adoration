from typing import List, Optional
import uuid
from faker import Faker
from pydantic import BaseModel
from pydantic.types import SecretStr, UUID4


class User(BaseModel):
    """
    represent users for our application
    """

    id: UUID4 = uuid.uuid4()
    description: str
    meta_tags: List[str]
    permissions: List[dict]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    password: Optional[SecretStr]
    secret: Optional[SecretStr]

    @classmethod
    def fake(cls):
        """
        create a fake user
        """
        fake = Faker()
        profile = fake.simple_profile()
        return cls(
            description=fake.paragraph(nb_sentences=2),
            permissions=[fake.pydict(nb_elements=5) for _ in range(1, 10)],
            meta_tags=fake.words(unique=True),
            username=profile["username"],
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
