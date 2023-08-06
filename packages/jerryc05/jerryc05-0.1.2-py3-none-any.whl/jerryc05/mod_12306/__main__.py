def query_city(city: str) -> tuple:
    '''return (ID, CHN NAME)'''

    from jerryc05.mod_12306.station_name import parse
    city = city.lower()
    while not city or not 96 < ord(city[0]) < 123:
        print(f'Invalid argument: Expected letters but found {city}.')
        return ()

    station = parse(city)
    if not station:
        station = [('', '', '', '--- NO RESULT! ---', '', '')]
    station.sort(key=lambda x: x[3])
    print('''\
+-----+--------------------+-----+--------------+
| NO. |    STATION NAME    | ID: |   CHN NAME   |
+-----+--------------------+-----+--------------+\
''')
    for index, item in enumerate(station):
        print(f'''\
| {index+1:3} | {item[3]:18} | {item[2]:3} | {item[1]:{12-len(item[1])+item[1].count(" ")}} |\
''')
    print('''\
+-----+--------------------+-----+--------------+\
''')

    if not station[0][0]:
        return query_city(input(f'City name "{city}" not found, retry: '))

    index_chosen = int(input('Index number: '))-1
    while not 0 <= index_chosen < len(station):
        index_chosen = int(input('Index number invalid, retry: '))-1

    station_chosen: tuple = station[index_chosen]
    print(f'''Chosen station name:
+-----+--------------------+-----+--------------+
| {index_chosen+1:3} | {station_chosen[3]:18} | {station_chosen[2]:3} | {station_chosen[1]:{12-len(station_chosen[1])+station_chosen[1].count(" ")}} |
+-----+--------------------+-----+--------------+

''')
    return (station_chosen[1], station_chosen[2])


def main(args=[]):
    '''param: args =  [depart_city, arrive_city, date]'''

    __len_args = len(args)
    if __len_args < 3:
        print(f'Missing argument: Expected 3 but found {__len_args}.')
        return

    # todo support more argument
    depart_city, arrive_city, date = \
        query_city(args[0]), query_city(args[1]), args[2]

    from urllib import request
    with request.urlopen(
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        f'leftTicketDTO.train_date={date}&'
        f'leftTicketDTO.from_station={depart_city[1]}&'
        f'leftTicketDTO.to_station={arrive_city[1]}&'
        'purpose_codes=ADULT'
    ) as r:
        import json
        print(f'''\
+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+
| TRAIN | START |  END  | TOTAL |  VIP  |  1ST  |  2ND  |  SOFT-  |  HARD-  | HARD | NONE |
|  NO.  | TIME: | TIME: | TIME: | CLASS | CLASS | CLASS | SLEEPER | SLEEPER | SEAT | SEAT |
+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+\
''')
        from jerryc05.mod_12306.parser import ticket_count, colored_text
        train_data: tuple = json.loads(r.read())['data']['result']
        if not train_data:
            train_data = (
                '|||-----|||||-----|-----|-----|||||||||||||||||||||||',)
        for item in train_data:
            train = item.split('|')
            train_no = train[3]
            # from_station_code = train[6]
            # from_station_name = depart_city[0]
            # to_station_code = train[7]
            # to_station_name = arrive_city[0]
            start_time = train[8]
            arrive_time = train[9]
            total_time = train[10]
            vip_class_seat = ticket_count(train[32])
            first_class_seat = ticket_count(train[31])
            second_class_seat = ticket_count(train[30])
            soft_sleeper = ticket_count(train[23])
            hard_sleeper = ticket_count(train[28])
            hard_seat = ticket_count(train[29])
            no_seat = ticket_count(train[26])

            info = f'| {train_no:5} '\
                f'| {start_time:5} '\
                f'| {arrive_time:5} '\
                f'| {total_time:^5} '\
                f'| {vip_class_seat:^5} '\
                f'| {first_class_seat:^5} '\
                f'| {second_class_seat:^5} '\
                f'| {soft_sleeper:^7} '\
                f'| {hard_sleeper:^7} '\
                f'| {hard_seat:^4} '\
                f'| {no_seat:^4} |'

            if not second_class_seat == '\\' and not second_class_seat == '0':
                colored_text(info, 'green', style='bright')

            elif (vip_class_seat == '\\' or vip_class_seat == '0') and \
                (first_class_seat == '\\' or first_class_seat == '0') and \
                (second_class_seat == '\\' or second_class_seat == '0') and \
                (soft_sleeper == '\\' or soft_sleeper == '0') and \
                (hard_sleeper == '\\' or hard_sleeper == '0') and \
                (hard_seat == '\\' or hard_seat == '0') and \
                    (no_seat == '\\' or no_seat == '0'):
                colored_text(info, 'red', style='dim')

            else:
                print(info)

        print(f'''\
+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+\
''')

    # from getpass import getpass
    # print(
    #     f'\nYour password is hidden when typing!\nPassword = {getpass("Type password here (hidden): ")}')


if __name__ == "__main__":
    from sys import path
    path.insert(0, '.')
    main(['beijing', 'xiam', '2019-05-03'])
