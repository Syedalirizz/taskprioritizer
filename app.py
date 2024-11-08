import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state to hold tasks
if "task_list" not in st.session_state:
    st.session_state.task_list = []

# Function to calculate priority score (urgency + importance)
def calculate_priority(task):
    try:
        # Calculate days left until the deadline
        deadline = datetime.strptime(task['deadline'], "%Y-%m-%d")
        days_left = (deadline - datetime.now()).days
    except:
        days_left = 0  # Default to 0 if no deadline

    # Return a score based on urgency (days left) and importance (importance level)
    return days_left * task['importance']

# Streamlit UI
st.title("Task Prioritizer")
st.write("Enter your tasks, deadlines, and importance levels to prioritize them!")

# Input fields for tasks
with st.form(key="task_form"):
    task_name = st.text_input("Task Name")
    deadline = st.date_input("Deadline")
    importance = st.slider("Importance (1 to 5)", 1, 5)
    
    add_task_button = st.form_submit_button("Add Task")
    
    if add_task_button:
        # Add the task to the session state task list
        st.session_state.task_list.append({
            'task_name': task_name,
            'deadline': deadline.strftime('%Y-%m-%d'),
            'importance': importance
        })
        st.success(f"Task '{task_name}' added successfully!")

# Display entered tasks if any
if st.session_state.task_list:
    df = pd.DataFrame(st.session_state.task_list)
    df['priority'] = df.apply(calculate_priority, axis=1)
    df = df.sort_values(by='priority', ascending=False)

    st.subheader("Prioritized Tasks")
    
    # Display tasks in a table with better styling
    st.write(df[['task_name', 'deadline', 'importance', 'priority']].style.format({'priority': "{:.0f}"}))
else:
    st.write("No tasks added yet. Add tasks to get started.")

