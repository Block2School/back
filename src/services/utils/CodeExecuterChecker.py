from typing import NamedTuple

class CodeExecuterCheckerResult(NamedTuple):
    safe: bool
    reason: str
    logOutput: str

ban_list = [
    "rm",
    "sudo",
    "chmod",
    "touch",
    "mv",
    "system",
    "subprocess",
    "execve"
]

class CodeExecuterChecker:
    @staticmethod
    def check_code(code: str, user_uuid: str) -> dict:
        if code is None:
            return CodeExecuterCheckerResult(
                safe=True,
                reason="No code provided",
                logOutput=f"[{user_uuid}] No code provided"
            )

        # check if the code contains any banned keywords
        for banned_word in ban_list:
            if banned_word in code:
                return CodeExecuterCheckerResult(
                    safe=False,
                    reason=f"Code contains banned keyword: {banned_word}",
                    logOutput=f"[{user_uuid}] Code contains banned keyword: {banned_word}"
                )
        return CodeExecuterCheckerResult(
            safe=True,
            reason="Code is safe",
            logOutput=f"[{user_uuid}] Code is safe"
        )