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


def exception_test(message,  method_to_test, **kwargs):
    print(message, end="...")
    try:
        method_to_test(**kwargs)
        raise DebugException("this should fail")
    except Exception as e:
        if isinstance(e, DebugException):
            raise e
        pass
    print("passed")


def _test(throws, info):
    if throws:
        raise Exception("Throws")
    else:
        print(info)


def main():
    exception_test("testing - should throw 0", _test, throws=True, info="hello")
    try:
        exception_test("testing - should not throw 1",  _test, throws=False, info="hello")
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
