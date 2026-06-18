🧹 Chore-Share App

A light-hearted interactive app that raises awareness about the gender gap in unpaid household work — and helps you split chores fairly and playfully between partners!

Built with ❤️ using Streamlit, Plotly, and Pandas.
🎯 Purpose

Women consistently spend more time on household chores than men — often unpaid and unnoticed. 

Use it to raise awareness, inspire conversations and build empathy.

📊 Visualization

The main graph is a grouped bar chart built using Plotly Express. It compares the average time spent on various household tasks by:

    🧍‍♀️ Women

    🧍 Men

It includes:

    Side-by-side bars for each chore category (e.g., cooking, cleaning, childcare)

    A visible gap showing where time imbalance exists

    A total time summary and difference display

Data Source: 

This dataset is artificially generated to simulate global trends in unpaid household work. It does not represent any specific country or official source, but aims to reflect patterns commonly reported in international surveys.

🎮 How to Play: The Chore Split Game

Scroll down in the app to find the "Your Fair Chore Plan" section:

    Enter your names (e.g., Alice and Bob)

    Use sliders to indicate how much time each person has available for chores

    The app calculates a fair share of chores based on time availability and shows:

        Chore-by-chore breakdown

        Who might owe dessert 😄

        Celebratory balloons if the split is fair!

This feature encourages empathy and teamwork in a fun and gamified way.
🛠️ Tech Stack

    Streamlit – for building the interactive web UI

    Plotly – for rich, interactive visualizations

    Pandas – for data manipulation and analysis

    Python 3.8+ compatible

📦 Python Packages

Here’s the list of required packages (included in requirements.txt):

streamlit
pandas
plotly

Install them using:

pip install -r requirements.txt
📁 Project Structure

chore-share-app/
├── app.py ← main Streamlit application
├── chores.csv ← sample dataset with chore data
├── requirements.txt ← dependencies
└── README.md ← this file
🚀 How to Run

    Clone the repository or download the ZIP

    Install requirements:

    pip install -r requirements.txt

    Launch the app:

    streamlit run app.py

    The app will open at http://localhost:8501