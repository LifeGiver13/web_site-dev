from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploaded_cover_page"


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
