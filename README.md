# 📈Time Series Generator (DGP Simulation)

Welcome to the **Time Series Generator** — an interactive tool for creating custom time series data using a fully configurable **Data Generating Process (DGP)**.

Whether you're a student learning about time series, a researcher testing forecasting models, or a developer building demos — this tool gives you full control to simulate realistic or experimental data.

---

## 🧠 What is a Data Generating Process (DGP)?

A **Data Generating Process (DGP)** is a way of describing how data comes to life — it's the combination of all the underlying patterns, rules, and randomness that produce the numbers we observe over time.

In time series data, the DGP typically includes:

* 📉 **Trend** – a long-term pattern like steady growth or decline
* 🌤️ **Seasonality** – repeating cycles (e.g. monthly spikes)
* 🎲 **Noise** – random variation and unpredictability

Think of the DGP as the invisible machine behind your data — it shapes how your series behaves, even if you can't see it directly.

With this app, you’re not just generating data — you’re designing your own DGP by adjusting the trend, seasonality, and noise to simulate countless real-world scenarios.

---

## ⚙️ Features Overview

From basic simulations to advanced customization:

* 📈 Simulate trend, seasonality, and noise components with your own values
* 🔁 Choose between absolute or relative seasonality and noise dynamics
* 📊 Visualize individual components using toggle checkboxes
* 📐 Select from a variety of built-in trend types (linear, exponential, wavy, etc.)
* 🎚️ Adjust trend parameters interactively using sliders (e.g. slope, frequency)
* 💾 Download generated data as a CSV file
* 🧠 Smart caching avoids regenerating the same data unnecessarily
* 🎨 Beautiful UI with clean design and Bootstrap styling
* 🧪 Experiment endlessly by tweaking values and watching real-time updates

---

## 🎯 Suggested Value Ranges

Use these values as starting points for generating clear and realistic simulations:

| 📌 Trend Type             | 📉 Trend   | 🌤️ Seasonality | 🎲 Noise   |
| ------------------------- | ---------- | --------------- | ---------- |
| Linear / Piecewise        | 100 – 300  | 500 – 1500      | 100 – 1000 |
| Exponential / Logarithmic | 500 – 1000 | 200 – 600       | 200 – 400  |
| Wavy                      | 50 – 150   | 200 – 400       | 100 – 200  |
| Polynomial                | 0.05 – 10  | 5 – 200         | 5 – 50     |
| Recovery                  | 0.05 – 0.9 | 5 – 30          | 5 – 20     |

---

## 🌐 Live Demo

You can try the tool directly in your browser:

👉 **[Launch the Time Series Generator](https://time-series-generator.onrender.com/)**

No installation needed — just open the link and start exploring!

---

## 🚀 Running the App Locally

### 🧱 Requirements

Make sure you have:

* Python 3.7+
* `pip` installed

### 📦 Install dependencies

Clone the repo and install packages:

`pip install -r requirements.txt`

### ▶️ Run in Debug Mode (for development)

Open `app.py` and **replace this line**:

`app.run(host='0.0.0.0', port=8000)`

**with this line**:

`app.run(debug=True)`

Then run the app:

`python app.py`

The app should open automatically in your browser at:

[http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 🧪 Notebook Included for Testing & Exploration

This project comes with a **Jupyter notebook** to help you:

* Interactively test the DGP function
* Experiment with different parameter combinations
* Visualize results in code before using the UI
* Prototype ideas for forecasting models or transformations

---

## 🙋‍♂️ Author

Made with ❤️ by **Ali Adel**

🔗 [LinkedIn](https://www.linkedin.com/in/ali-adel-84b390101/)

---

## 📃 License

This project is open-source and free to use for educational and personal purposes.
