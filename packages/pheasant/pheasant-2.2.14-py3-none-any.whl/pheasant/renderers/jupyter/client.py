"""A module provides jupyter client interface."""
import atexit
import datetime
import logging
import re
from typing import Any, Dict, Iterator, List, Optional

from jupyter_client.kernelspec import find_kernel_specs, get_kernel_spec
from jupyter_client.manager import KernelManager

from pheasant.core.base import format_timedelta
from pheasant.renderers.jupyter.progress import ProgressBar

logger = logging.getLogger("pheasant")

kernel_names: Dict[str, list] = {}
kernel_clients: Dict[str, Any] = {}
execution_report = {"page": datetime.timedelta(0), "total": datetime.timedelta(0)}


def find_kernel_names() -> Dict[str, list]:
    """Find kernel names for languages.

    Returns
    -------
    kernel_names
        dict of {language: list of kernel name}.
    """
    if kernel_names:
        return kernel_names

    kernel_specs = find_kernel_specs()
    for kernel_name in kernel_specs:
        kernel_spec = get_kernel_spec(kernel_name)
        language = kernel_spec.language
        if language not in kernel_names:
            kernel_names[language] = [kernel_name]
        else:
            kernel_names[language].append(kernel_name)

    return kernel_names


def get_kernel_name(language: str, index: int = 0) -> Optional[str]:
    """Select one kernel name for a language."""
    kernel_names = find_kernel_names()
    if language not in kernel_names:
        return None
    else:
        return kernel_names[language][index]


def start_kernel(
    kernel_name: str, init_code: str = "", timeout: int = 3, retry: int = 10
) -> None:
    if kernel_name in kernel_clients:
        return

    def start():
        kernel_manager = KernelManager(kernel_name=kernel_name)
        kernel_manager.start_kernel()
        kernel_client = kernel_manager.blocking_client()
        kernel_client.start_channels()
        try:
            kernel_client.execute_interactive(init_code, timeout=timeout)
        except TimeoutError:
            kernel_client.shutdown()
            return False
        else:

            def shutdown():  # pragma: no cover
                logger.info(f'Shutting down kernel: "{kernel_name}".')
                kernel_client.shutdown()

            atexit.register(shutdown)
            kernel_clients[kernel_name] = kernel_client
            return kernel_client

    progress_bar = ProgressBar(retry, init=f"Starting kernel: '{kernel_name}'")

    now = datetime.datetime.now()

    def message(result):
        dt = format_timedelta(datetime.datetime.now() - now)
        return f"Kernel Started ({dt})" if result else "Retrying"

    for k in range(retry):
        if progress_bar.progress(start, message):
            progress_bar.finish()
            break
    else:
        raise TimeoutError


def restart_kernel(kernel_name: str):
    if kernel_name in kernel_clients:
        del kernel_clients[kernel_name]
    kernel_manager = kernel_clients[kernel_name]
    kernel_manager.restart_kernel()


def get_kernel_client(kernel_name: str):
    if kernel_name in kernel_clients:
        return kernel_clients[kernel_name]

    start_kernel(kernel_name)
    return kernel_clients[kernel_name]


def execute(
    code: str, kernel_name: Optional[str] = None, language: str = "python"
) -> List:
    if kernel_name is None:
        kernel_name = get_kernel_name(language)
        if kernel_name is None:
            raise ValueError(f"No kernel found for language {language}.")

    kernel_client = get_kernel_client(kernel_name)

    outputs = []

    def output_hook(msg):
        output = output_from_msg(msg)
        if output:
            outputs.append(output)

    msg = kernel_client.execute_interactive(
        code, allow_stdin=False, output_hook=output_hook
    )

    create_execution_report(msg)
    return list(stream_joiner(outputs))


def create_execution_report(msg) -> None:
    start_time = msg["parent_header"]["date"].astimezone()
    end_time = msg["header"]["date"].astimezone()
    msg["parent_header"]["date"] = start_time
    msg["header"]["date"] = end_time
    execution_report["start"] = start_time
    execution_report["end"] = end_time
    execution_report["cell"] = end_time - start_time
    execution_report["page"] += execution_report["cell"]
    execution_report["total"] += execution_report["cell"]
    execution_report["execution_count"] = msg["content"]["execution_count"]
    execution_report["message"] = msg


def output_from_msg(msg) -> Optional[dict]:
    """Create an output dictionary from a kernel's IOPub message.

    Returns
    -------
    dict: the output as a dictionary.
    """
    msg_type = msg["msg_type"]
    content = msg["content"]

    if msg_type == "execute_result":
        return dict(type=msg_type, data=content["data"])
    elif msg_type == "display_data":
        return dict(type=msg_type, data=content["data"])
    elif msg_type == "stream":
        return dict(type=msg_type, name=content["name"], text=content["text"])
    elif msg_type == "error":
        traceback = "\n".join([strip_ansi(tr) for tr in content["traceback"][1:-1]])
        return dict(
            type=msg_type,
            ename=content["ename"],
            evalue=content["evalue"],
            traceback=traceback.strip(),
        )
    else:
        return None


def stream_joiner(outputs: List[Dict]) -> Iterator[Dict]:
    name = text = ""
    for output in outputs:
        if output["type"] != "stream":
            if text:
                yield stream_cell(name, text)
                name = text = ""
            yield output
            continue
        if not name:
            name = output["name"]
        if output["name"] == name:
            text += output["text"]
        else:
            yield stream_cell(name, text)
            name, text = output["name"], output["text"]
    if text:
        yield stream_cell(name, text)


def stream_cell(name: str, text: str) -> Dict[str, str]:
    if "\x08" in text:
        text, source = "", text
        index = 0
        for char in source:
            if char == "\x08":
                text = text[:-1]
            elif char == "\r":
                text = text[:index]
            elif char == "\n":
                text += char
                index = len(text)
            else:
                text += char
    return {"type": "stream", "name": name, "text": text.strip()}


# from nbconvert.filters.ansi
_ANSI_RE = re.compile("\x1b\\[(.*?)([@-~])")


def strip_ansi(source: str) -> str:
    """
    Remove ANSI escape codes from text.

    Parameters
    ----------
    source
        Source to remove the ANSI from
    """
    return _ANSI_RE.sub("", source)
