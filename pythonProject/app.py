from flask import Flask, render_template,request


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form!=None:
        f=request.form
        for key in f:
            for value in f.getlist(key):
                print(key,":", value)
        return render_template('index.html', form=f) 
    return render_template('index.html')
def submitRecepy():
    f=request.form
    for key in f:
        for value in f.getlist(key):
            print(key,":", value)
    return f

@app.route('/submitRecepty', methods=['POST', 'GET'])
def submitRecepty():
    f=request.form
    for key in f:
        for value in f.getlist(key):
            print(key,":", value)
    return"adasdas "
if __name__ == '__main__':
    app.run(debug=True)

