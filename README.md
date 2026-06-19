```markdown
# 🧠 MindShare — Making Invisible Mental Work Visible

> In every household, every team, every relationship — there's work that everyone sees... and work that nobody notices. 
    MindShare makes it visible.

## 🎯 The Problem

Someone cooked dinner. That's **visible** ✅

But who:
- 👻 Planned what to cook?
- 👻 Checked what ingredients were available?
- 👻 Made the grocery list?
- 👻 Considered dietary restrictions?
- 👻 Bought the ingredients?
- 👻 Cleaned up after?

**One visible task. Five invisible ones.** And they almost always fall on the same person.

This invisible mental load — the planning, scheduling, tracking, worrying, coordinating — is real, exhausting, and almost always unequally distributed. But it's never been measurable.

**Until now.**

---

## 💡 What MindShare Does

MindShare is a guided, interactive tool that:

1. **Logs daily activities** for each person in a household or team
2. **Auto-classifies** every activity as visible or invisible work using a keyword engine
3. **Uncovers hidden tasks** behind visible ones through intelligent follow-up questions
4. **Calculates the IRI** (Invisible Responsibility Index) — showing who carries the mental load
5. **Tracks patterns** across multiple days
6. **Visualizes the imbalance** with interactive charts and fairness scoring
7. **Simulates rebalancing** with a What-If tool

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/ankkits/Mindshare.git
cd mindshare
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` if executed locally

### Dependencies (`requirements.txt`)

```
streamlit>=1.36.0
pandas>=2.0.0
altair>=5.0.0
```

Three packages. That's it. Zero API keys. Zero external services.

---

## 🔄 Complete User Flow

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: CONTEXT                                            │
│  Pick: 🏠 Household  💼 Project Team  👶 New Parents        │
│  Sets context-specific activity suggestions                 │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: PEOPLE                                             │
│  Enter names: "Sarah, Mike, Grandma"                        │
│  Minimum 2 people required                                  │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: DATE                                               │
│  Pick the day being logged                                  │
│  Previously logged dates are blocked                        │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: DAILY LOG (per person)                             │
│  ████░░░░░░  Person 1 of 3: Sarah                           │
│                                                             │
│  Quick-pick from suggestions:                               │
│  ☑ Cooked dinner           ☐ Drove kids to school           │
│  ☑ Scheduled dentist       ☐ Bought groceries               │
│                                                             │
│  Or type your own: [_________________________]              │
│  Mental weight: [████████░░ 8]                              │
│                                                             │
│  Sarah's activities so far:                                 │
│  1. Cooked dinner (weight: 8)                     [🗑️]      │
│  2. Scheduled dentist (weight: 7)                 [🗑️]      │
│                                                             │
│  [← Previous]                    [Next Person →]            │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: HIDDEN WORK DETECTOR                               │
│  ███░░░░░░  Topic 1 of 3: Cooking                           │
│                                                             │
│  Triggered by:                                              │
│  - Sarah — "Cooked dinner"                                  │
│  - Mike — "Cooked lunch"                                    │
│                                                             │
│  Who planned what to cook?            [Sarah        ▼]      │
│  Who made the grocery list?           [Sarah        ▼]      │
│  Who bought the ingredients?          [Mike         ▼]      │
│  Who considered dietary restrictions? [Sarah        ▼]      │
│  Who cleaned up after?                [Nobody/Skip  ▼]      │
│                                                             │
│  [Save & Next →]         [Skip This Topic →]                │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 5B: DAY COMPLETE                                      │
│  ✅ Day logged: 2025-01-06                                  │
│  - 12 activities logged                                     │
│  - 8 hidden tasks uncovered                                 │
│  - 1 day(s) total                                           │
│                                                             │
│  [📅 Log Another Day]      [📊 Go to Analysis]              │
└─────────────────────┬───────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: ANALYSIS DASHBOARD                                 │
│  Full interactive dashboard with all charts and metrics     │
│  (See Dashboard Features section below)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Step-by-Step Details

