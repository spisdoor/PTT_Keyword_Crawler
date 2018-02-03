from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Required
from crawler.crawler import *
app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"

class KeywordForm(FlaskForm):
    name = StringField("請輸入欲查詢 PTT 版名稱", validators=[Required()])
    page_num = IntegerField("請輸入欲查詢頁數", validators=[Required()])
    keyword = StringField("請輸入關鍵字", validators=[Required()])
    search_way = SelectField('請輸入搜尋方式', choices=[('title', '標題'), ('content', '內文'), ('message', '留言')], validators=[Required()])
    submit = SubmitField("Submit")

@app.route("/", methods=["GET", "POST"])
def index():
    article_title = []
    article_content = []
    article_message = []
    form = KeywordForm()

    if form.validate_on_submit():
        name = form.name.data
        page_num = form.page_num.data
        keyword = form.keyword.data
        search_way = form.search_way.data
        form.name.data = ""
        form.page_num.data = ""
        form.keyword.data = ""
        form.search_way.data = ""

        if search_way == "title":
            article_title = getByArticleTitle(name, page_num, keyword)
            return render_template("index.html", form=form, article_title=article_title, keyword=keyword)
        elif search_way == "content":
            article_content = getByArticleContent(name, page_num, keyword)
            return render_template("index.html", form=form, article_content=article_content, keyword=keyword)
        elif search_way == "message":
            article_message = getByArticleMessage(name, page_num, keyword)
            return render_template("index.html", form=form, article_message=article_message, keyword=keyword)
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
