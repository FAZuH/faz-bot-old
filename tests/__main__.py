import unittest
import sys

from tests.db.manga_notify.test_chapter_repository import TestChapterRepository

from loguru import logger


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChapterRepository)
    logger.debug(suite.countTestCases())
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=2)
    runner.run(suite)
