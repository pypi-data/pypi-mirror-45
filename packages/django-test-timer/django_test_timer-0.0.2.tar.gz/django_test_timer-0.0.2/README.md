# django-test-timer

Print the amount of time that each unit test took. 

Tested with Django 1.11, Python 2.7

## Install

`pip install django-test-timer`

Then in your Django settings

```python
TEST_RUNNER = 'django_test_timer.TimedTestRunner'
```

Then run your tests as usual.

## Settings

By default, all tests will be printed. To only print tests that take a certain amount of time, set the threshold in your settings.py

```python
TIMED_TEST_THRESHOLD_SECS = 2.0
```

## Example Output

```
>>> ./manage.py test
....
----------------------------------------------------------------------
Ran 5 tests

Tests Times (>0.0s):
  [2.09s] test_foo (main.tests.test_general.DemoTestCase)
  [1.004s] test_bar (main.tests.test_general.DemoTestCase)
  [0.0s] test_this (main.tests.test_general.DemoTestCase)
  [0.0s] test_that (main.tests.test_general.DemoTestCase)
  [0.0s] test_not_implemented_errors (main.tests.test_general.DemoTestCase)
  
  Destroying test database for alias 'default'...
  ```