### Step 1: Choose Context

Pick a scenario that matches your situation:

| Context | Description | Example Suggestions |
|---------|-------------|-------------------|
| 🏠 **Household** | Daily household and family responsibilities | Cooked dinner, Planned weekly meals, Drove kids to school, Worried about finances |
| 💼 **Project Team** | Work and team collaboration | Wrote code, Planned sprint backlog, Followed up with client, Tracked blockers |
| 👶 **New Parents** | Newborn and early parenting | Night feeding, Researched sleep training, Scheduled checkup, Worried about milestones |

The context determines which **activity suggestions** appear during logging. It does not affect classification or analysis.

### Step 2: Enter Names

Enter the names of everyone involved, separated by commas.

- Minimum 2 people required
- Names are used throughout the app for logging, follow-ups, and analysis
- Examples: "Sarah, Mike" or "Mom, Dad, Grandma" or "Priya, Marcus, Lena, Sam"

### Step 3: Pick a Date

- Select the day you're logging activities for
- You can log multiple days and compare them over time
- Previously logged dates are blocked to prevent duplicates
- If you've already logged days, you can skip straight to analysis

### Step 4: Log Activities

For each person, log everything they did that day:

**Quick-Pick Suggestions:**
- Context-specific checkboxes for common activities
- Select multiple at once with a single mental weight
- Already-added activities auto-hide from the list
- Counter shows remaining suggestions

**Type Your Own:**
- Free text input for anything not in the suggestions
- Individual mental weight slider per activity
- Activities are auto-classified by the keyword engine

**Mental Weight Scale:**
- 1 = Barely a thought
- 5 = Moderate effort
- 10 = Consumed your mind all day
- Self-reported — no right or wrong answer

**Activity Management:**
- 🗑️ Delete button per activity
- Running count of activities per person
- Full log preview for all people

### Step 5: Hidden Work Detection

After logging, MindShare scans all activities and identifies those with hidden work behind them.

**How it works:**
1. Activities are matched against follow-up trigger keywords
2. Matching activities are **grouped by topic** (Cooking, Transportation, Medical, etc.)
3. Each topic's questions are asked **only once** — even if multiple people triggered them
4. For each hidden task, you assign who handled it or skip it

**Example:**

Sarah logged "Cooked dinner" and Mike logged "Made lunch". Both trigger the **Cooking** group, but these questions appear only once:
- Who planned what to cook? → Sarah
- Who made the grocery list? → Sarah
- Who bought the ingredients? → Mike
- Who considered dietary restrictions? → Sarah
- Who cleaned up after? → Mike

Each assigned task becomes an **invisible activity** with a default mental weight, added to that person's load.

**Follow-up Topic Groups:**

| Group | Triggered By | Questions Asked |
|-------|-------------|----------------|
| Cooking | cook, bake, make dinner | 6 questions |
| Grocery Shopping | grocery, buy food, store | 5 questions |
| Medical Appointments | doctor, dentist, checkup | 6 questions |
| School & Education | school, homework, field trip | 6 questions |
| Cleaning | clean, vacuum, mop | 4 questions |
| Laundry | laundry, fold, iron | 5 questions |
| Celebrations & Gifts | birthday, gift, party | 5 questions |
| Repairs & Maintenance | fix, repair, plumber | 5 questions |
| Transportation | drive, drop off, pick up | 4 questions |
| Childcare | daycare, babysitter, nanny | 5 questions |
| Software Development | deploy, build, code | 5 questions |
| Bills & Finances | pay bill, mortgage, utilities | 4 questions |
| Pet Care | walk dog, vet, feed pet | 4 questions |
| Travel & Vacation | travel, flight, hotel, pack | 6 questions |
| School Lunches | pack lunch, lunchbox | 4 questions |
| Bathing Kids | bathe, bath time | 4 questions |
| Trash & Recycling | trash, garbage, recycling | 4 questions |
| Homework Help | homework, school work | 5 questions |
| Documentation | documentation, wrote docs | 4 questions |

