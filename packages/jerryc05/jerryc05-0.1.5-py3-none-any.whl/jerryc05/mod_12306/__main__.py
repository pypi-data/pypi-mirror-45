f=tuple
c=None
b=SystemError
P=input
O=int
M=len
K=print
def main(args=c):
	q=' ';L='';J='0';I='\\';F=args
	if not F:F=[]
	if M(F)<3:raise b(f'Missing argument: Expected "<d_city> <a_city> <date>" but found {F}.')
	A=F[2]
	while not M(A)==10 or not O(A[:4])>2018 or not 0<O(A[5:7])<13 or not 0<O(A[8:])<32:
		if M(A)==8:A=f"{A[:4]}-{A[4:6]}-{A[6:8]}"
		else:A=P(f'Date "{A}" invalid, retry: ')
	if 1:
		R=L;S=L;import jerryc05.mod_12306.station_name;g=jerryc05.mod_12306.station_name.parse;E=F[0].lower();import operator as h;i=h.itemgetter
		while not S:
			B=c
			while not B or not B[0][0]:
				while not E or not 96<ord(E[0])<123:E=P(f"Invalid argument: Expected letters but found {E}, retry: ")
				B=g(E)
				if not B:B=[(L,L,L,'--- NO RESULT! ---',L,L)]
				B.sort(key=i(3));K('+-----+--------------------+------+--------------+\n| No. |    STATION NAME    | CODE |   CHN NAME   |\n+-----+--------------------+------+--------------+')
				for (j,G) in enumerate(B):K(f"| {j+1:3} | {G[3]:18} | {G[2]:4} | {G[1]:{12-M(G[1])+G[1].count(' ')}} |")
				K('+-----+--------------------+------+--------------+')
				if not B[0][0]:B=c;E=P(f'City name "{E}" not found, retry: ')
			Q=O(P('Index number: '))-1
			while not 0<=Q<M(B):Q=O(P('Index number invalid, retry: '))-1
			D=B[Q];K(f"""Chosen station name:
+-----+--------------------+------+--------------+
| {Q+1:3} | {D[3]:18} | {D[2]:4} | {D[1]:{12-M(D[1])+D[1].count(" ")}} |
+-----+--------------------+------+--------------+

""")
			if not R:R=D[1],D[2]
			else:S=D[1],D[2]
			E=F[1].lower()
	if 1:
		import urllib.request
		with urllib.request.urlopen(f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={A}&leftTicketDTO.from_station={R[1]}&leftTicketDTO.to_station={S[1]}&purpose_codes=ADULT")as k:
			import json;K('+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+\n| TRAIN | START |  END  | TOTAL |  VIP  |  1ST  |  2ND  |  SOFT-  |  HARD-  | HARD | NONE |\n|  NO.  | TIME: | TIME: | TIME: | CLASS | CLASS | CLASS | SLEEPER | SLEEPER | SEAT | SEAT |\n+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+');import jerryc05.mod_12306.mod_parser;H=jerryc05.mod_12306.mod_parser.ticket_count;d=jerryc05.mod_12306.mod_parser.colored_text;e=k.read()
			if b'<'in e[:4]:raise b(f"Invalid date, {A} may be some date in the past.")
			try:T=json.loads(e)['data']['result']
			except Exception as l:raise b(f"Internal process error, please contact support. Detail: {l}")
			if not T:T='|||-----|||||-----|-----|-----|||||||||||||||||||||||',
			for G in T:
				C=G.split('|');m=C[3];n=C[8];o=C[9];p=C[10];U=H(C[32]);V=H(C[31]);N=H(C[30]);W=H(C[23]);X=H(C[28]);Y=H(C[29]);Z=H(C[26]);a=f"| {m:5} | {n:5} | {o:5} | {p:^5} | {U:^5} | {V:^5} | {N:^5} | {W:^7} | {X:^7} | {Y:^5}| {Z:^5}|"
				if not N==I and not N==J:d(a,'green',style='bright')
				elif(U==I or U==J)and(V==I or V==J)and(N==I or N==J)and(W==I or W==J)and(X==I or X==J)and(Y==I or Y==J)and(Z==I or Z==J):d(a,'red',style='dim')
				else:K(a)
			K('+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+')