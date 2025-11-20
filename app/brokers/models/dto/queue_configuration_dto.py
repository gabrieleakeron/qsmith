from pydantic import BaseModel


class QueueConfigurationDto(BaseModel):
    url: str
    fifoQueue: bool = False
    contentBasedDeduplication: bool = False
    defaultVisibilityTimeout: int = 30
    delay: int = 0
    receiveMessageWait: int = 0