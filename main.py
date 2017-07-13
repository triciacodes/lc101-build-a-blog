from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
# this gives you a view into what is happening in terminal
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# creating a persistent class
class Blog(db.Model):

    # specify the data fields that should go into columns
    id = db.Column(db.Integer, primary_key=True)
    # these are both set as Text instead of String so there is not a character limit
    title = db.Column(db.Text)  # blog title
    post = db.Column(db.Text)   # blog post text

    def __init__(self, title, post):
        self.title = title
        self.post = post 

# DISPLAYS ALL BLOG POSTS

@app.route('/blog')
def index():

    all_blog_posts = Blog.query.all()
    # first of the pair matches to {{}} in for loop in the .html template, second of the pair matches to variable declared above
    return render_template('blog.html', posts=all_blog_posts)

# DISPLAYS NEW BLOG ENTRY FORM

@app.route('/newpost')
def blog_entry_form():
    return render_template('new_post.html')

# VALIDATION FOR EMPTY FORM

def empty_val(x):
    if x:
        return True
    else:
        return False

# THIS HANDLES THE REDIRECT (SUCCESS) AND ERROR MESSAGES (FAILURE)

@app.route('/newpost', methods=['POST', 'GET'])
def add_entry():

    # THIS CREATES VARIABLES WITH FORM INPUTS

    post_title = request.form['blog_title']
    post_entry = request.form['blog_post']

    # THIS CREATES EMPTY STRINGS FOR THE ERROR MESSAGES

    title_error = ""
    blog_entry_error = ""

    if empty_val(post_title) and empty_val(post_entry):

        if request.method == 'POST':
            post_title = request.form['blog_title']
            post_entry = request.form['blog_post']
            post_new = Blog(post_title, post_entry)
                
            db.session.add(post_new)
            db.session.commit()

            return redirect('/blog')

    else:
        return render_template('new_post.html')

# only runs when the main.py file run directly
if __name__ == '__main__':
    app.run()