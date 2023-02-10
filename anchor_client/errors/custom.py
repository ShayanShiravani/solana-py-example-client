import typing
from anchorpy.error import ProgramError


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "You are not authorized to perform this action.")

    code = 6000
    name = "Unauthorized"
    msg = "You are not authorized to perform this action."


class CannotGetBump(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Cannot get the bump.")

    code = 6001
    name = "CannotGetBump"
    msg = "Cannot get the bump."


CustomError = typing.Union[Unauthorized, CannotGetBump]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: Unauthorized(),
    6001: CannotGetBump(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
