'''
Description:
A decorator class for OpenHTF test phases that prints a header and a result

Usage:

@TestPrinter()
def my_test_case(test):
    console_output.cli_print('Hello, World', logger=None)



Sample Output:

==================== 0001: my_test_case ===================

Hello, World
result: PASS

'''

from openhtf.util import console_output
import functools


class mem:
    '''
    An alternative to global variables
    '''
    pass


mem.test_printer_counter = 0


class TestPrinter():
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            mem.test_printer_counter += 1
            test_api = args[0]
            test_name = func.__name__

            # Print a banner. The test is about to begin
            console_output.banner_print(f'{mem.test_printer_counter:04}: {test_name}', logger=None)

            # And here's the test
            result = func(*args, **kwargs)

            # Check the result. Test phases do not need to return a result. In that
            # case, check for failed or unset measurements to determine pass or fail
            if not result:
                measurements = str(test_api.measurements)

                if "'FAIL'" in measurements or "'UNSET'" in measurements:
                    result_msg = "FAIL"

                else:
                    result_msg = "PASS"

            elif result.name == 'CONTINUE':
                result_msg = "PASS"

            elif result.name == 'SKIP':
                result_msg = "SKIP"

            else:
                result_msg = "FAIL"

            # Print the result
            console_output.cli_print(f"result: {result_msg}", logger=None)

            return result

        return wrapper
