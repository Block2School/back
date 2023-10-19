import logging
from fastapi import Request
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("graylog_logger")

prod = "production," if os.getenv("MODE") == "production" else "local,"

class Log():
    @staticmethod
    def login_log(req: Request, wallet: str, failed: bool = True, banned: bool = False):
        extradict = {
            "wallet": wallet,
            "tags": f"{prod}back,login",
            "ip": req.client.host
        }
        if banned:
            logger.info(f"Banned user tried to log in ({wallet})", extra=extradict)
        if failed:
            logger.warning(f"Login failed for {wallet}", extra=extradict)
        else:
            logger.info(f"Login successful for {wallet}", extra=extradict)

    @staticmethod
    def register_log(req: Request, wallet: str):
        extradict = {
            "wallet": wallet,
            "tags": f"{prod}back,login",
            "ip": req.client.host
        }
        logger.info(f"A new account is registered: {wallet}", extra=extradict)

    @staticmethod
    def error_log(tag: str, near: str, function: str, exception: str = None, is_critical: bool = False):
        extradict = {
            "tags": f"{prod}back,error,{tag}",
            "function": function,
            "error_log": exception
        }
        if not is_critical:
            logger.exception(f"An error occured near {near}", extra=extradict)
        else:
            logger.critical(f"A critical error occured near {near}", extra=extradict)

    @staticmethod
    def route_log(request: Request, tag: str, uuid: str):
        extradict = {
            "tags": f"{prod}back,routing,{tag}",
            "uuid": uuid if uuid != "open_route" else None,
            "url": str(request.url),
            "method": str(request.method),
            "headers": str(request.headers)
        }
        if uuid != "open_route":
            logger.info(f"User {uuid} accessed to {str(request.url)}", extra=extradict)
        else:
            logger.info(f"A user accessed to {str(request.url)}", extra=extradict)

    @staticmethod
    def warning_log(where: str, what: str):
        extradict = {
            "tags": f"{prod}back,warning",
            "where": where,
            "what": what
        }
        logger.warning(f"{what} in {where}", extra=extradict)

    @staticmethod
    def jwt_log(request: Request, uuid: str = None, admin_checker: bool = False):
        extradict = {
            "tags": f"{prod}back,login",
            "uuid": uuid,
            "ip": request.client.host,
            "url": str(request.url),
            "method": str(request.method),
            "headers": str(request.headers)
        }
        if admin_checker:
            if uuid:
                logger.warning(f"{uuid} tried to reach a moderation route", extra=extradict)
            else:
                logger.warning("Somebody tried to reach a moderation route", extra=extradict)
        else:
            if not uuid:
                logger.warning("Somebody tried to reach a protected route with a fake token", extra=extradict)