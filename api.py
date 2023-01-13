from flask import Flask,render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///properties.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Property(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.pid} - {self.pname}"

@app.route('/', methods=['GET', 'POST'])
def create():
    if request.method=='POST':
            pname = request.form['pname']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            propertyy = Property(pname=pname, state=state, city=city, address=address)
            db.session.add(propertyy)
            db.session.commit()
            return redirect(url_for('show'))
    return render_template('create.html')


@app.route("/show",methods=['GET','POST'])
def show():
    try:
        allProperty = Property.query.all() 
        return render_template('create.html',allProperty=allProperty,status=True)
    except Exception as e:
        return render_template('create.html',status=False)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
            city=request.form['city']
            return redirect(url_for('search_result',city=city))

    return render_template('search.html')


@app.route('/search_result/<string:city>', methods=['GET', 'POST'])
def search_result(city):

        prop=Property.query.filter_by(city=city).all()
        return render_template('search.html',prop=prop, status=True)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method=='POST':
            pid=request.form['pid']
            pname = request.form['pname']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            upd=Property.query.filter_by(pid=pid).first()
            upd.address=address
            upd.pname=pname
            upd.city=city
            upd.state=state
            db.session.add(upd)
            db.session.commit()

            return redirect(url_for('update_result'))
    return render_template('update.html')
     

@app.route("/update_result", methods=['GET','POST'])
def update_result():
    try:
        allProperty = Property.query.all() 
        return render_template('update.html',allProperty=allProperty,status=True)
    except Exception as e:
        return render_template('update.html',status=False)


if __name__ == "__main__":
    app.run(debug=True, port=5000)