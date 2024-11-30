import pywhatkit as kit
import datetime
import tkinter as tk
from tkinter import ttk, StringVar, messagebox
import time
import threading
import queue
import os

# Global stop flag
stop_flag = False

# Queue for thread-safe communication
message_queue = queue.Queue()

# Directory to save logs
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def log_results(results):
    """Log results to a file."""
    log_file = os.path.join(LOG_DIR, f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(log_file, "w") as file:
        file.write("\n".join(results))
    return log_file


def send_message_with_logging(participant, message):
    """Send a message and return the status."""
    try:
        current_time = datetime.datetime.now()
        scheduled_time = current_time + datetime.timedelta(minutes=2)  # Schedule 2 minutes from now
        hour, minute = scheduled_time.hour, scheduled_time.minute

        # Ensure we're not crossing into the next hour
        if minute >= 60:
            hour += 1
            minute -= 60

        kit.sendwhatmsg(participant, message, hour, minute, wait_time=15, tab_close=True, close_time=2)
        return f"Message sent to {participant}."
    except Exception as e:
        return f"Failed to send message to {participant}: {e}"

def start_sending(progress_bar, percent_var, result_label, participants, instructor, message, main_frame, progress_frame):
    """Simulate message sending with a progress bar and return to main screen."""
    global stop_flag
    total_tasks = len(participants) + (1 if instructor else 0)
    step = 100 / total_tasks

    results = []
    completed = 0
    for participant in participants:
        if stop_flag:  # Check if the operation should stop
            message_queue.put("STOPPED")
            break

        participant = participant.strip()
        if participant:
            result = send_message_with_logging(participant, message)
            results.append(result)
            completed += 1
            progress_bar['value'] += step
            percent_var.set(f"{int((completed / total_tasks) * 100)}%")
            result_label.update()
            time.sleep(0.5)  # Simulate time delay for better user feedback

    if not stop_flag and instructor:
        result = send_message_with_logging(instructor, message)
        results.append(result)
        completed += 1
        progress_bar['value'] += step
        percent_var.set(f"{int((completed / total_tasks) * 100)}%")
        result_label.update()
        time.sleep(0.5)

    if not stop_flag:
        # Show results if not stopped 
        log_file = log_results(results)
        message_queue.put(f"COMPLETED:{log_file}")
    else:
        message_queue.put("STOPPED")

    stop_flag = False


def update_ui():
    """Update the UI with latest results."""
    try:
        if not message_queue.empty():
            message = message_queue.get_nowait()
            result_label.config(text=message)

            if message.startswith("COMPLETED"):
                _, log_file = message.split(":")
                messagebox.showinfo("Results", f"Messages sent successfully! Log saved to {log_file}.")
            elif message == "STOPPED":
                messagebox.showinfo("Stopped", "Messages sending process stopped.")
            main_frame.tkraise()
            progress_bar['value'] = 0
            percent_var.set("0%")
    except queue.Empty:
        pass

    root.after(100, update_ui)  # Schedule the next UI update


def send_messages():
    """Handle sending messages and transition to progress bar."""
    global stop_flag
    participants = participants_entry.get().split(',')
    instructor = instructor_entry.get().strip()
    message = message_entry.get("1.0", tk.END).strip()

    if not message:
        messagebox.showerror("Error", "Message cannot be empty.")
        return

    # Transition to progress frame
    progress_frame.tkraise()

    # Start sending messages in a separate thread
    stop_flag = False
    threading.Thread(target=start_sending, args=(progress_bar, percent_var, progress_label, participants, instructor, message, main_frame, progress_frame)).start()

    # Start UI update loop
    update_ui()


def stop_operation():
    """Stop the ongoing operation."""
    global stop_flag
    stop_flag = True


# Main UI setup
root = tk.Tk()  # Ensure root is defined
root.title("WhatsApp Message Sender")

def on_closing():
    """Handle the window close event."""
    global stop_flag
    if  stop_flag:
        if messagebox.askyesno("Quit", "Messages are still being sent. Do you want to stop and exit?"):
            stop_flag = True
        else:
            return
    else:
        if messagebox.askyesno("Quit", "Are you sure you want to exit?"):
            root.destroy()

# Attach the handler to the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)


# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

tk.Label(main_frame, text="Participants (comma-separated):").pack(pady=5)
participants_entry = tk.Entry(main_frame, width=50)
participants_entry.pack(pady=5)

tk.Label(main_frame, text="Instructor's phone number:").pack(pady=5)
instructor_entry = tk.Entry(main_frame, width=50)
instructor_entry.pack(pady=5)

tk.Label(main_frame, text="Message:").pack(pady=5)
message_entry = tk.Text(main_frame, height=5, width=50)
message_entry.pack(pady=5)

send_button = tk.Button(main_frame, text="Send Messages", command=send_messages)
send_button.pack(pady=10)

# Progress frame setup
progress_frame = tk.Frame(root)
progress_frame.pack(fill="both", expand=True)

percent_var = StringVar(value="0%")
progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=10)

percent_label = tk.Label(progress_frame, textvariable=percent_var)
percent_label.pack(pady=5)

# Define result_label to display messages or status updates
result_label = tk.Label(progress_frame, text="Status will appear here.", wraplength=300, justify="center")
result_label.pack(pady=5)

progress_label = tk.Label(progress_frame, text="Sending messages...")
progress_label.pack(pady=5)

stop_button = tk.Button(progress_frame, text="Stop", command=stop_operation)
stop_button.pack(pady=10)

# Start with the main frame
main_frame.tkraise()

root.mainloop()
