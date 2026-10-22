"""Capture high-resolution screenshots of the running Streamlit app across all navigation pages."""
import time
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "output", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1600,1100")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

print("Initializing Edge WebDriver...")
driver = webdriver.Edge(options=options)

try:
    print("Navigating to http://localhost:8501...")
    driver.get("http://localhost:8501")
    time.sleep(5)  # Wait for Streamlit WebSocket to load

    # 1. Executive Dashboard
    print("Capturing Executive KPI Command Center...")
    driver.save_screenshot(os.path.join(FIG_DIR, "screenshot_dashboard.png"))

    # Navigation options by substring match
    nav_labels = [
        ("Supplier Disruption Radar", "screenshot_radar.png"),
        ("Inventory & Buffer Watch", "screenshot_inventory.png"),
        ("Autonomous Mitigation Copilot", "screenshot_mitigation.png"),
        ("What-If Scenario Simulator", "screenshot_simulator.png"),
        ("Action Queue & SLA Tracker", "screenshot_action_queue.png"),
        ("Ground Truth & Model Audit", "screenshot_model_audit.png"),
    ]

    for label_sub, filename in nav_labels:
        try:
            print(f"Finding tab matching: {label_sub}...")
            labels = driver.find_elements(By.TAG_NAME, "label")
            clicked = False
            for lbl in labels:
                if label_sub in lbl.text:
                    driver.execute_script("arguments[0].scrollIntoView(true);", lbl)
                    driver.execute_script("arguments[0].click();", lbl)
                    clicked = True
                    break
            
            if clicked:
                time.sleep(3.5)  # Wait for page re-render
                out_path = os.path.join(FIG_DIR, filename)
                driver.save_screenshot(out_path)
                print(f"Saved: {filename}")
            else:
                print(f"Could not find label matching {label_sub}")
        except Exception as e:
            print(f"Error capturing {label_sub}: {e}")

finally:
    driver.quit()
    print("All screenshots captured successfully!")
