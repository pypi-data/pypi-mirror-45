def main(args: list = []):
    from jerryc05.mod_12306.train_station import parse
    for x in parse(input('Keywords for train station? ')):
        print(x)

    # from getpass import getpass
    # print(
    #     f'\nYour password is hidden when typing!\nPassword = {getpass("Type password here (hidden): ")}')


if __name__ == "__main__":
    main()
