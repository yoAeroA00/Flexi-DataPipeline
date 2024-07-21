from typing import Optional
from dataclasses import dataclass

@dataclass
class Processed(repr=False, eq=False, match_args=False):
    userId: str
    timeStamp: str
    OriginalFileName: str
    OriginalFileFormat: str
    OriginalFileContent: str
    ProcessedOCRText: Optional[str] = None
    ProcessedLLMCompletion: Optional[str] = None
    ProcessedJSON: Optional[dict] = None
