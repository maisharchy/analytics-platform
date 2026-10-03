# Lets us convert the chart image into Base64 text
import base64

# Lets us create an in-memory file instead of saving an image to disk
import io

# Import Matplotlib so we can create charts
import matplotlib

# Use a non-GUI backend because this code runs in a server
matplotlib.use("Agg")

# Import pyplot, which gives us functions for creating charts
import matplotlib.pyplot as plt


# Main purple color used for the charts
PURPLE = "#4b2a85"

# Light purple color used for the filled area of the line chart
LIGHT = "#b79ce0"


# Convert a Matplotlib figure into a Base64 string
def _to_b64(fig):

    # Create an in-memory file for the PNG image
    buf = io.BytesIO()

    # Save the chart as a PNG inside the in-memory file
    # dpi=200 makes the image higher quality
    # bbox_inches="tight" removes unnecessary whitespace
    fig.savefig(
        buf,
        format="png",
        dpi=200,
        bbox_inches="tight"
    )

    # Close the chart after saving it to free memory
    plt.close(fig)

    # Get the PNG data from the in-memory file
    # Then convert the bytes into Base64 text
    return base64.b64encode(buf.getvalue()).decode()


# Apply common styling to a chart
def _style(ax, title):

    # Add a title to the chart
    # loc="left" puts the title on the left side
    # fontsize=11 controls the title size
    # fontweight="bold" makes it bold
    # color="#222" makes it dark gray
    ax.set_title(
        title,
        loc="left",
        fontsize=11,
        fontweight="bold",
        color="#222"
    )

    # Hide the top and right borders of the chart
    ax.spines[["top", "right"]].set_visible(False)

    # Add a light horizontal grid
    ax.grid(axis="y", alpha=0.2)


# Create a bar chart
def bar_chart(labels, values, title):

    # Create a figure that is 6 inches wide and 3 inches tall
    fig, ax = plt.subplots(figsize=(6, 3))

    # Create the bars using the labels and values provided
    # PURPLE controls the bar color
    ax.bar(labels, values, color=PURPLE)

    # Apply our common chart styling
    _style(ax, title)

    # Convert the chart to a Base64 string and return it
    return _to_b64(fig)


# Create a line chart
def line_chart(labels, values, title):

    # Create a figure that is 6 inches wide and 3 inches tall
    fig, ax = plt.subplots(figsize=(6, 3))

    # Create x-axis positions based on how many labels we have
    # Example: 5 labels -> 0, 1, 2, 3, 4
    x = range(len(labels))

    # Draw the line using the values
    # linewidth controls how thick the line is
    # marker="o" adds a circle at each data point
    ax.plot(
        x,
        values,
        color=PURPLE,
        linewidth=2.5,
        marker="o"
    )

    # Fill the area underneath the line
    # alpha=0.3 makes the fill partially transparent
    ax.fill_between(
        x,
        values,
        color=LIGHT,
        alpha=0.3
    )

    # Tell Matplotlib where the x-axis labels should go
    ax.set_xticks(list(x))

    # Replace 0, 1, 2, 3... with labels like Mon, Tue, Wed...
    ax.set_xticklabels(labels)

    # Apply our common chart styling
    _style(ax, title)

    # Convert the chart to a Base64 string and return it
    return _to_b64(fig)