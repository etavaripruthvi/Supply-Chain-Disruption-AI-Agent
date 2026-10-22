# The Layman's Guide to the Supply Chain Disruption AI Agent
## Everything You Need to Know About This Project in Simple, Everyday Language

> **Target Audience:** Group members, non-technical managers, classmates, and anyone who wants to understand the project in 5 minutes without getting lost in complex equations or coding jargon.

---

## 1. The 30-Second Elevator Pitch

Imagine you run an electrical home appliances factory in **Chakan, Pune** (**Meridian Home Appliances Pvt Ltd**), manufacturing **26 Lakh ceiling fans, air coolers, mixer grinders, and water heaters** every year, generating **₹364 Crore in revenue**.

If a single supplier in Ahmedabad fails to deliver **powder coating paint (worth just ₹345/kg)** or a Taiwanese supplier delays an **imported shipment of plastic resin (ABS)**, **the entire assembly line stops dead**. Workers sit idle, 184 machine stations halt, customer shipments miss deadlines, and the factory burns **₹22 Lakhs every single hour** the plant is down.

Today, factories find out about missing parts **the day the delivery is missed**—when it is already too late to fix. 

**Our project built an intelligent AI Operations Agent** that looks at deliveries, warehouse stock, factory schedules, and vendor finances to spot supply chain disasters **3 to 5 weeks before they hit the factory floor**. Even better, it doesn't just sound an alarm—it automatically diagnoses what went wrong, writes an official warning letter to the vendor, and drafts an emergency backup order plan for the plant managers.

---

## 2. The Real Problem Explained Simply

### The "Rearview Mirror" Trap
Most manufacturing companies track suppliers using **monthly scorecard reports** (like OTIF - On-Time In-Full). 
* **The Analogy:** This is like driving a car forward by only looking in the rearview mirror. By the time the monthly report tells you a supplier's on-time delivery dropped to 70% last month, **the accident has already happened**. Factory lines are already idled, and customers are angry.

### The 3 Hidden Traps in Meridian's Factory:
1. **The "Boiling Frog" Delay:** A vendor rarely collapses overnight. In week 1, they are 1 day late. In week 3, they are 2 days late. In week 6, they are 6 days late. A human buyer managing 10 suppliers doesn't notice this subtle "creep" until the vendor completely stops shipping.
2. **The "Single Point of Failure" (Sole Sourcing):** 
   * In our Chakan plant, **Powder Coating (RW09)** is purchased from **only one vendor in the entire country** (**Ahmedabad Coatings & Powders, S09**). If that supplier faces a cash-flow crisis, **every single painted fan and cooktop line stops**.
3. **Information Silos:** 
   * The logistics team knows a container ship from Kaohsiung, Taiwan carrying ABS plastic resin (S08) is stuck at JNPT port.
   * The warehouse team knows the Chakan shelf has only **16 days of CRCA steel sheet (RW02)** left.
   * The factory team knows the peak summer fan assembly run starts next week.
   * **Problem:** None of these teams talk to each other in real-time. By the time they connect the dots, the factory runs completely out of parts.

---

## 3. How Our AI Solves This: The "Medical Health Checkup" Analogy

Think of our AI system like a **smart ICU monitoring system** for supply chains. Just as a doctor checks heart rate, oxygen levels, and blood pressure to detect an illness before a patient collapses, our AI monitors **4 vital signs** for every supplier:

| Vital Sign | What It Measures | In Simple Terms |
|:---|:---|:---|
| **1. Delivery Health (35%)** | *Pulse & Blood Pressure* | Are shipments starting to arrive late? Has the delay crept up over the last 60 days compared to their normal baseline? |
| **2. Inventory Runway (25%)** | *Oxygen Tank Level* | How many days of raw materials are left in the warehouse? If we only have 16 days of steel sheet left, but the supplier takes 18 days to deliver, we are in the "red zone". |
| **3. Factory Impact (20%)** | *Physical Stamina* | In the past, have this supplier's parts caused assembly lines in Chakan to slow down or produce defective finished fans/heaters? |
| **4. Supplier Financial Health (20%)** | *Underlying Illness* | Is the vendor running out of cash? Are they an uncertified broker or located in an overseas trade corridor (e.g. Taiwan) facing delays? |