### Step 5B: Day Complete

After hidden work detection, you see a summary:
- Number of activities logged
- Number of hidden tasks uncovered
- Total days logged so far

**Two options:**
- 📅 **Log Another Day** — clears current day data, goes back to date picker
- 📊 **Go to Analysis** — see the full dashboard

### Step 6: Analysis Dashboard

Full interactive dashboard with filters, charts, and insights. See the complete feature list below.

---

## 📊 Dashboard Features

### Summary Banner

| Metric | Description |
|--------|-------------|
| Days Logged | Total number of days in the analysis |
| Total Activities | All logged + hidden tasks combined |
| Visible | Count of visible (Execution) tasks |
| Invisible | Count of invisible (Planning, Scheduling, etc.) tasks |
| Hidden Uncovered | Tasks surfaced through follow-up questions |

Plus a color-coded callout:
- 🔴 > 60% invisible: "The majority of effort is unseen"
- 🟡 40–60% invisible: "A significant hidden burden"
- 🟢 < 40% invisible: "A relatively balanced split"

### IRI (Invisible Responsibility Index)

**Metric Cards:** Each person's IRI percentage with deviation from fair share and status emoji.

**Donut Chart:** "Who Carries the Load?" — proportional mental weight distribution.

**Horizontal Bar Chart:** IRI % per person with a **red dashed fair-share line** for visual comparison.

### Fairness Analysis

| Metric | Description |
|--------|-------------|
| Fair Share per Person | 100% ÷ number of people |
| Disparity Score | Standard deviation of IRI values |

Per-person breakdown:
```
Sarah — IRI: 68.2% (+18.2% from fair share) 🔴 Overburdened
Mike  — IRI: 31.8% (−18.2% from fair share) ⚪ Underloaded
```

### Daily Mental Load Trend (Multi-day only)

**Line chart** showing total mental weight per person per day. Reveals patterns like:
- Is one person consistently higher?
- Are there spikes on certain days?
- Is it getting more balanced over time?

### IRI Trend Over Time (Multi-day only)

**Line chart** showing each person's IRI % per day with a **red dashed fair-share reference line**. Shows whether the load distribution is improving or worsening.

### Day-by-Day Comparison Table (Multi-day only)

| Date | Person | Tasks | Invisible | Mental Weight | IRI (%) |
|------|--------|-------|-----------|---------------|---------|
| 2025-01-06 | Sarah | 8 | 6 | 47 | 65.3 |
| 2025-01-06 | Mike | 5 | 1 | 25 | 34.7 |
| 2025-01-07 | Sarah | 7 | 5 | 42 | 61.8 |
| 2025-01-07 | Mike | 6 | 2 | 26 | 38.2 |

### Disparity Trend (Multi-day only)

**Bar chart** — disparity score per day, color-coded:
- 🟢 Green: < 10 (balanced)
- 🟡 Orange: 10–20 (moderate imbalance)
- 🔴 Red: > 20 (highly unequal)

Answers the question: **"Is it getting more balanced over time?"**

### Before vs After: Hidden Work Impact

**Side-by-side donut charts:**
- **Before:** IRI based only on logged activities
- **After:** IRI including hidden tasks uncovered through follow-ups

**Shift table:**

| Person | Before IRI (%) | After IRI (%) | Shift |
|--------|---------------|---------------|-------|
| Sarah | 52.0 | 68.2 | +16.2 |
| Mike | 48.0 | 31.8 | −16.2 |

Plus a callout: *"Sarah's share increased by 16.2pp once hidden work was accounted for."*

### Visible vs Invisible Work

**Two charts side by side:**
1. **Stacked bar (normalized):** Proportion of visible vs invisible work per person
2. **Grouped bar:** Raw count of visible vs invisible activities per person

Color-coded: 🟢 Green = Visible, 🔴 Red/Orange = Invisible

### Mental Load by Category

**Two charts side by side:**
1. **Heatmap:** Person × Category grid, color intensity = mental weight
2. **Grouped bar chart:** Mental weight per category per person

