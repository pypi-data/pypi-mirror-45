I='.'
__version__='0.1.6'
import urllib.request
with urllib.request.urlopen('https://pypi.org/project/jerryc05/')as G:
	A=G.read();B=A.find(b'package-header__name');B=A.find(b'c05',B)+4;H=A.find(b'\n',B);E=A[B:H].decode('utf-8');C=__version__.split(I);D=C[-1]
	for F in range(0,len(D)):
		if D[F].isalpha():C.remove(D);C.append(f"{int(D[:F])-0.1}");break
	if C<E.split(I):print(f'New version {E} available!!!\nType "pip3 install -U jerryc05" to upgrade.')