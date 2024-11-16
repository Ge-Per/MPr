from flask import Flask, request, render_template

app = Flask(__name__)


# Function to save text to a file
def save_to_file(data):
    with open("data.txt", "a") as file:
        file.write(data + "\n")


@app.route("/")
def form():
    # Send HTML form to the client
    return render_template("form.html")


@app.route("/save_text", methods=["POST"])
def save_text():
    # Get data from the text field
    text = request.form.get("text")

    if text:
        # Save text to a file
        save_to_file(text)
        return "Data saved successfully.", 200
    else:
        return "No text provided.", 400


if __name__ == "__main__":
    app.run(port=8000)
