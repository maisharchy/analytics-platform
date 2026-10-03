# Import Flask tools we need to build the web app
from flask import Flask, request, render_template, make_response
# Import date so we can put today's date on the report
from datetime import date
# Import our chart functions from charts.py
from charts import bar_chart, line_chart
# Import WeasyPrint to convert HTML into a PDF
from weasyprint import HTML


# Create the Flask application
app = Flask(__name__)

# These fields must be included in the JSON request
REQUIRED = ["title", "kpis", "columns", "rows"]

# Connect chart names from the JSON to the functions that create them
# "bar" -> bar_chart()
# "line" -> line_chart()
CHART_TYPES = {
    "bar": bar_chart,
    "line": line_chart
}

# Create a GET endpoint at /health
@app.get("/health")
def health():
    # Return a simple response to show the server is working
    return {"status": "ok"}


# Create a POST endpoint at /report
@app.post("/report")
def report():
    # Get the JSON data sent by the user
    # silent=True prevents Flask from throwing an error if the JSON is invalid
    data = request.get_json(silent=True)

    # If there is no JSON data, return an error with HTTP status 400
    if not data:
        return {"error": "JSON body required"}, 400

    # Check which required fields are missing
    # It loops through REQUIRED and keeps fields that are not in data
    missing = [k for k in REQUIRED if k not in data]

    # If any required fields are missing, return an error
    if missing:
        return {"error": f"missing fields: {missing}"}, 400

    # Get the chart information from the JSON
    # If "charts" does not exist, use an empty list
    # pop() also removes "charts" from data
    # so it won't be passed twice later
    chart_specs = data.pop("charts", [])

    # Create an empty list to store the generated charts
    charts = []

    # Loop through every chart requested in the JSON
    for spec in chart_specs:
        # Look at the chart's "type"
        # Then find the matching function in CHART_TYPES
        # Example:
        # "bar" -> bar_chart
        # "line" -> line_chart
        fn = CHART_TYPES.get(spec.get("type"))


        # If the chart type isn't supported, return an error
        if fn is None:
            return {
                "error": f"unknown chart type: {spec.get('type')}"
            }, 400


        # Generate the chart and add it to the charts list
        charts.append({

            # Save the chart title
            "title": spec["title"],

            # Call the appropriate chart function
            # and generate the Base64 image
            "img": fn(
                spec["labels"],
                spec["values"],
                spec["title"]
            ),
        })


    # Render the HTML template using the data we received
    html = render_template(

        # Tell Flask which HTML template to use
        "report.html",

        # Add today's date to the template
        # Example: October 02, 2026
        generated=date.today().strftime("%B %d, %Y"),

        # Pass the generated charts to the template
        charts=charts,

        # Pass the remaining JSON data to the template
        # This includes title, subtitle, kpis, columns, rows, etc.
        **data,
    )


    # Convert the generated HTML into a PDF
    pdf = HTML(string=html).write_pdf()


    # Create a Flask response containing the PDF
    resp = make_response(pdf)


    # Tell the browser/client that the response is a PDF
    resp.headers["Content-Type"] = "application/pdf"


    # Tell the browser that this should be downloaded as report.pdf
    resp.headers["Content-Disposition"] = (
        "attachment; filename=report.pdf"
    )


    # Send the PDF back to whoever called the API
    return resp

