#!/usr/bin/env python3
"""
Timer med GUI, pauser och flera aktiviteter
-------------------------------------------
GUI-app med Tkinter för att:
- Starta och stoppa timers för flera aktiviteter
- Pausa/fortsätta timers
- Logga varje aktivitet i en CSV-fil med meddelande, varaktighet, datum och starttid

Loggfil med tidinmatningar: timer_log.csv
"""

import csv
import time
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

LOG_FILE = Path(__file__).with_name("timer_log.csv")

class Timer:
    def __init__(self, message):
        self.message = message
        self.start_time = None
        self.paused_time = 0
        self.running = False
        self.pause_start = None

    def start(self):
        self.start_time = time.time()
        self.running = True

    def pause(self):
        if self.running and not self.pause_start:
            self.pause_start = time.time()
            self.running = False

    def resume(self):
        if self.pause_start:
            self.paused_time += time.time() - self.pause_start
            self.pause_start = None
            self.running = True

    def stop(self):
        if self.pause_start:
            self.resume()
        self.running = False
        return time.time() - self.start_time - self.paused_time


def initialise_log():
    if not LOG_FILE.exists():
        with LOG_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["meddelande", "varaktighet", "datum", "klockslag"])


def format_duration(seconds):
    return str(timedelta(seconds=int(seconds)))


def log_entry(message, duration):
    now = datetime.now()
    with LOG_FILE.open("a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            message,
            format_duration(duration),
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        ])


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer")

        self.timers = {}

        self.tree = ttk.Treeview(root, columns=("message", "status"), show="headings")
        self.tree.heading("message", text="Meddelande")
        self.tree.heading("status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Starta ny timer", command=self.start_timer).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Pausa", command=self.pause_timer).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Fortsätt", command=self.resume_timer).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Stoppa", command=self.stop_timer).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Visa logg", command=self.show_log).pack(side=tk.LEFT, padx=5)

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for msg, timer in self.timers.items():
            if timer.pause_start:
                status = "Pausad"
            elif timer.running:
                status = "Pågår"
            else:
                status = "Stoppad"
            self.tree.insert("", tk.END, iid=msg, values=(msg, status))

    def start_timer(self):
        msg = simpledialog.askstring("Meddelande", "Vad vill du tajma?")
        if msg and msg not in self.timers:
            t = Timer(msg)
            t.start()
            self.timers[msg] = t
            self.refresh_tree()
        elif msg in self.timers:
            messagebox.showerror("Fel", "Timer med detta meddelande finns redan.")

    def pause_timer(self):
        self._act_on_selected("pause")

    def resume_timer(self):
        self._act_on_selected("resume")

    def stop_timer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ingen vald", "Välj en aktivitet först.")
            return
        msg = selected[0]
        timer = self.timers.get(msg)
        if timer and (timer.running or timer.pause_start):
            duration = timer.stop()
            log_entry(msg, duration)
            messagebox.showinfo("Klart", f"'{msg}' loggades ({format_duration(duration)})")
            del self.timers[msg]
            self.refresh_tree()

    def _act_on_selected(self, action):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ingen vald", "Välj en aktivitet först.")
            return
        msg = selected[0]
        timer = self.timers.get(msg)
        if timer:
            if action == "pause":
                timer.pause()
            elif action == "resume":
                timer.resume()
            self.refresh_tree()

    def show_log(self):
        if not LOG_FILE.exists():
            messagebox.showinfo("Logg", "Ingen logg finns ännu.")
            return
        top = tk.Toplevel(self.root)
        top.title("Logg")
        text = tk.Text(top, height=20, width=60)
        text.pack()
        with LOG_FILE.open("r", encoding="utf-8") as f:
            for line in f:
                text.insert(tk.END, line)
        text.config(state="disabled")


def main():
    initialise_log()
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
