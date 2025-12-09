from flask import Flask,redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SUPER_SECRET_KEY'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movielist.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director=db.Column(db.String(100), nullable=False)
    genre=db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=False)

 
    
    def __repr__(self) -> str:
        return f"{self.id} - {self.title,self.year,self.rating,self.description,self.director,self.genre}"





with app.app_context():
    db.create_all()
@app.route("/")
def base():
    return render_template('add.html')



@app.route("/movies",methods=["GET","POST"])
def movies():
    if request.method=="post":
        title=request.form("title")
        director=request.form("director")
        genre=request.form("genre")
        year=request.form("year")
        rating=request.form("rating")
        description=request.form("description")
        New_movie=Movie(title=title,director=director,genre=genre,year=year,rating=rating,description=description)
        db.session.add(New_movie)
        db.session.commit()
    movie=Movie.query.all()  

    return render_template("add.html",movies=movie)


@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    if request.method=="post":
        title=request.form['title']
        director=request.form['director']
        genre=request.form['genre']
        year=request.form['year']
        rating=request.form['rating']
        description=request.form['description']

        updatelist=Movie.query.filter_by(id=id).first()
        updatelist.title=title
        updatelist.director=director
        updatelist.genre=genre
        updatelist.year=year
        updatelist.rating=rating    
        updatelist.description=description

        db.session.add(updatelist)
        db.session.commit()

        return redirect("/")
    updatelist=Movie.query.filter_by(id=id).first()
    return render_template("movielist.html",movies=updatelist)

@app.route("/delete/<int:id>",methods=["GET","POST"])
def delete(id):
    if request.method=="post":
        deletelist=Movie.query.filter_by(id=id).first()
        db.session.delete(deletelist)
        db.session.commit()
        return redirect("/")
    
    deletelist=Movie.query.filter_by(id=id).first()
    return render_template("movielist.html",movies=deletelist)

if __name__ == "__main__":
    app.run(debug=True , port=5501)