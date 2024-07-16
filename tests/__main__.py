import sys
import unittest

from loguru import logger

from tests.db.manga_notify.test_user_subscription_repository import (
    TestUserSubscriptionRepository,
)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserSubscriptionRepository)
    logger.debug(suite.countTestCases())
    runner = unittest.TextTestRunner(stream=sys.stderr, verbosity=2)
    runner.run(suite)
