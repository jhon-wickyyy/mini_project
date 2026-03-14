from config import TEMPLATE_FILE
import os
from db import *
import urllib.parse
from auth import *
import datetime

def render_template(template_name, context):
    file_path = os.path.join(TEMPLATE_FILE, template_name)
    with open(file_path,'r',encoding="utf-8") as f:
        html_content = f.read()

    for  key,value in context.items():
        placeholer = f"{{{{{key}}}}}"
        html_content = html_content.replace(placeholer, value)

    return html_content


def handle_admin_login(error_msg=""):
    final_html = render_template('login.html', {"error_msg": error_msg})
    return final_html,"200 OK",""

def process_admin_login(request_data):
    users = load_users()

    parts = request_data.split('\r\n\r\n',1)
    parse_body = urllib.parse.parse_qs(parts[1])

    username = parse_body.get("username",[""])[0]
    password = parse_body.get("password",[""])[0]

    ###
    user = next((a for a in users if a.get('username') == username  and a.get('password')==password),None)

    if user:
        session_id = create_session(user)
        headers =f"Location: /admin\r\nSet-cookie: session_id={session_id};Path=/\r\n"
        return "","302 Found",headers

    html_body,status_code,extra_headers = handle_admin_login("账号密码错误")
    return html_body,status_code,extra_headers



def handle_home_page():
    articles = load_articles()
    articles_html = ""
    for article in articles:
        index = int(article.get('article_id'))
        articles_html += f"""
        <div style="background-color:#fff;padding:10px;">
            <h2><a href="/article?id={index}">{article.get('title','无标题')}</a>
            <p style="color:gray;">{article.get('date',' ')}</p>
        </div>
        """
    final_html = render_template("index.html", {"articles_html": articles_html})
    return final_html ,"200 OK",""

def handle_article_page(article_id):
    articles = load_articles()
    idx = int(article_id)
    article = next((a for a in articles if int(a.get('article_id')) == idx),None)

    #可以加入未搜素到的情况判断

    context ={
            "title": article.get('title', ''),
            "content": article.get('content', ''),
            "date": article.get('date', ''),
            }

    final_html = render_template("article.html", context)
    return final_html ,"200 OK",""

def handle_admin_dashboard(username):
    articles = load_articles()
    list_html = ""
    for article in articles:
        if article.get('username') == username:
            index = article.get('article_id')

            list_html += f"""
            <li>
                {article.get('title','')}({article.get('date',"")})
                <a href="/admin/edit?article_id={index}">[编辑]</a>
                <form method="POST" action="/admin/delete" style="display:inline;">
                    <input type="hidden" name="article_id" value="{index}">
                    <button type="submit" style="color:red;">删除</button>
                </form>
            </li>
            """


    final_html = render_template("admin.html",{"list_html":list_html})

    return final_html,"200 OK",""

def handle_admin_add_page():
    context = {
                "page_title": "添加文章",
                "action_url": "/admin/add",
                "title_value": "",
                "content_value": "",
                "hidden_id_input": "",
                }

    final_html = render_template("form.html",context)
    return final_html, "200 OK", ""

def process_admin_add(request_data,username):
    articles = load_articles()

    #防止没有文章的时候，没有id
    if articles:
        new_id = max(a["article_id"] for a in articles) + 1
    else:
        new_id = 0

    parts = request_data.split('\r\n\r\n',1)
    parsed_body = urllib.parse.parse_qs(parts[1])

    article = {
        "article_id": new_id,
        "title": parsed_body.get("title","")[0],
        "content": parsed_body.get("content","")[0],
        "date": datetime.date.today().isoformat(),
        "username": username,
    }
    articles.append(article)
    save_articles(articles)
    return "", "302 Found", "Location: /admin\r\n"

def handle_admin_edit_page(article_id):
    articles = load_articles()
    article = next((a for a in articles if str(a.get("article_id")) == str(article_id)), None)
    idx = article.get("article_id")

    context = {
        "page_title": "编辑页面",
        "action_url": "/admin/edit",
        "hiden_id_input": f"<input type=hiden name='article_id' value='{idx}'>",
        "title_value":article.get("title",""),
        "content_value":article.get("content",""),
    }

    final_html = render_template("form.html",context)
    return final_html,"200 OK",""

def process_admin_edit(request_data):
    parts = request_data.split("\r\n\r\n",1)
    if len(parts[1])>1:
        qarsed_body = urllib.parse.parse_qs(parts[1])
        idx = int(qarsed_body.get("article_id","")[0])
        articles = load_articles()

        article = next(a for a in articles if int(a.get("article_id"))==idx)
        article["title"] = qarsed_body.get("title","")[0]
        article["content"] = qarsed_body.get("content","")[0]
        article["date"] = datetime.date.today().isoformat()

        save_articles(articles)
    return "", "302 Found", "Location: /admin\r\n"

def process_admin_delete(request_data):
    parts = request_data.split("\r\n\r\n",1)
    parsed_body = urllib.parse.parse_qs(parts[1])
    article_id = int(parsed_body.get("article_id","")[0])

    articles = load_articles()
    article = next((a for a in articles if a.get("article_id")==article_id), None)
    articles.remove(article)
    save_articles(articles)
    return "", "302 Found", "Location: /admin\r\n"