The AI combines all 4 vital signs into a single **Health Score from 0 to 100**:
* **0 to 29 (Green - Low Risk):** Healthy supplier (e.g., Kalinga Steels S01, Pune Coil S02, Deccan Aluminium S03, Mumbai Polymer S07). No human intervention needed.
* **30 to 49 (Yellow - Medium Risk):** Minor symptoms or high concentration (e.g., Vadodara Wires S05 supplying 33% of spend; Bhiwandi Packaging S10 sole sourcing). Vendor manager reviews within 2 weeks.
* **50 to 69 (Orange - High Risk):** Sick supplier (e.g., Coimbatore Magnet S06, Bharat Metal Traders S04, Pacific Plastics Taiwan S08). Procurement lead must intervene within 3 days.
* **70 to 100 (Red - Critical Risk):** Emergency! (e.g., Ahmedabad Coatings S09 sole-source powder coating failure). Plant Operations Manager and Head of Supply Chain must take emergency action **within 24 hours**.

---

## 4. The 4 "Digital Workers" Inside Our AI System

Instead of a single monolithic script, our system operates like an automated corporate team with 4 specialized AI agents working together:

```
[Agent 1: The Detective] ──> Continuously tracks shipments & catches subtle delay trends.
          │
          ▼
[Agent 2: The Judge]     ──> Calculates the 0-100 risk score & triggers safety overrides.
          │
          ▼
[Agent 3: The Doctor]    ──> (Generative AI) Diagnoses root cause & drafts vendor warning letters.
          │
          ▼
[Agent 4: The Dispatcher]──> Hands the task to the right manager with a ticking SLA countdown.
```

1. **Agent 1: The Telemetry Detective (Synthesizer Agent)**  
   * Constantly reads 3,200 shipment records, 10 raw material inventories, and 600 plant work orders.
   * Compares the last 60 days against the previous 120 days to see if performance is deteriorating.
2. **Agent 2: The Risk Judge (Scoring Engine)**  
   * Weighs all 4 vital signs.
   * **The Golden Safety Rule:** If a supplier is the *only* company that makes a part (sole source) AND their financial health score drops below 65 (like S09 Ahmedabad Coatings with score 58), this agent instantly overrides the math and forces the supplier into **CRITICAL risk**. No excuses.
