import matplotlib
import matplotlib.pyplot as plt

from server.helpers.db import DBHelper

FILE_PATH = "piantina.png"


def generate_chart_report(date_from, date_to):
    data = DBHelper.get_report_data(date_from, date_to)

    timestamps = []
    temperature = []
    humidity = []
    dryness = []
    light = []
    for item in data:
        timestamps.append(item["timestamp"].strftime("%d/%m %H"))
        temperature.append(item["temperature"])
        humidity.append(item["humidity"])
        dryness.append(item["dryness"])
        light.append(item["light"])

    matplotlib.use("agg")
    plt.plot(timestamps, temperature, "-g", label="temperature", linewidth=2)
    plt.plot(timestamps, humidity, "-b", label="humidity", linewidth=2)
    plt.plot(timestamps, dryness, "-r", label="dryness", linewidth=2)
    plt.plot(timestamps, light, "-y", label="light", linewidth=2)
    plt.legend()
    plt.savefig(FILE_PATH)

    return FILE_PATH
