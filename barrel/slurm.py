from enum import Enum

JobId = str


class JobStateCode(Enum):
    """Worker state."""

    BOOT_FAIL = 0
    CANCELLED = 1
    COMPLETED = 2
    CONFIGURING = 3
    COMPLETING = 4
    DEADLINE = 5
    FAILED = 6
    NODE_FAIL = 7
    OUT_OF_MEMORY = 8
    PENDING = 9
    PREEMPTED = 10
    RUNNING = 11
    RESV_DEL_HOLD = 12
    REQUEUE_FED = 13
    REQUEUE_HOLD = 14
    REQUEUED = 15
    RESIZING = 16
    REVOKED = 17
    SIGNALING = 18
    SPECIAL_EXIT = 19
    STAGE_OUT = 20
    STOPPED = 21
    SUSPENDED = 22
    TIMEOUT = 23
