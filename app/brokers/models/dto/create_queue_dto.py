from pydantic import BaseModel


class CreateQueueDto(BaseModel):
    code: str
    description: str | None = None
    fifoQueue: bool = False
    contentBasedDeduplication: bool = False
    defaultVisibilityTimeout: int = 30
    delay: int = 0
    receiveMessageWait: int = 0