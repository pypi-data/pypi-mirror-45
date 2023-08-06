#
# Providing meaningful error codes
#


class ErrorCodesBPF2EAF:
    ERROR_CODE_NOT_ENOUGH_CMD_ARGUMENTS: int = 1  # 1 = not enough parameters specified on the command line
    ERROR_CODE_MAU_TIER_MISSING: int = 2  # 2 = MAU tier is missing from the BPF file (no timing information -> abort)
