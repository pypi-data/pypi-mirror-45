def fizz_buzz(x: int) -> str or int:
    if not x % 15:  # === (not x % 3) and (not x % 5)
        return 'FizzBuzz'
    if not x % 3:
        return 'Fizz'
    if not x % 5:
        return 'Buzz'
    return x


if __name__ == "__main__":
    for x in range(1,101):
        print(fizz_buzz(x))

    assert (fizz_buzz(3) == 'Fizz')
    assert (fizz_buzz(5) == 'Buzz')
    assert (fizz_buzz(15) == 'FizzBuzz')


    print('.')
