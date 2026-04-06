import logging
import os


def get_root_logger():
    logger = logging.getLogger("basicsr")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def scandir(dir_path, suffix=None, recursive=False, full_path=False):
    for entry in os.scandir(dir_path):
        if entry.name.startswith("."):
            continue
        if entry.is_file():
            if suffix is None or entry.name.endswith(suffix):
                yield entry.path if full_path else entry.name
        elif recursive and entry.is_dir():
            yield from scandir(entry.path, suffix=suffix, recursive=True, full_path=full_path)
