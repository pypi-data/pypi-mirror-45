class DebugException(Exception):
    pass


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


def exception_test(message,  exception, method_to_test, **kwargs):
    print(message, end="...")
    try:
        method_to_test(**kwargs)
        raise DebugException("this should fail")
    except exception as e:
        if isinstance(e, DebugException):
            raise e
        pass
    print("passed")


def _test(throws, ex, info):
    if throws:
        raise ex("Throws")
    else:
        print(info)


class TestException(Exception):
    def __init__(self, message="Test Exception", errors=None):
        super().__init__(message)
        self.errors = errors


def main():
    exception_test("testing - should throw 0", Exception, _test, throws=True, ex=Exception, info="hello")
    try:
        exception_test("testing - should not throw 1", TestException, _test, throws=False, ex=TestException,
                       info="hello")
        raise Exception("this should not pass!")
    except DebugException:
        pass
    assert_test(True, "just some testing 0")
    assert_test(True, "just some testing 1", "error occurred 1")
    assert_test(True, "just some testing 2", "error occurred 2", "this passed 2")
    # assert_test(False, "error occurred 3")
    # assert_test(False, "just some testing 4", "error occurred 4")
    # assert_test(False, "just some testing 5", "error occurred 5", "this passed 5")


if __name__ == '__main__':
    main()
