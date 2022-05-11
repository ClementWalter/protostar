import queue
from logging import Logger
from typing import TYPE_CHECKING, Any, cast

from tqdm import tqdm as bar

from src.commands.test.test_cases import BrokenTestSuite
from src.commands.test.test_results_queue import TestResultsQueue
from src.commands.test.testing_summary import TestingSummary

if TYPE_CHECKING:
    from src.commands.test.test_collector import TestCollector


class TestingLiveLogger:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    def log(
        self,
        test_results_queue: TestResultsQueue,
        test_collector_result: "TestCollector.Result",
    ):
        testing_summary = TestingSummary([])

        try:
            with bar(
                total=test_collector_result.test_cases_count,
                bar_format="{l_bar}{bar}[{n_fmt}/{total_fmt}]",
                dynamic_ncols=True,
            ) as progress_bar:
                tests_left_n = test_collector_result.test_cases_count
                progress_bar.update()
                try:
                    while tests_left_n > 0:
                        (test_suite, test_case_result) = test_results_queue.get()
                        testing_summary.extend([test_case_result])
                        cast(Any, progress_bar).colour = (
                            "RED"
                            if len(testing_summary.failed) + len(testing_summary.broken)
                            > 0
                            else "GREEN"
                        )
                        progress_bar.write(str(test_case_result))

                        if isinstance(test_case_result, BrokenTestSuite):
                            tests_in_case_count = len(test_suite.test_functions)
                            progress_bar.update(tests_in_case_count)
                            tests_left_n -= tests_in_case_count
                        else:
                            progress_bar.update(1)
                            tests_left_n -= 1
                finally:
                    progress_bar.bar_format = "{desc}"
                    progress_bar.update()
                    testing_summary.log(
                        logger=self._logger,
                        collected_test_cases_count=test_collector_result.test_cases_count,
                        collected_test_suites_count=len(
                            test_collector_result.test_suites
                        ),
                    )

        except queue.Empty:
            # https://docs.python.org/3/library/queue.html#queue.Queue.get
            # We skip it to prevent deadlock, but this error should never happen
            pass
