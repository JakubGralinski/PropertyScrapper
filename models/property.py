from pydantic import BaseModel


class Property(BaseModel):
    """
    Represents the data structure of a Property.
    """

    name: str
    location: str
    price: str
    description: str