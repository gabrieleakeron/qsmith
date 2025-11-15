from pydantic import BaseModel

class QueueDto(BaseModel):
    id:str|None = None
    code:str
    broker_id:str
    url:str
    fifoQueue:bool = False
    contentBasedDeduplication: bool = False
    defaultVisibilityTimeout:int = 30
    delay:int = 0
    receiveMessageWait:int = 0
