def main(args:list=None):
    from getpass import getpass
    print(f'\nYour password is hidden when typing!\nPassword = {getpass("Pretend that you are entering password: ")}')

if __name__ == "__main__":
    main()