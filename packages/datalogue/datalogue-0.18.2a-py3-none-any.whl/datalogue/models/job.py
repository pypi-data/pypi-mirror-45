from datetime import datetime
from uuid import UUID
from typing import Union
from dateutil.parser import parse

from datalogue.utils import SerializableStringEnum
from datalogue.errors import _enum_parse_error, DtlError


class JobStatus(SerializableStringEnum):
    Scheduled = "Scheduled"
    Defined = "Defined"
    Running = "Running"
    Succeeded = "Succeeded"
    Failed = "Failed"
    Unknown = "Unknown"

    @staticmethod
    def parse_error(s: str) -> str:
        return _enum_parse_error("job status", s)


def job_status_from_str(string: str) -> Union[DtlError, JobStatus]:
    return SerializableStringEnum.from_str(JobStatus)(string)


class Job:
    def __init__(self, run_at: datetime, status: JobStatus, stream_collection_id: UUID):
        self.stream_collection_id = stream_collection_id
        self.status = status
        self.run_at = run_at

    def __repr__(self):
        return f'{self.__class__.__name__}(stream_collection_id: {self.stream_collection_id!r}, status: {self.status!r}, ' \
               f'run_at: {self.run_at!r})'


def _job_from_payload(json: dict) -> Union[DtlError, Job]:
    run_at = json.get("runDate")
    if run_at is None:
        return DtlError("Job object should have a 'runDate' property")
    else:
        try:
            run_at = parse(run_at)
        except ValueError:
            return DtlError("The 'runDate' could not be parsed as a valid date")

    status = json.get("combinedStreamState")
    if status is None:
        return DtlError("Job object should have a 'combinedStreamState' property")
    else:
        status = job_status_from_str(status)
        if isinstance(status, DtlError):
            return status

    stream_collection_id = json.get("streamCollectionId")
    if stream_collection_id is None:
        return DtlError("Job object should have a 'streamCollectionId' property")
    else:
        try:
            stream_collection_id = UUID(stream_collection_id)
        except ValueError:
            return DtlError("'streamCollectionId' field was not a proper uuid")

    return Job(run_at, status, stream_collection_id)
