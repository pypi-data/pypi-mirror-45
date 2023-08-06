def main():
    from sys import argv
    argv: list
    if len(argv) == 1:
        argv.append('12306')
    from my_12306.__main__ import main as main_12306
    # todo

    {
        '12306': lambda: main_12306(argv[1:]),
    }.get(argv[1] if type(argv[1]) == str else f'{argv[1]}',
          lambda: print(f'Argument {argv[1]} invalid'))()


if __name__ == "__main__":
    main()
