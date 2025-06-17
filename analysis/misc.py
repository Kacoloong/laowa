from typing import Annotated
BLOCK_SIZE = 2**6
NUM_SIZE = 2**8
FINAL_USE_SLICE = 4  # Each slice generates 16 byte digest.

HashValue = str
Message = tuple[int, ...]
MessageBlock = Annotated[tuple[int, ...], BLOCK_SIZE]

# --State Spec--
LANE_LENGTH = 8
ROW_LENGTH = 4
COLUMN_LENGTH = 4
SLICE_SIZE = ROW_LENGTH * COLUMN_LENGTH
SIZE = LANE_LENGTH * ROW_LENGTH * COLUMN_LENGTH



def get_id( z: int, y: int, x: int) -> int:
    return SLICE_SIZE * z + COLUMN_LENGTH * y + x

