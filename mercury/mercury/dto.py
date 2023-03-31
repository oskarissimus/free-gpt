from typing import Optional

from pydantic import BaseModel


class CodeExecutionDTO(BaseModel):
    code: str
    output: str
    error_output: str
    timestamp: Optional[str] = None

    @classmethod
    def from_channels_tuple_and_code(cls, channels_tuple, code: str):
        stdin, stdout, stderr = channels_tuple
        return cls(
            code=code,
            output=stdout.read().decode("utf-8"),
            error_output=stderr.read().decode("utf-8"),
        )

    @classmethod
    def from_bigquery_row(cls, row):
        return cls(
            code=row["input"],
            output=row["output"],
            error_output=row["error_output"],
            timestamp=str(row["timestamp"]),
        )

    def __str__(self):
        return f"""=> Input: {self.code}
=> Output: {self.output}
=> Error output: {self.error_output}
=> Timestamp: {self.timestamp}"""

    def __repr__(self):
        return self.__str__()