Categories: Planning, Scheduling, Coordination, Monitoring, Emotional Labor, Execution

### Who Does What?

**Expandable card per person** showing:
- Visible task count
- Invisible task count
- Invisible percentage
- Full activity table sorted by mental weight

### Heaviest Mental Load Activities

**Horizontal bar chart** — top 10 activities by mental weight, color-coded by person. Tooltips show date, category, visibility.

### What-If Rebalancer

**Interactive tool** inside an expander:
- Every activity listed with current assignment
- Dropdown to reassign each activity to a different person
- **Live comparison table** showing current IRI vs new IRI and the change
- **Disparity metric** showing current vs new disparity score

### Insight Report

Auto-generated bullet points:
- Total days and activities recorded
- Who carries the highest load and by how much
- Who carries the least
- Percentage of invisible work
- Number of hidden tasks uncovered
- Heaviest category
- Disparity score with rating

### Data Export

- 📥 **Download Full Data** — all activities with date, person, category, visibility, weight
- 📥 **Download IRI Report** — per-person IRI summary

### Sidebar (during analysis)

- **Filters:** Users, Categories, Dates
- **Log Another Day** button
- **Start Over** button
- Context, people, and completed dates displayed

---

## 🧠 Intelligence Engine

MindShare uses a **keyword-based classification engine** — no AI, no APIs, no external services.

### How Classification Works

```
User types: "Cooked dinner"
                ↓
Code does: "cooked dinner".lower() → "cooked dinner"
                ↓
Checks CLASSIFICATION_RULES:
  Does "cooked dinner" contain "cook"? → YES
  Return: Category = "Execution", Visibility = "Visible"
                ↓
Checks FOLLOW_UP_RULES:
  Does "cooked dinner" contain "cook"? → YES
  Return: "Cooking" group with 6 follow-up questions
```

It's `if keyword in text` — works anywhere Python runs. No internet needed.

### Auto-Classification Examples

| You Type | Matched Keyword | Category | Visibility |
|----------|----------------|----------|------------|
| "Cooked dinner" | `cook` | Execution | Visible |
| "Planned weekly meals" | `plan` | Planning | Invisible |
| "Scheduled a doctor appointment" | `schedule`, `appointment` | Scheduling | Invisible |
| "Worried about finances" | `worry` | Emotional Labor | Invisible |
| "Drove kids to school" | `drive to` | Execution | Visible |
| "Tracked blockers across teams" | `track` | Monitoring | Invisible |
| "Followed up with client" | `follow up` | Coordination | Invisible |
| "Wrote code or built a feature" | `code`, `build` | Execution | Visible |
| "Mediated a disagreement" | `mediate` | Emotional Labor | Invisible |
| "Bought groceries" | `buy`, `grocery` | Execution | Visible |
| "Made the grocery list" | `plan` (via "made") | Planning | Invisible |
| "Called the plumber" | `call`, `plumber` | Coordination | Invisible |
| "Remembered someone's birthday" | `remember`, `birthday` | Monitoring | Invisible |

**Fallback:** Unrecognized activities default to **"Uncategorized / Invisible"** — the safe assumption is that unrecognized work is likely invisible.

### Classification Categories

| Category | Keywords (examples) | Typically |
|----------|-------------------|-----------|
| **Planning** | plan, decide, research, compare, choose, evaluate | Invisible |
| **Scheduling** | schedule, book, appointment, reserve, sign up, calendar | Invisible |
| **Coordination** | coordinate, follow up, call, email, delegate, negotiate | Invisible |
| **Monitoring** | track, monitor, check, review, remember, make sure, verify | Invisible |
| **Emotional Labor** | worry, comfort, support, listen, mediate, soothe, encourage | Invisible |
| **Execution** | cook, clean, wash, drive, buy, build, deploy, fix, code | Visible |

### What It Handles Well

