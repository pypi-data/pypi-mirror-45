
def assert_test(value, error=None, message=None, passed=None):
    if message is not None:
        print(message)
    assert value, error
    if passed is not None:
        print(passed)


def main():
    assert_test(True)
    assert_test(True, "error occurred 0")
    assert_test(True, "error occurred 1", "just some testing 1")
    assert_test(True, "error occurred 2", "just some testing 2", "this passed 2")
    # assert_test(False, "error occurred 3")
    assert_test(False, "error occurred 4", "just some testing 4")
    assert_test(False, "error occurred 5", "just some testing 5", "this passed 3")


if __name__ == '__main__':
    main()
