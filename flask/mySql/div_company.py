import mysql.connector
from flask import Flask, render_template, request
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploaded_cover_page"


'''
# Establish a connection to the database
When connecting to a database there are 4keys pieces of info

- host: The address to the server the database is running on. Typically localhost
- user: The username to connect to the database
- password: The password to connect to the database
- database: The name of the database to connect to



'''
conn = mysql.connector.connect(

    host="localhost",
    user="life_giver",
    password="lifegiver13",
    database="amc_se"

)

cursor = conn.cursor()
# sql = "SELECT * FROM novel_list"
# cursor.execute(sql)

# novel_list = cursor.fetchall()

# for novel in novel_list:
#     print(novel)

user_sql = "SELECT username, email_address FROM users WHERE username='Toshiro' "
cursor.execute(user_sql)

users = cursor.fetchall()

# updating = "UPDATE users SET username= 'Toishiro' WHERE id = 8 "
# cursor.execute(updating)

# update = cursor.fetchall()

# print(update)


# for user in users:
#     print(user)


@app.route("/novel_upload", methods=["POST", "GET"])
def uploading_info():
    if request.method == "POST":
        novel_name = request.form.get("novelName")
        novel_type = request.form.get("novelType")
        theme = request.form.get("theme")
        author = request.form.get("author")
        book_cover = request.files["book_cover"]

        # Save the uploaded book cover
        cover_path = None
        if book_cover:
            cover_path = os.path.join(
                app.config["UPLOAD_FOLDER"], book_cover.filename)
            book_cover.save(cover_path)

        # Insert data into the MySQL database
        insert_query = """
            INSERT INTO novel_list (novel_name, novel_type, theme, author, cover_page)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (novel_name, novel_type, theme, author, cover_path)

        cursor.execute(insert_query, values)

        return "Novel uploaded successfully!"

    return render_template("novel_upload.html")


@app.route("/novel_list")
def novel_list():
    # Fetch data from MySQL
    cursor.execute(
        "SELECT novel_name, novel_type, theme, author, cover_page FROM novel_list")
    novels = cursor.fetchall()

    return render_template("novel_list.html", novels=novels)


if __name__ == "__main__":
    app.run(debug=True)
