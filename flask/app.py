from flask import Flask, render_template, request, url_for
import os
import json

app = Flask(__name__)


# @app.route("/")
# # Attach a decoration that handles the route
# def hello_world():
#     return "Anime Novels"
app.config["UPLOAD_FOLDER"] = "static/uploaded_cover_page"


@app.route("/intro", methods=["GET", "POST"])
@app.route("/intro/<username>")
def intro(username=None):
    print(request.args)
    username = request.args.get("username", "User")
    emailA = request.form.get("emailA")
    password = request.args.get("password", "1234")

    if request.method == "POST":
        username = request.form.get("userName")
        emailA = request.form.get("emailA")
        password = request.form.get("password")
        print(username, emailA, password)

        with open("user_info.txt", "w") as file:
            info = (f"User Name: {username}\n")
            info += (f"EmailAdress: {emailA}\n")
            info += (f"Password: {password}\n")
            file.write(info)
        file.close()
   # Check if credentials are correct

    if username:
        return f"Welcome to Anime Novels {username}"

    else:
        return "Hello, User"


@app.route('/listing_page.html')
def listings():
    return render_template("default_page.html", page_title="View All Products", page_header="All Products", page_content="We have all products.")


@app.route('/landing_page')
def style():
    return render_template("landing_page.html", page_title="Welcome")


@app.route('/TBE.html')
def TBE():
    return render_template("TBE.html", page_title="The Bone Exorsist")


# @app.route('/listing.html')
# def listing_page():
#     anime_list = [
#         {"name": "The Moon Of Dominion",
#          "novel_type": " Shonen",
#          "theme": "Freindship, Adventure, Supernatural, and Betrayal",
#          "image_url": "data:image/jpeg;base64,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",
#          "link": ""
#          },
#         {"name": "The Bone Exorcist",
#          "novel_type": "Shonen",
#          "Theme": "Super-natural, Mystry, Drama, Funny and Revenge.",
#          "img_url": "static/images/bone_exors.webp",
#          "link": "templates/TBE.html"},
#     ]
#     return render_template("listing.html", anime_list=anime_list)


# @app.route('/popular_novels.html')
# def popular_novels():
#     anime_list = [
#         {"name": "The Moon Of Dominion",
#          "novel_type": " Shonen",
#          "theme": "Freindship, Adventure, Supernatural, and Betrayal",
#          "image_url": "data:image/jpeg;base64,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",
#          "link": ""
#          },
#         {"name": "The Tower Of Light and Darkness ",
#          "novel_type": "Shonen",
#          "Theme": "Super-natural, Mystry, Drama, Funny and Revenge.",
#          "img_url": "data:image/jpeg;base64,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",
#          "link": ""},
#     ]
#     return render_template("popular_novels.html", anime_list=anime_list)


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
