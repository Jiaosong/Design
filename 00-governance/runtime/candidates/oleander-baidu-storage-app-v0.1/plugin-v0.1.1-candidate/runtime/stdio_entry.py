import logging

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

from app.server import mcp


if __name__ == "__main__":
    mcp.run(transport="stdio")
