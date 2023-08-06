n='Index number invalid, retry: '
m='Index number: '
l='+-----+--------------------+------+--------------+'
k='+-----+--------------------+------+--------------+\n| No. |    STATION NAME    | CODE |   CHN NAME   |\n+-----+--------------------+------+--------------+'
j='--- NO RESULT! ---'
C=list
i=enumerate
h=ord
A=str
e=SystemError
d=tuple
S=' '
Q=None
O=int
H=input
F=len
E=print
B=''
def query_city(d_city,a_city):
	import jerryc05.mod_12306.station_name;K=jerryc05.mod_12306.station_name.parse;C=d_city.lower();J=[];import operator as L;M=L.itemgetter
	while F(J)<2:
		A=Q
		while not A or not A[0][0]:
			while not C or not 96<h(C[0])<123:C=H(f"Invalid argument: Expected letters but found {C}, retry: ")
			A=K(C)
			if not A:A=[(B,B,B,j,B,B)]
			A.sort(key=M(3));E(k)
			for (N,G) in i(A):E(f"| {N+1:3} | {G[3]:18} | {G[2]:4} | {G[1]:{12-F(G[1])+G[1].count(' ')}} |")
			E(l)
			if not A[0][0]:A=Q;C=H(f'City name "{C}" not found, retry: ')
		I=O(H(m))-1
		while not 0<=I<F(A):I=O(H(n))-1
		D=A[I];E(f"""Chosen station name:
+-----+--------------------+------+--------------+
| {I+1:3} | {D[3]:18} | {D[2]:4} | {D[1]:{12-F(D[1])+D[1].count(" ")}} |
+-----+--------------------+------+--------------+

""");J.append((D[1],D[2]));C=a_city.lower()
	return J
def main(args=Q):
	N='0';M='\\';J=args
	if not J:J=[]
	if F(J)<3:raise e(f'Missing argument: Expected "<d_city> <a_city> <date>" but found {J}.')
	A=J[2]
	while not F(A)==10 or not O(A[:4])>2018 or not 0<O(A[5:7])<13 or not 0<O(A[8:])<32:
		if F(A)==8:A=f"{A[:4]}-{A[4:6]}-{A[6:8]}"
		else:A=H(f'Date "{A}" invalid, retry: ')
	if 1:
		T=B;U=B;import jerryc05.mod_12306.station_name;o=jerryc05.mod_12306.station_name.parse;I=J[0].lower();import operator as p;q=p.itemgetter
		while not U:
			C=Q
			while not C or not C[0][0]:
				while not I or not 96<h(I[0])<123:I=H(f"Invalid argument: Expected letters but found {I}, retry: ")
				C=o(I)
				if not C:C=[(B,B,B,j,B,B)]
				C.sort(key=q(3));E(k)
				for (r,K) in i(C):E(f"| {r+1:3} | {K[3]:18} | {K[2]:4} | {K[1]:{12-F(K[1])+K[1].count(' ')}} |")
				E(l)
				if not C[0][0]:C=Q;I=H(f'City name "{I}" not found, retry: ')
			R=O(H(m))-1
			while not 0<=R<F(C):R=O(H(n))-1
			G=C[R];E(f"""Chosen station name:
+-----+--------------------+------+--------------+
| {R+1:3} | {G[3]:18} | {G[2]:4} | {G[1]:{12-F(G[1])+G[1].count(" ")}} |
+-----+--------------------+------+--------------+

""")
			if not T:T=G[1],G[2]
			else:U=G[1],G[2]
			I=J[1].lower()
	if 1:
		import urllib.request
		with urllib.request.urlopen(f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={A}&leftTicketDTO.from_station={T[1]}&leftTicketDTO.to_station={U[1]}&purpose_codes=ADULT")as s:
			import json;E('+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+\n| TRAIN | START |  END  | TOTAL |  VIP  |  1ST  |  2ND  |  SOFT-  |  HARD-  | HARD | NONE |\n|  NO.  | TIME: | TIME: | TIME: | CLASS | CLASS | CLASS | SLEEPER | SLEEPER | SEAT | SEAT |\n+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+');import jerryc05.mod_12306.mod_parser;L=jerryc05.mod_12306.mod_parser.ticket_count;f=jerryc05.mod_12306.mod_parser.colored_text;g=s.read()
			if b'<'in g[:4]:raise e(f"Invalid date, {A} may be some date in the past.")
			try:V=json.loads(g)['data']['result']
			except Exception as t:raise e(f"Internal process error, please contact support. Detail: {t}")
			if not V:V='|||-----|||||-----|-----|-----|||||||||||||||||||||||',
			for K in V:
				D=K.split('|');u=D[3];v=D[8];w=D[9];x=D[10];W=L(D[32]);X=L(D[31]);P=L(D[30]);Y=L(D[23]);Z=L(D[28]);a=L(D[29]);b=L(D[26]);c=f"| {u:5} | {v:5} | {w:5} | {x:^5} | {W:^5} | {X:^5} | {P:^5} | {Y:^7} | {Z:^7} | {a:^5}| {b:^5}|"
				if not P==M and not P==N:f(c,'green',style='bright')
				elif(W==M or W==N)and(X==M or X==N)and(P==M or P==N)and(Y==M or Y==N)and(Z==M or Z==N)and(a==M or a==N)and(b==M or b==N):f(c,'red',style='dim')
				else:E(c)
			E('+-------+-------+-------+-------+-------+-------+-------+---------+---------+------+------+')