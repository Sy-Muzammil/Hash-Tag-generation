from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
   return render_template('index.html',mdict=out_dict,stdict=stdict)

@app.route('/handle/<cur>')
def handle(cur):
    global stdict
    stdict[cur] = 1
    return render_template('index.html',mdict=out_dict,stdict=stdict)
    

def process(fn):
    dct={}
    st={}
    fp = open(fn,'r')
    for j in fp:
        jlist = j.split("\t")
        dct[jlist[0]] = (jlist[1],jlist[2])
        st[jlist[0]] = -1
    return dct,st
if __name__ == "__main__":
    fname = "data.txt"
    global out_dict
    global stdict
    out_dict,stdict = process(fname)
    app.run(debug=True)
