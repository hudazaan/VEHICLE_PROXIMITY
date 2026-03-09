import sqlite3
import time
import csv

class IncidentDB:
    def __init__(self):
        import os
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        self.conn = sqlite3.connect("logs/adas_incidents.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS incidents 
                            (id INTEGER PRIMARY KEY, timestamp TEXT, object_type TEXT, 
                             confidence REAL, distance_est TEXT)''')
        self.conn.commit()

    def save_incident(self, obj_type, conf, dist):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO incidents (timestamp, object_type, confidence, distance_est) VALUES (?, ?, ?, ?)", 
                            (ts, obj_type, conf, dist))
        self.conn.commit()

    def export_to_csv(self):
        """
        Converts the SQLite database into a CSV report.
        """
        output_path = "logs/forensic_report.csv"
        try:
            # newest data at the top
            self.cursor.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
            rows = self.cursor.fetchall()
            
            headers = [description[0] for description in self.cursor.description]
            
            # using 'w' mode ensures the old 2026-03-05 data is DELETED first
            with open(output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers) 
                writer.writerows(rows)   
                
            print(f"--- New Forensic Report Created with {len(rows)} entries ---")
        except Exception as e:
            print(f"--- ERROR EXPORTING CSV: {e} ---")