import logging
import os
from dataclasses import field
from typing import Dict, Iterable, List

from pheasant.core.converter import Converter
from pheasant.core.decorator import Decorator, monitor
from pheasant.core.page import Page
from pheasant.renderers.embed.embed import Embed
from pheasant.renderers.jupyter.jupyter import Jupyter
from pheasant.renderers.number.number import Anchor, Header
from pheasant.renderers.script.script import Script

logger = logging.getLogger("pheasant")


class Pheasant(Converter):
    script: Script = field(default_factory=Script, init=False)
    jupyter: Jupyter = field(default_factory=Jupyter, init=False)
    header: Header = field(default_factory=Header, init=False)
    embed: Embed = field(default_factory=Embed, init=False)
    anchor: Anchor = field(default_factory=Anchor, init=False)
    decorator: Decorator = field(default_factory=Decorator, init=False)
    pages: Dict[str, Page] = field(default_factory=dict, init=False)

    def init(self):
        self.anchor.header = self.header
        self.register("script", [self.script])
        self.register("main", [self.header, self.jupyter, self.embed])
        self.register("link", [self.anchor])

        self.decorator.name = "pheasant"
        self.decorator.register("surround", [self.header, self.jupyter, self.embed])

    @monitor(format=True)
    def convert_from_files(self, paths: Iterable[str]) -> List[str]:
        paths = list(paths)
        logger.info("Pheasant converter resetting...")
        self.reset()
        logger.info("Done. Start conversion of each page.")
        for path in paths:
            logger.info(f"Converting: {os.path.relpath(path)}")
            if path.endswith(".py"):
                self.convert_from_file(path, "script", copy=True)
            self.convert_from_file(
                path, "main", copy=True, preprocess=self.jupyter.reset_source
            )
            self.jupyter.progress_bar.finish()
            self.pages[path].meta["extra_html"] = self.jupyter.extra_html

        self.jupyter.dump()

        for path in paths:
            self.convert_from_file(path, "link")

        return [self.pages[path].output for path in paths]
