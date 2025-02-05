from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
# Attach a decoration that handles the route
def hello_world():
    return "Anime Novel Web-site"


@app.route('/listing.html')
def listing_page():
    anime_list = [
        {"name": "The Moon Of Dominion",
         "novel_type": " Shonen",
         "theme": "Freindship, Adventure, Supernatural, and Betrayal",
         "image_url": "data:image/jpeg;base64,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",
         "link": ""
         },
        {"name": "The Bone Exorcist",
         "novel_type": "Shonen",
         "theme": "Super-natural, Mystry, Drama, Funny and Revenge.",
         "image_url": "static/images/bone_exors.webp",
         "link": "TBE.html"},
        {"name": "Onepiece",
         "novel_type": "Shonen",
         "theme": "DFantasy, Mystry, Drama, Funny and Revenge.",
         "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwv9BE5y0e3J7tGx1n8DVIU6sGgWj3-mvE5w&s",
         "link": ""}

    ]
    return render_template("listing.html", anime_list=anime_list)


if __name__ == "__main__":
    app.run(debug=True)
