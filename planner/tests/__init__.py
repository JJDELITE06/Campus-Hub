# planner/tests/ -- our automated UNIT TESTS, one file per build step.
#
# RUN ALL OF THEM:        python manage.py test
# RUN ONE FILE:           python manage.py test planner.tests.test_step04_factory
#
# HOW A TEST WORKS:
#   * A test class inherits from TestCase. Every method whose name starts
#     with "test_" is one test.
#   * Django creates an EMPTY, temporary database for the tests and throws it
#     away afterwards, so tests never touch your real db.sqlite3.
#   * Each test follows three steps:  ARRANGE (set things up),
#     ACT (do the thing), ASSERT (check the result).
#   * assertEqual(a, b) passes when a equals b. assertTrue(x) passes when x
#     is True. If an assert fails, the test fails and tells you the line.
#
# RULE FOR THE TEAM: when you add a class, add its tests in the same pull
# request, and run ALL the tests before you push. If they are all "OK",
# you did not break anybody else's work.
