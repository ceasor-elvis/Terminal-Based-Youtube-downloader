from pydantic import BaseModel, AnyUrl

class Input_data(BaseModel):
    urls: AnyUrl | None = None