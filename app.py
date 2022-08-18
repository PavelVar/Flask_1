from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    '''class for create an object of database'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Article {self.id}'


# adding route for the main page
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


# adding route for the main page
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/customers')
def customers():
    return render_template('7_customers.html')


@app.route('/tabs')
def tabs():
    return render_template('4_tabs.html')


# adding route for the page where we could create articles
@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':  # if method post, we add attributes
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)  # and create an object with attributes
        try:  # trying to add object to db
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')  # after adding going to page with all posts
        except Exception:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create-article.html')  # if method is not post, going to the create article page


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()  # getting the list of all articles ordered by date descending
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except Exception:
        return 'При удалении статьи произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.get(id)
    if request.method == 'POST':  # if method is POST changing attributes and trying to commit changes to db
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect(f'/posts/{article.id}')
        except Exception:
            return 'При изменении статьи произошла ошибка'
    else:
        return render_template('post-update.html', article=article)  # if method is not POST going to udate page


if __name__ == '__main__':
    app.run(debug=True)
