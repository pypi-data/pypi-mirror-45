
def assert_test(value, message, error=None, passed=None):
    if message is not None:
        if passed is None or not value:
            print(message)
        else:
            print(message, end="...")
    if value:
        if passed is not None:
            print(passed)
    else:
        if error is not None:
            print(error)
        assert False


def main():
    assert_test(True, "just some testing 0")
    assert_test(True, "just some testing 1", "error occurred 1")
    assert_test(True, "just some testing 2", "error occurred 2", "this passed 2")
    assert_test(False, "error occurred 3")
    assert_test(False, "just some testing 4", "error occurred 4")
    assert_test(False, "just some testing 5", "error occurred 5", "this passed 5")


if __name__ == '__main__':
    main()