3. **Agent 3: The Operations Doctor (LLM Generative Copilot)**  
   * Powered by Google Gemini / Generative AI.
   * When a vendor enters the danger zone, this agent doesn't just print an error code. It reads the full history and **writes real business documents in seconds**:
     * A formal **Root-Cause Analysis (RCA)** memo.
     * An official, professional **Vendor Breach & Cure Notice** (a legal warning letter ready to email to the supplier's CEO).
     * An **Internal Emergency Plan** telling the factory which secondary vendor to buy from and whether to pay for express freight.
4. **Agent 4: The Dispatcher (SLA Orchestrator)**  
   * Pushes the alert directly into an Action Queue.
   * Assigns a specific person (e.g., Plant Manager or Category Lead) with a strict deadline (**Within 24 Hours** or **Within 3 Days**).

---

## 5. The Key Numbers & What They Mean

When presenting to professors or managers, these are the 4 numbers you need to know:

### 1. 100% Disruption Recall (Sensitivity)
* **What it means:** Out of 10 suppliers, there were 4 emerging, troubled disruptions (S09, S06, S04, S08). **Our AI caught all 4 of them (4 out of 4)**.
* **Why it matters:** In factory operations, a "False Negative" (missing a failing supplier) causes an entire assembly line to shut down. 100% recall means **zero missed line-down crises**.

### 2. 100% Precision
* **What it means:** When the AI rings the alarm bell and says *"This supplier is about to fail"*, it was right **100% of the time**. It gave zero false alarms across the entire portfolio.
* **Why it matters:** If an AI gives false alarms every day, managers will ignore it (the "boy who cried wolf" problem). 100% precision means managers can trust every alert.

### 3. ₹4,196.8 Lakhs (₹41.97 Crore) Spend-at-Risk
* **What it means:** Out of our company's total ₹16,158 Lakhs (₹161.6 Crore) yearly raw material purchasing budget, ₹4,196.8 Lakhs (about 26.0%) was tied up with suppliers entering the danger zone. The AI pinpoints exactly where the company's money is vulnerable.

### 4. ₹3.08 Crore ($370,000) Cost Avoidance
* **What it means:** Catching these 4 troubled suppliers 3 to 5 weeks early prevented an estimated **140 hours of idle factory line stoppage**. Since factory downtime costs ₹22 Lakhs per hour, the system saved the business over ₹3 Crore in pure waste.

---

## 6. Guided Tour of the 7 Web App Screens

The project includes a working web application (`http://localhost:8501`). Here is what each screen does in plain English:

1. **📊 Executive KPI Command Center**:  
   The "CEO Dashboard". Shows total company revenue (₹363.9 Cr), raw material spend (₹161.6 Cr), spend at risk (₹41.97 Cr), the 100% detection rate, and a chart proving that troubled suppliers were getting worse for 9 months while normal suppliers stayed steady.
2. **🎯 Supplier Disruption Radar**:  
   The "Drill-Down Screen". Lets you pick any supplier (like `S09 Ahmedabad Coatings` or `S08 Pacific Plastics`) and see a diamond-shaped radar chart showing exactly which vital sign is failing (Delivery vs Inventory vs Factory vs Health).
3. **📦 Inventory & Buffer Watch**:  
   The "Warehouse Runway Screen". Shows every raw material SKU (RW01–RW10) with red bars showing how many days of stock are left compared to the blue bars showing how long the supplier takes to deliver. Highlights `REORDER NOW` for CRCA steel sheet and ABS granules.
4. **🤖 Autonomous Mitigation Copilot**:  
   The "AI Doctor Screen". You select an at-risk supplier and click the button. The AI immediately authors a 3-part action plan: Root-Cause Analysis, an official warning letter to the vendor, and internal re-routing instructions.
5. **🧪 What-If Scenario Simulator**:  
   The "Stress-Test Sandbox". You can move sliders to simulate a 4-day shipping delay spike, a 30% Taiwan tariff increase, or a 25% summer fan demand surge. The screen instantly recalculates the entire portfolio in real time.
6. **📋 Action Queue & SLA Tracker**:  
   The "To-Do List". Shows all open emergencies, who owns them (Plant Manager, Category Lead), their deadline, and lets you download a clean spreadsheet (`.csv`).
7. **📈 Ground Truth & Model Audit**:  
   The "Proof of Accuracy Screen". Shows the Confusion Matrix proving the 100% recall and 100% precision against real benchmark data.

---

## 7. How to Explain This Project in 60 Seconds (Viva / Interview Script)

If anyone asks you: *"What did your group do for IA-3?"*, recite this:

> *"We tackled Problem 8: Supply Chain Disruption Prediction for Meridian Home Appliances Pvt Ltd, an electrical appliance manufacturer in Chakan, Pune producing 26 Lakh appliances annually with ₹364 Crore in revenue.  
> 
> The core business problem is that manufacturing companies discover supplier delays too late, causing assembly lines to shut down at a cost of ₹22 Lakhs per hour.  
> 
> We built an end-to-end AI operations system that monitors four vital signs across deliveries, warehouse inventory, factory output, and supplier finances. Our algorithm caught 100% of emerging disruptions 3 to 5 weeks in advance across 10 suppliers and 10 raw materials.  
> 
> Furthermore, we built a Generative AI copilot that automatically writes vendor cure notices and backup routing plans, saving ₹3.08 Crore in prevented downtime. We also built an interactive web application with a live What-If stress-testing simulator."*

---

## 8. Quick Glossary of Common Terms

* **JIT (Just-in-Time):** A manufacturing strategy where parts arrive only a few days or hours before they are needed to save warehouse space. Very efficient, but very fragile.
* **Lead Time:** How many days it takes from the moment you place an order until the truck arrives at your factory.
* **Days of Cover (Runway):** How many days the factory can keep operating using only the inventory currently sitting on the warehouse shelf.
* **Sole Source:** A part that can only be purchased from one specific supplier in the country/world (like S09 for powder coating). Highest risk.
* **OTIF (On-Time In-Full):** The traditional metric measuring whether a shipment arrived on the agreed date with the full quantity.
* **SLA (Service Level Agreement):** The mandatory time limit a manager has to fix a problem (e.g., within 24 hours).
* **Recall:** The percentage of actual problems the AI caught (Our score: 100%).
* **Precision:** How often the AI's alarm is an actual problem rather than a false alarm (Our score: 100%).

---
*Created for the MBA AI Agents & Autonomous Business Operations Project Team | Meridian Home Appliances Case*
