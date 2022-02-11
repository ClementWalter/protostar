from pathlib import Path
from re import Pattern
from typing import Optional, List

from src.commands.test.runner import TestRunner
from src.commands.test.utils import collect_subdirectories


async def run_test_runner(
    sources_directory: Path,
    omit: Optional[Pattern] = None,
    match: Optional[Pattern] = None,
    cairo_paths: Optional[List[Path]] = None,
    cairo_paths_recursive: Optional[List[Path]] = None,
):
    cairo_path = [
        *(cairo_paths or []),
        *(
            [
                s
                for path_recursive in cairo_paths_recursive or []
                for s in collect_subdirectories(path_recursive)
            ]
        ),
    ]

    test_root_dir = Path(sources_directory)
    runner = TestRunner(include_paths=cairo_path)
    await runner.run_tests_in(
        test_root_dir,
        omit_pattern=omit,
        match_pattern=match,
    )