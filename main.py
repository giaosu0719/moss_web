from flask import Flask,request,redirect,render_template,flash
import os,subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Secreet!'
path_results = './results/'

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/results/<number>')
def results(number):
    try:
        f = open(path_results + number + "/config.txt")
    except FileNotFoundError:
        return render_template('results.html', resultss = 'Id not found.', logs = '')
    else:
        Check_entry = f.read()
        if Check_entry == "True":
            with open(path_results + number + '/config.txt','w') as f:
                f.write("False")
            with open(path_results + number + '/log.txt','r') as f:
                link = f.read()
            if link == '':
                return render_template('results.html', resultss = 'Loi roi thu lai di!', logs = '')
            else:
                return render_template('results.html', resultss = '', logs = link)
        else:
            return render_template('results.html', resultss = 'May deo co quyen', logs = '')

@app.route('/', methods = ['POST'])
def moss():
    # print(request.values)
    if not request.values.get('lang'):
        flash('Pick a language!')
        return redirect('/')
    if not request.values.get('code1') or not request.values.get('code2'):
        flash('Nhap code di dit me may!')
        return redirect('/')
    
    # Tao thu muc ket qua
    dir = os.listdir(path_results)
    number = str(len(dir) + 1)
    path = os.path.join(path_results,number)
    os.mkdir(path)
    # con cac bu cha ba lua :fire:
    # Luu ket qua
    with open(path_results + number + f'/code1.{request.values.get('lang')}', 'w') as f:
        f.write(f'{request.values.get('code1')}')
    with open(path_results + number + f'/code2.{request.values.get('lang')}', 'w') as f:
        f.write(f'{request.values.get('code2')}')
    with open(path_results + number + '/config.txt', 'w') as f:
        f.write('True')
    
    # Moss cac thu
    f = open(path_results + number + f'/log.txt', 'w')
    if request.values.get('lang') == "py":
        subprocess.call(["perl", "moss.pl", "-l", "python", f"{path_results + number + '/code1.py'}", f"{path_results + number + '/code2.py'}"],stdout=f)
    else:
        subprocess.call(["perl", "moss.pl", "-l", "cc", f"{path_results + number + '/code1.cpp'}", f"{path_results + number + '/code2.cpp'}"],stdout=f)

    return redirect(f'/results/{number}')



if __name__ == "__main__":
    from waitress import serve
    # serve(app,host='0.0.0.0',port=80) # Stable run
    app.run(host="0.0.0.0", debug=True, port=80) # Debug
