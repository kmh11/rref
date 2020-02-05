from flask import Flask, send_file, request
app = Flask(__name__)

@app.route('/')
def index():
    return send_file("index.html")

def swapSort(m):
	zc = lambda r: len([i for i in range(len(r)) if len(list(filter(lambda x:x!=0, r[:i+1]))) == 0])
	code = ""
	for i in range(len(m)):
		for r in range(len(m)-1):
			if zc(m[r]) > zc(m[r+1]):
				m[r], m[r+1] = m[r+1], m[r]
				code += f'{{%variable%}}([{r+1},{r+2}],:) = {{%variable%}}([{r+2},{r+1}],:)\n'
	return code

@app.route('/code', methods=['POST'])
def code():
	matrix = request.data.decode("utf8").replace(';', '\n').translate(str.maketrans('', '', ''.join(set(request.data.decode("utf8")) - set("\u2212- \n\t0123456789.e")))).strip().split("\n")
	coefficients = [[float(d.strip().replace("−", "-")) for d in r.strip().split(" ")[:-1] if len(d.strip()) > 0] for r in matrix if len(r.strip()) > 0]
	answers = [[float(d.replace("−", "-")) for d in r.split(" ") if len(d.strip()) > 0][-1] for r in matrix if len(r.strip()) > 0]
	mname = '{%variable%}'
	m = [coefficients[i] + [answers[i]] for i in range(len(coefficients))]
	code = mname+" = "+"["+" ; ".join(" ".join([str(d) for d in r]) for r in m)+"]"+"\n"
	code += swapSort(m)
	for i in range(len(m)):
		for j in range(len(m)):
			if i == j or i >= len(m[i]): continue
			if m[i][i] != 0:
				pmj = m[j][:]
				m[j] = [m[j][k] - m[i][k]*m[j][i]/m[i][i] for k in range(len(m[j]))]
				if m[j] != pmj: code += f'{mname}({j+1},:) = {mname}({j+1},:) - {mname}({i+1},:)*{mname}({j+1},{i+1})/{mname}({i+1},{i+1})\n'
			else:
				for p in range(i+1, len(m[i])):
					if m[i][p] != 0:
						pmj = m[j][:]
						m[j] = [m[j][k] - m[i][k]*m[j][p]/m[i][p] for k in range(len(m[j]))]
						if m[j] != pmj: code += f'{mname}({j+1},:) = {mname}({j+1},:) - {mname}({i+1},:)*{mname}({j+1},{p+1})/{mname}({i+1},{p+1})\n'
						break
	for i in range(len(m)):
		if i >= len(m[i]): continue
		if m[i][i] != 0:
			if m[i][i] != 1: code += f'{mname}({i+1},:) = {mname}({i+1},:)/{mname}({i+1},{i+1})\n'
		else:
			for p in range(i+1, len(m[i])):
				if m[i][p] != 0:
					if m[i][p] != 1: code += f'{mname}({i+1},:) = {mname}({i+1},:)/{mname}({i+1},{p+1})\n'
					break
	code += swapSort(m)
	return code.replace("-","\u2212").strip()

if __name__ == "__main__":
	app.run()
