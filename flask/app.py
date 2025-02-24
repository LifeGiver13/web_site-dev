from flask import Flask, render_template, request, url_for, session
import os
import json
import mysql.connector

app = Flask(__name__)
app.secret_key = "watcher1345Ligivers*&%$"

# @app.route("/")
# # Attach a decoration that handles the route
# def hello_world():
#     return "Anime Novels"
app.config["UPLOAD_FOLDER"] = "static/uploaded_cover_page"


conn = mysql.connector.connect(

    host="localhost",
    user="life_giver",
    password="lifegiver13",
    database="amc_se"

)

cursor = conn.cursor(dictionary=True)


@app.route("/", methods=["GET", "POST"])
def intro():
    logged_in = session.get("logged_in", False)
    username = session.get("username", "Guest")

    if request.method == "POST":
        entered_username = request.form.get("username")
        entered_password = request.form.get("password")

        # Parameterized query to fetch user matching entered username and password
        select_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(select_query, (entered_username, entered_password))
        print(entered_username, entered_password)
        user = cursor.fetchone()

        if user:
            session["username"] = user["username"]
            session["logged_in"] = True
            return f"Welcome to Anime Novels, {user['username']}!"
        else:
            return "Invalid information, please try again."

    return render_template("/", username=username, logged_in=logged_in)


# @app.route("/", methods=["GET", "POST"])
# def intro(username=None):
#     logged_in = session.get("logged_in") if session.get("logged_in") else False
#     username = session["username"] if session.get("logged_in") else "Guest"

#     if request.method == "POST":

#         username = request.args.get("username", "User")
#         emailA = request.form.get("emailA")
#         password = request.form.get("password")

#         select_querry = " SELECT username, password, email_address FROM users WHERE username = %s"
#         cursor.execute(select_querry, (username,))
#         user = cursor.fetchone()
#         if user:
#             # Check if entered credentials match database records
#             if password == user["password"] and emailA == user["email_address"]:
#                 session["username"] = user["username"]
#                 session["logged_in"] = True
#                 return f"Welcome to Anime Novels, {user['username']}!"
#             else:
#                 return "Invalid credentials, please try again."
#         else:
#             return "User not found. Please register."

#     return render_template('/', username=username, logged_in=logged_in)


@app.route('/listing_page.html')
def listings():
    return render_template("default_page.html", page_title="View All Products", page_header="All Products", page_content="We have all products.")


@app.route('/landing_page')
def style():
    return render_template("landing_page.html", page_title="Welcome")


@app.route('/TBE.html')
def TBE():
    return render_template("TBE.html", page_title="The Bone Exorsist")


@app.route("/novel_upload2", methods=["POST", "GET"])
def uploading_info2():
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

        # Insert data into MySQL
        insert_query = """
            INSERT INTO novel_list (novel_name, novel_type, theme, author, cover_page)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (novel_name, novel_type, theme, author, cover_path)

        cursor.execute(insert_query, values)
        conn.commit()

        print(f"{cursor.rowcount} record inserted.")
        return "Novel uploaded successfully!"

    return render_template("novel_upload.html")


@app.route("/novel_list2")
def novel_list2():
    cursor.execute(
        "SELECT novel_name, novel_type, theme, author, cover_page FROM novel_list")

    novels = cursor.fetchall()
    conn.commit()
    return render_template("listing.html", novels=novels)


@app.route("/novel_upload", methods=["POST", "GET"])
def uploading_info():
    # Check if the request method is POST (form submission)
    if request.method == "POST":
        # Retrieve form data submitted by the user
        # Get the novel name from the form
        novel_name = request.form.get("novelName")
        # Get the type of novel (e.g., manga, light novel)
        novel_type = request.form.get("novelType")
        # Get the novel theme (e.g., fantasy, sci-fi)
        theme = request.form.get("theme")
        author = request.form.get("author")  # Get the author's name
        # Get the uploaded book cover file
        book_cover = request.files["book_cover"]

        # Save the uploaded book cover if provided
        if book_cover:
            cover_path = os.path.join(
                app.config["UPLOAD_FOLDER"], book_cover.filename)  # Define the file path
            book_cover.save(cover_path)  # Save the file to the specified path
        else:
            cover_path = None  # Set to None if no file was uploaded

        # Create a dictionary to store the novel details
        novel_data = {
            "Novel Name": novel_name,
            "Novel Type": novel_type,
            "Theme": theme,
            "Author": author,
            "Book Cover": cover_path  # Store the file path of the book cover
        }

        json_file = "novels.json"  # Define the JSON file name to store novel data

        # Check if the JSON file exists and load existing data
        if os.path.exists(json_file):
            with open(json_file, "r") as file:
                try:
                    novels = json.load(file)  # Load existing novel data
                except json.JSONDecodeError:
                    novels = []  # Initialize an empty list if the file is empty or corrupted
        else:
            novels = []  # Initialize an empty list if the file does not exist
        for novel in novels:
            if novel["Book Cover"]:
                novel["Book Cover"] = url_for(
                    "static", filename=f"uploaded_cover_page/{os.path.basename(novel['Book Cover'])}")

        # Append the new novel data to the list
        novels.append(novel_data)

        # Save the updated list back to the JSON file
        with open(json_file, "w") as file:
            # Write data in JSON format with indentation
            json.dump(novels, file, indent=4)

        # Response message after successful upload
        return "Novel uploaded successfully!"

    # If request method is GET, render the novel upload page
    return render_template("novel_upload.html")


# Route to display the list of uploaded novels
@app.route('/listing.html')
def novel_list():
    json_file = "novels.json"  # Define the JSON file name

    # Load existing novel data from the JSON file
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                novels = json.load(file)  # Load novel data
            except json.JSONDecodeError:
                novels = []  # Initialize an empty list if the file is empty or corrupted
    else:
        novels = []  # Initialize an empty list if the file does not exist

    # Render the listing page and pass the novel data to the template
    return render_template("listing.html", novels=novels)


if __name__ == "__main__":
    app.run(debug=True)
