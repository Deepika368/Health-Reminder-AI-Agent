
import csv
import os
from datetime import datetime

import streamlit as st

FILE = "medicines.csv"
FIELDS = ["medicine", "time", "notes"]

st.set_page_config(
    page_title="Health Reminder AI Agent",
    page_icon="💊",
    layout="centered"
)


def load_medicines():
    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_medicines(medicines):
    with open(FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(medicines)


st.title("💊 Health Reminder AI Agent")
st.write("Manage your medicine schedule in one place.")

now = datetime.now()
st.info("Current time: " + now.strftime("%I:%M %p"))

medicines = load_medicines()

st.subheader("➕ Add a medicine")

with st.form("medicine_form"):
    medicine = st.text_input("Medicine name")
    time = st.time_input("Reminder time")
    notes = st.text_input("Notes (optional)")

    submitted = st.form_submit_button("Save medicine")

    if submitted:
        if not medicine.strip():
            st.error("Please enter a medicine name.")
        else:
            medicines.append({
                "medicine": medicine.strip(),
                "time": time.strftime("%H:%M"),
                "notes": notes.strip()
            })
            save_medicines(medicines)
            st.success("Medicine schedule saved!")
            st.rerun()


st.subheader("📋 Your medicine schedule")

medicines = load_medicines()

if medicines:
    for index, item in enumerate(medicines):
        st.write(
            f"**{index + 1}. {item['medicine']}** "
            f"— {item['time']}"
        )
        if item.get("notes"):
            st.caption(item["notes"])

        if st.button("Delete", key=f"delete_{index}"):
            medicines.pop(index)
            save_medicines(medicines)
            st.rerun()
else:
    st.write("No medicines added yet.")

st.subheader("⏰ Reminder checker")

if st.button("Check reminders now"):
    current_time = datetime.now().strftime("%H:%M")
    due = [
        item for item in load_medicines()
        if item["time"] == current_time
    ]

    if due:
        for item in due:
            st.warning(
                f"Reminder: {item['medicine']} is scheduled now."
            )
    else:
        st.info("No medicine is scheduled for this exact minute.")

st.subheader("🤖 Health Information Assistant")

question = st.text_input(
    "Ask a general health question",
    placeholder="Example: How can I build a healthy routine?"
)

if st.button("Get general guidance"):
    if question.strip():
        st.write(
            "Your question: " + question.strip()
        )
        st.write(
            "General guidance: Maintain a regular sleep schedule, "
            "stay hydrated, eat balanced meals, and consult a "
            "qualified healthcare professional for personal advice."
        )
        st.caption(
            "This is a basic demo assistant, not an AI medical diagnosis."
        )
    else:
        st.warning("Please enter a question.")