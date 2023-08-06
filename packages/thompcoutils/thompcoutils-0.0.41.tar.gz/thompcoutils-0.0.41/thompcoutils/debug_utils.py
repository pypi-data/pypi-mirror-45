from functools import partial


def assert_test(value, message, error=None, passed=None):
    if message is not None:
        print(message, end="...")
    if value:
        if passed is None:
            print("passed")
        else:
            print(passed)
    else:
        if error is None:
            print("FAILED!!")
        else:
            print(error)
        assert False


def exception_test(throws, message,  method_to_test):
    print(message, end="...")
    try:
        method_to_test
        if throws:
            raise Exception("this should fail")
    except Exception as e:
        if not throws:
            raise e
    print("passed")


def _test(throws, second):
    if throws:
        raise Exception("Throws")
    else:
        print(second)


def main():
    exception_test(True, "testing - should throw", partial(_test, True, "hello"))
    exception_test(False, "testing - should NOT throw",  partial(_test, False, "hello"))
    exception_test(True, "testing - should throw", partial(_test, throws=True, second="hello"))
    exception_test(False, "testing - should NOT throw",  partial(_test, False, "hello"))
    assert_test(True, "just some testing 0")
    assert_test(True, "just some testing 1", "error occurred 1")
    assert_test(True, "just some testing 2", "error occurred 2", "this passed 2")
    # assert_test(False, "error occurred 3")
    # assert_test(False, "just some testing 4", "error occurred 4")
    # assert_test(False, "just some testing 5", "error occurred 5", "this passed 5")

if __name__ == '__main__':
    main()
