def main(args:list=None):
    print(args)
    from getpass import getpass
    print(f'Your password is protected\n\nPassword = {getpass("Pretend that you are entering password: ")}')

if __name__ == "__main__":
    main()