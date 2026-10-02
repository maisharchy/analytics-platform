# Import Flask tools we need to build the web app
from flask import Flask, request, render_template, make_response

# Import WeasyPrint to convert HTML into a PDF
from weasyprint import HTML


# Create the Flask application
app = Flask(__name__)


# Create a GET endpoint at /health
@app.get("/health")
def health():
    # Return a simple response to show the server is working
    return {"status": "ok"}


# Create a POST endpoint at /report
@app.post("/report")
def report():
    # Get the JSON data sent by the user
    data = request.get_json()

    # Fill the HTML template with the JSON data
    html = render_template("report.html", **data)

    # Convert the HTML into a PDF
    pdf = HTML(string=html).write_pdf()

    # Create a response containing the PDF
    resp = make_response(pdf)

    # Tell the browser/client that the response is a PDF
    resp.headers["Content-Type"] = "application/pdf"

    # Tell the browser to download the file as report.pdf
    resp.headers["Content-Disposition"] = "attachment; filename=report.pdf"

    # Send the PDF back to the user
    return resp