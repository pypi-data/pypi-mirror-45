def station_name(station_name: str = 'station_name.js'):
    js_list: list = []
    with open(station_name, encoding='utf-8') as __js:
        js: str = __js.read()
        start = js.find("'")
        if start == -1:
            raise AssertionError(
                'Parsing js failed: "=" not found in "station_name.js"')
        start += 1
        if js[start] == '@':
            start += 1
        end = js.find("'", start)
        js_list = js[start:end].split('@')
        js_list.sort()

    with open('train_station.py', 'w', encoding='utf-8') as station:
        # for i in range(0, 26):
        #     station.write(f'def __{chr(ord("a")+i)}():\n return (')
        #     for index in range(indice[i], indice[i+1]):
        #         station.write(f"'{js_list[index]}',\n")
        #     station.write(')\n')

        station.write('def parse(s)->list:\n x=(')
        for x in js_list:
            station.write(f"'{x}',\n")
        station.write(''')
 from bisect import bisect
 i=bisect(x,s[0])
 r,t=[],x[i]
 while s[0]==t[0]:
  if s in t:
   r.append(t)
  i+=1
  t=x[i]
 return r\
''')


if __name__ == "__main__":
    station_name()