| Input | Result |
|-------|--------|
| "Cooked dinner" | ✅ Execution/Visible + Cooking follow-ups |
| "I cooked pasta for the family" | ✅ Same — `cook` found |
| "Made dinner for everyone" | ✅ `made dinner` matched |
| "Scheduled the dentist" | ✅ Scheduling/Invisible + Medical follow-ups |
| "Called the plumber about the leak" | ✅ Coordination/Invisible + Repairs follow-ups |
| "Worried about baby's development" | ✅ Emotional Labor/Invisible |

### What It Won't Handle

| Input | Problem | Fallback |
|-------|---------|----------|
| "Made food" | No keyword match for generic phrasing | Uncategorized/Invisible |
| "Handled the kitchen situation" | Too vague | Uncategorized/Invisible |
| "Took care of dinner" | No keyword match | Uncategorized/Invisible |

The fallback is **safe** — defaulting to invisible is the right bias for this app.

---

## 📐 Key Metrics — Detailed

### Invisible Responsibility Index (IRI)

```
IRI (%) = (Person's Total Mental Weight ÷ Everyone's Total Mental Weight) × 100
```

**Example:**
- Sarah's total weight: 68
- Mike's total weight: 32
- Total: 100
- Sarah's IRI: 68%
- Mike's IRI: 32%

A higher IRI means that person carries a disproportionate share of the mental load.

### Fairness Deviation

```
Fair Share = 100% ÷ Number of People
Deviation = Person's IRI (%) − Fair Share (%)
```

**Example (2 people):**
- Fair share: 50%
- Sarah's deviation: 68% − 50% = +18% → 🔴 Overburdened
- Mike's deviation: 32% − 50% = −18% → ⚪ Underloaded

| Deviation Range | Status | Meaning |
|----------------|--------|---------|
| > +15% | 🔴 Overburdened | Carrying far more than fair share |
| +5% to +15% | 🟡 Slightly High | Somewhat above fair share |
| −5% to +5% | 🟢 Balanced | Roughly equal distribution |
| < −5% | ⚪ Underloaded | Carrying less than fair share |

### Disparity Score

```
Disparity = Standard Deviation of all IRI values
```

| Score | Rating | Meaning |
|-------|--------|---------|
| 0 | Perfect | Exactly equal distribution |
| < 10 | 🟢 Balanced | Minor differences |
| 10–20 | 🟡 Moderate | Noticeable imbalance |
| > 20 | 🔴 Severe | Highly unequal distribution |

---

## 📁 Project Structure

```
mindshare/
├── app.py               ← Complete Streamlit application (single file)
├── requirements.txt     ← Python dependencies (3 packages)
└── README.md            ← Documentation
```

## ⚠️ Important Disclaimers

### About Mental Weight Scores
Mental weight is a **self-reported score** reflecting how mentally heavy an activity *felt* to the person logging it. It is **not** an objective measure. There is no right or wrong answer. Planning dinner might be a 3 for one person and an 8 for another depending on context, stress, and cognitive load. The scale:
- 1 = Barely a thought
- 5 = Moderate mental effort
- 10 = Consumed your thoughts all day

### About Hidden Task Weights
Hidden tasks uncovered through follow-up questions use **estimated default weights** (typically 3–7). These provide reasonable relative values for comparison but are not based on clinical research or validated datasets.

### About Data Persistence
All data lives in **Streamlit session state** — it persists while your browser tab is open but is **lost** when you close the tab, refresh the page, or the session times out. Use the CSV download feature to save your data.

### About Classification Accuracy
The keyword engine covers ~150 common activity patterns. Unusual or very vague phrasing may not be recognized and will default to "Uncategorized / Invisible". This is by design — the safe assumption is that unrecognized work is likely invisible.

### Overall
**MindShare surfaces patterns, not precise measurements.** It is a tool for **awareness and conversation**, not clinical assessment or legal evidence.


*Built for Engineering the unseen 2026*

<p align="center">
  <strong>You can't fix what you can't see.</strong><br>
  MindShare gives you the data to start the conversation.
</p>
```

