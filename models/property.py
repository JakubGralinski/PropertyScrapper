from pydantic import BaseModel


class Property(BaseModel):
    """
    Represents the data structure of a Property.
    """

    name: str
    location: str
    price: str
    capacity: str
    rating: float
    reviews: int
    description: str
