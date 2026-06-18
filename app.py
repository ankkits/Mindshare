import streamlit as st
import pandas as pd
import altair as alt

# ============================================================
# PAGE CONFIG
# ============================================================
try:
    st.set_page_config(page_title="MindShare", page_icon="🧠", layout="wide")
except st.errors.StreamlitAPIException:
    pass

# ============================================================
# INTELLIGENCE ENGINE
# ============================================================
CLASSIFICATION_RULES = [
    (["plan", "decide", "research", "compare", "figure out", "think about",
      "look into", "explore options", "brainstorm", "strategize", "prioritize",
      "choose", "evaluate", "consider"], "Planning", "Invisible"),
    (["schedule", "book", "appointment", "reserve", "rsvp", "sign up",
      "register", "enroll", "set up time", "calendar", "remind", "reschedule",
      "cancel appointment", "arrange"], "Scheduling", "Invisible"),
    (["coordinate", "follow up", "call", "email", "text", "message",
      "check in", "confirm", "organize", "delegate", "ask", "negotiate",
      "communicate", "notify", "inform", "reach out", "contact"], "Coordination", "Invisible"),
    (["track", "monitor", "check", "review", "keep an eye", "notice",
      "remember", "make sure", "verify", "update list", "inventory",
      "watch for", "observe", "log", "maintain list"], "Monitoring", "Invisible"),
    (["worry", "comfort", "support", "listen", "encourage", "reassure",
      "manage feelings", "mediate", "calm down", "soothe", "emotional",
      "stress about", "anxiety", "cope", "counsel", "apologize",
      "smooth things over", "de-escalate", "cheer up"], "Emotional Labor", "Invisible"),
    (["cook", "clean", "wash", "vacuum", "mop", "scrub", "dust",
      "laundry", "iron", "fold", "dishes", "trash", "garbage",
      "mow", "garden", "water plants", "fix", "repair", "assemble",
      "install", "paint", "build", "hang", "organize closet",
      "declutter", "sweep", "wipe"], "Execution", "Visible"),
    (["feed", "bathe", "diaper", "dress", "drop off", "pick up",
      "drive to", "play with", "read to", "help with homework",
      "pack lunch", "put to bed", "night feeding", "tummy time",
      "change clothes"], "Execution", "Visible"),
    (["buy", "shop", "pick up", "get groceries", "go to store",
      "return item", "drop off", "deliver", "carry", "load",
      "unload", "pack", "unpack", "move"], "Execution", "Visible"),
    (["implement", "code", "write code", "design", "build feature",
      "deploy", "test", "debug", "present", "demo", "write report",
      "submit", "file", "send report"], "Execution", "Visible"),
    (["pay bill", "pay rent", "transfer money", "deposit",
      "file taxes"], "Execution", "Visible"),
    (["budget", "compare prices", "find deals", "research cost",
      "financial plan", "savings plan", "insurance"], "Planning", "Invisible"),
]

FOLLOW_UP_RULES = [
    (["cook", "cooked", "make dinner", "make lunch", "make breakfast",
      "prepare meal", "bake", "made dinner", "made lunch", "made breakfast"],
     "Cooking",
     [
         ("Planned what to cook", "Planning", 6),
         ("Checked what ingredients were available", "Monitoring", 4),
         ("Made the grocery list", "Planning", 5),
         ("Bought the ingredients", "Execution", 4),
         ("Considered dietary preferences and allergies", "Emotional Labor", 5),
         ("Cleaned up after the meal", "Execution", 3),
     ]),
    (["grocery", "groceries", "buy food", "get groceries", "shop for food",
      "went to store", "go to store"],
     "Grocery Shopping",
     [
         ("Tracked what was running low at home", "Monitoring", 5),
         ("Planned meals for the week", "Planning", 7),
         ("Made the shopping list", "Planning", 5),
         ("Compared prices or found coupons", "Planning", 4),
         ("Organized and put away the groceries", "Execution", 3),
     ]),
    (["doctor", "pediatrician", "dentist", "appointment", "checkup",
      "check-up", "vaccination", "therapist", "specialist", "vet"],
     "Medical Appointments",
     [
         ("Remembered it was time for this appointment", "Monitoring", 5),
         ("Researched and chose the provider", "Planning", 6),
         ("Called to schedule the appointment", "Scheduling", 5),
         ("Arranged time off work or childcare", "Coordination", 6),
         ("Prepared paperwork or insurance info", "Planning", 5),
         ("Will follow up on results or next steps", "Coordination", 5),
     ]),
    (["school", "homework", "school form", "parent-teacher", "pta",
      "school event", "school project", "field trip"],
     "School & Education",
     [
         ("Reads the school emails and newsletters", "Monitoring", 5),
         ("Tracks assignment due dates", "Monitoring", 6),
         ("Communicates with teachers", "Coordination", 5),
         ("Arranges supplies or materials", "Planning", 4),
         ("Signs permission slips and forms", "Coordination", 3),
         ("Coordinates with other parents", "Coordination", 5),
     ]),
    (["clean", "vacuum", "mop", "scrub", "tidy", "declutter", "organize"],
     "Cleaning",
     [
         ("Noticed it needed to be cleaned", "Monitoring", 4),
         ("Keeps track of cleaning supplies", "Monitoring", 3),
         ("Sets the standard for cleanliness", "Emotional Labor", 5),
         ("Plans the overall cleaning schedule", "Planning", 4),
     ]),
    (["laundry", "wash clothes", "fold", "iron", "did laundry"],
     "Laundry",
     [
         ("Noticed the hamper was full", "Monitoring", 3),
         ("Keeps track of detergent and supplies", "Monitoring", 3),
         ("Sorted the clothes properly", "Planning", 3),
         ("Put the clean clothes away", "Execution", 3),
         ("Remembers seasonal clothing swaps for kids", "Planning", 5),
     ]),
    (["birthday", "gift", "present", "party", "celebration", "event", "holiday"],
     "Celebrations & Gifts",
     [
         ("Remembered the date", "Monitoring", 5),
         ("Planned what gift to buy", "Planning", 5),
         ("Researched and purchased the gift", "Planning", 5),
         ("Coordinated the celebration logistics", "Coordination", 6),
         ("Sent the RSVP or thank-you note", "Coordination", 4),
     ]),
    (["fix", "repair", "plumber", "electrician", "handyman",
      "maintenance", "broken", "leaking"],
     "Repairs & Maintenance",
     [
         ("First noticed the problem", "Monitoring", 4),
         ("Researched how to fix it or who to call", "Planning", 5),
         ("Got quotes and scheduled the repair", "Coordination", 6),
         ("Arranged to be home for the technician", "Scheduling", 5),
         ("Followed up to make sure it was done right", "Coordination", 4),
     ]),
    (["drive", "drop off", "pick up", "carpool", "transport", "drove"],
     "Transportation",
     [
         ("Coordinates the overall schedule", "Coordination", 6),
         ("Arranged the carpool or backup plan", "Coordination", 5),
         ("Tracks extracurricular timing", "Monitoring", 5),
         ("Communicates with other parents about logistics", "Coordination", 4),
     ]),
    (["daycare", "babysitter", "nanny", "childcare", "sitter"],
     "Childcare",
     [
         ("Researched childcare options", "Planning", 7),
         ("Scheduled tours and interviews", "Scheduling", 6),
         ("Handles enrollment paperwork", "Coordination", 5),
         ("Communicates daily with the provider", "Coordination", 5),
         ("Has the backup plan when childcare falls through", "Planning", 7),
     ]),
    (["deploy", "implement", "build", "code", "design", "launch", "ship", "release"],
     "Software Development",
     [
         ("Defined the requirements", "Planning", 7),
         ("Broke down the work into tasks", "Planning", 6),
         ("Coordinated dependencies across teams", "Coordination", 7),
         ("Tracked progress and blockers", "Monitoring", 6),
         ("Communicated status to stakeholders", "Coordination", 5),
     ]),
    (["pay bill", "pay rent", "mortgage", "utilities", "insurance payment"],
     "Bills & Finances",
     [
         ("Tracks all the due dates", "Monitoring", 5),
         ("Set up autopay or reminders", "Planning", 4),
         ("Reviews statements for errors", "Monitoring", 4),
         ("Budgets and ensures sufficient funds", "Planning", 6),
     ]),
    (["walk dog", "feed pet", "vet", "groom", "pet care"],
     "Pet Care",
     [
         ("Scheduled the vet appointment", "Scheduling", 5),
         ("Tracks vaccination and medication schedules", "Monitoring", 5),
         ("Buys pet food and supplies", "Planning", 4),
         ("Arranged pet care for vacations", "Coordination", 5),
     ]),
    (["travel", "vacation", "trip", "flight", "hotel", "pack", "suitcase"],
     "Travel & Vacation",
     [
         ("Researched the destination", "Planning", 6),
         ("Compared and booked flights or hotels", "Planning", 7),
         ("Planned the itinerary", "Planning", 7),
         ("Arranged care for pets, plants, or mail", "Coordination", 5),
         ("Packed for the kids", "Planning", 5),
         ("Prepared travel documents", "Planning", 4),
     ]),
]

CONTEXT_SUGGESTIONS = {
    "🏠 Household": {
        "description": "Daily household and family responsibilities",
        "visible": [
            "Cooked dinner",
            "Did laundry",
            "Cleaned the kitchen",
            "Drove kids to school",
            "Bought groceries",
            "Packed school lunches",
            "Fixed something in the house",
            "Took out the trash",
            "Bathed the kids",
            "Helped with homework",
        ],
        "invisible": [
            "Planned weekly meals",
            "Made the grocery list",
            "Scheduled a doctor appointment",
            "Coordinated carpool with other parents",
            "Tracked what supplies were running low",
            "Researched summer camps or activities",
            "Remembered someone's birthday or event",
            "Worried about finances",
            "Sorted school forms and emails",
            "Followed up with plumber or repair person",
        ],
    },
    "💼 Project Team": {
        "description": "Work and team collaboration responsibilities",
        "visible": [
            "Wrote code or built a feature",
            "Fixed a bug",
            "Deployed to staging or production",
            "Wrote unit or integration tests",
            "Designed a UI or flow",
            "Reviewed a pull request",
            "Gave a demo or presentation",
            "Wrote documentation",
            "Set up CI/CD pipeline",
            "Debugged a production issue",
        ],
        "invisible": [
            "Defined requirements or wrote user stories",
            "Planned the sprint backlog",
            "Scheduled meetings and standups",
            "Followed up with client on feedback",
            "Tracked blockers across teams",
            "Coordinated QA handoff",
            "Updated the project timeline",
            "Onboarded a new team member",
            "Mediated a disagreement between teammates",
            "Remembered to renew a license or subscription",
        ],
    },
    "👶 New Parents": {
        "description": "Newborn and early parenting responsibilities",
        "visible": [
            "Night feeding",
            "Changed diapers",
            "Bathed the baby",
            "Drove to pediatrician",
            "Sterilized bottles",
            "Played during tummy time",
            "Bought diapers and formula",
            "Assembled baby furniture",
            "Pumped and stored milk",
            "Put baby to bed",
        ],
        "invisible": [
            "Researched sleep training methods",
            "Scheduled a checkup or vaccination",
            "Tracked feeding and diaper log",
            "Coordinated with daycare",
            "Worried about developmental milestones",
            "Followed up on insurance claim",
            "Researched baby-safe products",
            "Planned what to pack in the baby bag",
            "Booked a mommy-and-me class",
            "Read a parenting book or article",
        ],
    },
}


def classify_activity(activity_text):
    text = activity_text.lower().strip()
    for keywords, category, visibility in CLASSIFICATION_RULES:
        for kw in keywords:
            if kw in text:
                return category, visibility
    return "Uncategorized", "Invisible"


def collect_unique_follow_ups(daily_log):
    """Deduplicate follow-ups by group across all activities."""
    seen_groups = {}
    for entry in daily_log:
        text = entry["activity"].lower().strip()
        for keywords, group_name, prompts in FOLLOW_UP_RULES:
            matched = False
            for kw in keywords:
                if kw in text:
                    matched = True
                    break
            if matched:
                if group_name not in seen_groups:
                    seen_groups[group_name] = {
                        "group_name": group_name,
                        "triggered_by": [],
                        "follow_ups": prompts,
                        "date": entry["date"],
                    }
                seen_groups[group_name]["triggered_by"].append(
                    f"{entry['user']} — \"{entry['activity']}\""
                )
                break
    return list(seen_groups.values())


# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "members": [],
    "daily_log": [],          # current day being logged
    "hidden_tasks": [],       # current day hidden tasks
    "all_days_data": [],      # ALL completed days (list of dicts)
    "all_days_hidden": [],    # ALL completed days hidden tasks
    "completed_dates": [],    # dates already logged
    "step": "setup",
    "context": "",
    "current_member_idx": 0,
    "follow_up_idx": 0,
    "log_date": "",
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================================
# HEADER
# ============================================================
st.title("🧠 MindShare")
st.caption("Making Invisible Mental Work Visible")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    if st.session_state.step not in ("setup",):
        st.markdown(f"**Context:** {st.session_state.context}")
        st.markdown(f"**People:** {', '.join(st.session_state.members)}")
        if st.session_state.log_date:
            st.markdown(f"**Current Date:** {st.session_state.log_date}")
        if st.session_state.completed_dates:
            st.markdown(f"**Days Logged:** {len(st.session_state.completed_dates)}")
            for d in st.session_state.completed_dates:
                st.markdown(f"- ✅ {d}")
        st.divider()
        if st.button("🔄 Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ============================================================
# STEP 1: CHOOSE CONTEXT
# ============================================================
if st.session_state.step == "setup":
    st.subheader("Step 1: What's the setting?")
    st.markdown("This helps us suggest common activities you might forget to mention.")

    context_cols = st.columns(len(CONTEXT_SUGGESTIONS))
    for i, (label, info) in enumerate(CONTEXT_SUGGESTIONS.items()):
        with context_cols[i]:
            st.markdown(f"**{label}**")
            st.caption(info["description"])
            if st.button("Select", key=f"ctx_{i}", use_container_width=True):
                st.session_state.context = label
                st.session_state.step = "members"
                st.rerun()
    st.stop()

# ============================================================
# STEP 2: WHO ARE THE PEOPLE
# ============================================================
if st.session_state.step == "members":
    st.subheader("Step 2: Who are the people?")

    context = st.session_state.context
    if context == "🏠 Household":
        st.markdown("Enter the names of everyone in your household.")
        placeholder = "e.g. Sarah, Mike, Grandma"
    elif context == "💼 Project Team":
        st.markdown("Enter the names of your team members.")
        placeholder = "e.g. Priya, Marcus, Lena, Sam"
    elif context == "👶 New Parents":
        st.markdown("Enter the names of all caregivers — parents, grandparents, anyone helping.")
        placeholder = "e.g. Mom, Dad, Grandma"
    else:
        st.markdown("Enter the names of the people involved.")
        placeholder = "e.g. Alice, Bob, Charlie"

    with st.form("members_form"):
        members_input = st.text_input(
            "Names (separated by commas)", placeholder=placeholder
        )
        members_submitted = st.form_submit_button("Continue →", use_container_width=True)

        if members_submitted:
            names = [n.strip() for n in members_input.split(",") if n.strip()]
            if len(names) >= 2:
                st.session_state.members = names
                st.session_state.step = "date"
                st.rerun()
            else:
                st.warning("Please enter at least 2 names.")

    if st.button("← Back"):
        st.session_state.step = "setup"
        st.rerun()
    st.stop()

# ============================================================
# STEP 3: PICK DATE
# ============================================================
if st.session_state.step == "date":
    st.subheader("Step 3: Which day are we logging?")
    st.markdown(f"**People:** {', '.join(st.session_state.members)}")

    if st.session_state.completed_dates:
        st.info(f"✅ You've already logged: {', '.join(st.session_state.completed_dates)}")

    with st.form("date_form"):
        log_date = st.date_input("Date")
        date_submitted = st.form_submit_button("Start Logging This Day →", use_container_width=True)

        if date_submitted:
            date_str = str(log_date)
            if date_str in st.session_state.completed_dates:
                st.warning(f"You already logged {date_str}. Pick a different date.")
            else:
                st.session_state.log_date = date_str
                st.session_state.daily_log = []
                st.session_state.hidden_tasks = []
                st.session_state.step = "log"
                st.session_state.current_member_idx = 0
                st.session_state.follow_up_idx = 0
                st.rerun()

    # If we have completed days, offer to skip to analysis
    if st.session_state.completed_dates:
        st.markdown("---")
        if st.button("📊 Skip to Analysis — I'm done logging days", use_container_width=True):
            st.session_state.step = "analyze"
            st.rerun()

    if not st.session_state.completed_dates:
        if st.button("← Back"):
            st.session_state.step = "members"
            st.rerun()
    st.stop()

# ============================================================
# STEP 4: DAILY LOG — one person at a time
# ============================================================
if st.session_state.step == "log":
    members = st.session_state.members
    current_idx = st.session_state.current_member_idx
    current_member = members[current_idx]
    context = st.session_state.context

    # Counter to reset checkbox keys after each bulk add
    counter_key = f"add_counter_{current_member}"
    if counter_key not in st.session_state:
        st.session_state[counter_key] = 0

    st.progress(
        current_idx / len(members),
        text=f"Day: {st.session_state.log_date} — Person {current_idx + 1} of {len(members)}",
    )

    st.subheader(f"What did **{current_member}** do on {st.session_state.log_date}?")
    st.markdown(
        "**Pick from common activities below**, or type your own at the bottom."
    )
    st.info(
        "💡 **About mental weight:** This is a self-reported score reflecting how mentally "
        "heavy an activity *felt* — not an objective measure. There's no right or wrong answer. "
        "Planning dinner might be a 3 for one person and an 8 for another depending on "
        "context, stress, and cognitive load. Trust your gut."
    )

        # ---- QUICK-PICK FROM SUGGESTIONS ----
    context_data = CONTEXT_SUGGESTIONS.get(context, {})
    all_hints = context_data.get("visible", []) + context_data.get("invisible", [])

    if all_hints:
        person_logged = set(
            e["activity"] for e in st.session_state.daily_log
            if e["user"] == current_member
        )
        available_hints = [h for h in all_hints if h not in person_logged]

        counter_key = f"add_counter_{current_member}"
        if counter_key not in st.session_state:
            st.session_state[counter_key] = 0
        add_round = st.session_state[counter_key]

        if available_hints:
            remaining = len(available_hints)
            with st.expander(f"📋 Pick from common activities ({remaining} remaining)", expanded=True):
                selected = []

                hint_cols = st.columns(2)
                for j, hint in enumerate(available_hints):
                    col = hint_cols[j % 2]
                    checked = col.checkbox(
                        hint,
                        key=f"hint_{current_member}_r{add_round}_{j}",
                        value=False,
                    )
                    if checked:
                        selected.append(hint)

                if selected:
                    st.markdown("---")
                    st.markdown(f"**{len(selected)} selected** — set the mental weight:")

                    bulk_weight = st.slider(
                        "Mental weight for selected activities",
                        1, 10, 5,
                        key=f"bulk_weight_{current_member}_r{add_round}",
                        help="1 = barely a thought, 5 = moderate effort, 10 = consumed your mind all day",
                    )

                    if st.button(
                        f"✅ Add {len(selected)} activities",
                        use_container_width=True,
                        key=f"add_bulk_{current_member}_r{add_round}",
                    ):
                        for hint in selected:
                            st.session_state.daily_log.append({
                                "date": st.session_state.log_date,
                                "user": current_member,
                                "activity": hint,
                                "mental_weight": bulk_weight,
                            })
                        st.session_state[counter_key] += 1
                        st.rerun()
        else:
            st.success(f"All suggested activities have been added for {current_member}! Use the text input below for anything else.")

        st.markdown("---")
    # ---- ALREADY LOGGED ----
    person_entries = [e for e in st.session_state.daily_log if e["user"] == current_member]
    if person_entries:
        st.markdown(f"**{current_member}'s activities so far ({len(person_entries)}):**")
        for j, e in enumerate(person_entries):
            col_act, col_del = st.columns([5, 1])
            col_act.markdown(f"{j+1}. {e['activity']}  _(weight: {e['mental_weight']})_")
            if col_del.button("🗑️", key=f"del_{current_member}_{j}"):
                remove_idx = None
                count = 0
                for k, entry in enumerate(st.session_state.daily_log):
                    if entry["user"] == current_member:
                        if count == j:
                            remove_idx = k
                            break
                        count += 1
                if remove_idx is not None:
                    st.session_state.daily_log.pop(remove_idx)
                    # Increment counter to reset checkboxes
                    st.session_state[counter_key] += 1
                st.rerun()
        st.markdown("---")

    # ---- TYPE YOUR OWN ----
    st.markdown("**Or type something not in the list:**")

    with st.form(f"log_{current_member}_{current_idx}", clear_on_submit=True):
        activity = st.text_input(
            "What did they do?",
            placeholder="e.g. Worried about finances, Researched summer camps",
        )
        weight = st.slider(
            "How mentally heavy was this? (1 = trivial, 10 = exhausting)",
            1, 10, 5,
        )
        add_submitted = st.form_submit_button(
            f"Add to {current_member}'s list", use_container_width=True
        )

        if add_submitted and activity.strip():
            st.session_state.daily_log.append({
                "date": st.session_state.log_date,
                "user": current_member,
                "activity": activity.strip(),
                "mental_weight": weight,
            })
            st.rerun()

    # ---- NAVIGATION ----
    st.markdown("---")
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

    if current_idx > 0:
        if nav_col1.button("← Previous Person"):
            st.session_state.current_member_idx -= 1
            st.rerun()

    person_entries = [e for e in st.session_state.daily_log if e["user"] == current_member]

    if current_idx < len(members) - 1:
        if nav_col3.button("Next Person →"):
            if person_entries:
                st.session_state.current_member_idx += 1
                st.rerun()
            else:
                st.warning(f"Add at least one activity for {current_member}.")
    else:
        if nav_col3.button("✅ Done with this day →"):
            if person_entries:
                st.session_state.step = "hidden"
                st.session_state.follow_up_idx = 0
                st.rerun()
            else:
                st.warning(f"Add at least one activity for {current_member}.")

    if st.session_state.daily_log:
        with st.expander("📋 Everyone's log so far"):
            st.dataframe(pd.DataFrame(st.session_state.daily_log), use_container_width=True)

    st.stop()

# ============================================================
# STEP 5: HIDDEN WORK — DEDUPLICATED BY GROUP
# ============================================================
if st.session_state.step == "hidden":

    unique_groups = collect_unique_follow_ups(st.session_state.daily_log)
    follow_up_idx = st.session_state.follow_up_idx

    if not unique_groups or follow_up_idx >= len(unique_groups):
        # Save this day's data to the all-days store
        st.session_state.all_days_data.extend(st.session_state.daily_log)
        st.session_state.all_days_hidden.extend(st.session_state.hidden_tasks)
        st.session_state.completed_dates.append(st.session_state.log_date)
        st.session_state.step = "day_done"
        st.rerun()

    # Guard in case rerun is slow
    if st.session_state.step != "hidden":
        st.stop()

    current_group = unique_groups[follow_up_idx]

    st.progress(
        follow_up_idx / len(unique_groups),
        text=f"Topic {follow_up_idx + 1} of {len(unique_groups)}: {current_group['group_name']}",
    )

    st.subheader(f"🔍 Hidden Work — {current_group['group_name']}")
    st.caption(f"Day: {st.session_state.log_date}")

    st.markdown("**These activities triggered this set of questions:**")
    for trigger in current_group["triggered_by"]:
        st.markdown(f"- {trigger}")

    st.markdown("---")
    st.markdown("**Who handled the invisible work behind this?**")

    members = st.session_state.members
    user_options = ["Nobody / Skip"] + members

    with st.form("follow_up_form"):
        assignments = {}
        for i, (task_desc, task_cat, task_weight) in enumerate(current_group["follow_ups"]):
            assignments[i] = st.selectbox(
                f"Who **{task_desc.lower()}**?",
                user_options,
                key=f"fup_{follow_up_idx}_{i}",
            )

        col_save, col_skip = st.columns(2)
        fup_submitted = col_save.form_submit_button("Save & Next →", use_container_width=True)
        fup_skipped = col_skip.form_submit_button("Skip This Topic →", use_container_width=True)

        if fup_submitted:
            for i, (task_desc, task_cat, task_weight) in enumerate(current_group["follow_ups"]):
                assigned = assignments[i]
                if assigned != "Nobody / Skip":
                    st.session_state.hidden_tasks.append({
                        "date": current_group["date"],
                        "user": assigned,
                        "activity": task_desc,
                        "mental_weight": task_weight,
                        "category": task_cat,
                        "visibility": "Invisible",
                        "source": current_group["group_name"],
                    })
            st.session_state.follow_up_idx += 1
            st.rerun()

        if fup_skipped:
            st.session_state.follow_up_idx += 1
            st.rerun()

    if st.session_state.hidden_tasks:
        with st.expander(f"🔎 Hidden tasks uncovered so far ({len(st.session_state.hidden_tasks)})"):
            hidden_preview = pd.DataFrame(st.session_state.hidden_tasks)
            st.dataframe(
                hidden_preview[["user", "activity", "category", "mental_weight", "source"]],
                use_container_width=True,
            )

    st.stop()

# ============================================================
# STEP 5B: DAY DONE — log another day or go to analysis
# ============================================================
if st.session_state.step == "day_done":

    st.subheader(f"✅ Day logged: {st.session_state.log_date}")

    day_entries = len(st.session_state.daily_log)
    day_hidden = len(st.session_state.hidden_tasks)
    st.markdown(f"- **{day_entries}** activities logged")
    st.markdown(f"- **{day_hidden}** hidden tasks uncovered")
    st.markdown(f"- **{len(st.session_state.completed_dates)}** day(s) total so far")

    st.markdown("---")

    col_another, col_analyze = st.columns(2)

    if col_another.button("📅 Log Another Day", use_container_width=True):
        st.session_state.daily_log = []
        st.session_state.hidden_tasks = []
        st.session_state.log_date = ""
        st.session_state.step = "date"
        st.rerun()

    if col_analyze.button("📊 Go to Analysis", use_container_width=True):
        st.session_state.step = "analyze"
        st.rerun()

    st.stop()

# ============================================================
# STEP 6: ANALYSIS DASHBOARD
# ============================================================
if st.session_state.step == "analyze":

    # Build dataframe from ALL days
    if not st.session_state.all_days_data:
        st.warning("No data to analyze. Go back and log some days.")
        if st.button("← Back to logging"):
            st.session_state.step = "date"
            st.rerun()
        st.stop()

    df = pd.DataFrame(st.session_state.all_days_data)
    classifications = df["activity"].apply(classify_activity)
    df["category"] = [c[0] for c in classifications]
    df["visibility"] = [c[1] for c in classifications]
    df["source"] = "Logged"

    if st.session_state.all_days_hidden:
        hidden_df = pd.DataFrame(st.session_state.all_days_hidden)
        df = pd.concat([df, hidden_df], ignore_index=True)

    df["visibility"] = df["visibility"].str.strip().str.title()
    df["user"] = df["user"].str.strip()
    df["category"] = df["category"].str.strip()

    # Sidebar filters
    with st.sidebar:
        st.header("🔍 Filters")
        all_users = sorted(df["user"].unique())
        selected_users = st.multiselect("Users", all_users, default=all_users)
        all_categories = sorted(df["category"].unique())
        selected_categories = st.multiselect("Categories", all_categories, default=all_categories)
        all_dates = sorted(df["date"].unique())
        selected_dates = st.multiselect("Dates", all_dates, default=all_dates)

        st.divider()
        if st.button("📅 Log Another Day", use_container_width=True):
            st.session_state.daily_log = []
            st.session_state.hidden_tasks = []
            st.session_state.log_date = ""
            st.session_state.step = "date"
            st.rerun()

    df = df[
        df["user"].isin(selected_users)
        & df["category"].isin(selected_categories)
        & df["date"].isin(selected_dates)
    ]

    if df.empty:
        st.warning("No data matches your current filters.")
        st.stop()

    # ---- SUMMARY BANNER ----
    total_tasks = len(df)
    visible_count = len(df[df["visibility"] == "Visible"])
    invisible_count = len(df[df["visibility"] == "Invisible"])
    hidden_found = len(st.session_state.all_days_hidden)
    num_days = df["date"].nunique()

    st.subheader("📊 The Big Picture")

    banner_cols = st.columns(5)
    banner_cols[0].metric("Days Logged", num_days)
    banner_cols[1].metric("Total Activities", total_tasks)
    banner_cols[2].metric("Visible", visible_count)
    banner_cols[3].metric("Invisible", invisible_count)
    banner_cols[4].metric("🔍 Hidden Uncovered", hidden_found)

    if total_tasks > 0:
        inv_pct = round(invisible_count / total_tasks * 100, 1)
        if inv_pct > 60:
            st.error(f"⚠️ **{inv_pct}%** of all work is invisible — the majority of effort is unseen.")
        elif inv_pct > 40:
            st.warning(f"**{inv_pct}%** of all work is invisible — a significant hidden burden.")
        else:
            st.success(f"**{inv_pct}%** of work is invisible — a relatively balanced split.")

    # ---- RAW DATA ----
    with st.expander("📋 View All Data"):
        st.dataframe(
            df[["date", "user", "activity", "category", "visibility", "mental_weight"]],
            use_container_width=True,
        )

    # ---- IRI (OVERALL) ----
    st.subheader("📊 Invisible Responsibility Index (IRI)")

    iri_df = df.groupby("user")["mental_weight"].sum().reset_index()
    total_weight = iri_df["mental_weight"].sum()
    iri_df["IRI (%)"] = (iri_df["mental_weight"] / total_weight * 100).round(1)

    n_users = len(iri_df)
    fair_share = round(100 / n_users, 1)
    iri_df["Deviation"] = (iri_df["IRI (%)"] - fair_share).round(1)
    iri_df["Status"] = iri_df["Deviation"].apply(
        lambda d: "🔴 Overburdened" if d > 15
        else ("🟡 Slightly High" if d > 5
        else ("🟢 Balanced" if d >= -5
        else "⚪ Underloaded"))
    )

    iri_cols = st.columns(n_users)
    for idx, row in iri_df.iterrows():
        with iri_cols[idx]:
            st.metric(
                row["user"],
                f"{row['IRI (%)']}%",
                delta=f"{row['Deviation']:+.1f}% from fair",
                delta_color="inverse",
            )
            st.caption(row["Status"])

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        iri_donut = (
            alt.Chart(iri_df)
            .mark_arc(innerRadius=60, stroke="#fff", strokeWidth=2)
            .encode(
                theta=alt.Theta("mental_weight:Q"),
                color=alt.Color("user:N", legend=alt.Legend(title="Person")),
                tooltip=["user", "mental_weight", "IRI (%)"],
            )
            .properties(title="Who Carries the Load?", height=350)
        )
        st.altair_chart(iri_donut, use_container_width=True)

    with chart_col2:
        iri_bar = (
            alt.Chart(iri_df)
            .mark_bar(cornerRadiusEnd=6)
            .encode(
                x=alt.X("IRI (%):Q", title="IRI %", scale=alt.Scale(domain=[0, 100])),
                y=alt.Y("user:N", title="", sort="-x"),
                color=alt.Color("user:N", legend=None),
                tooltip=["user", "IRI (%)", "Deviation"],
            )
        )
        fair_line = (
            alt.Chart(pd.DataFrame({"fair": [fair_share]}))
            .mark_rule(color="red", strokeDash=[4, 4], strokeWidth=2)
            .encode(x="fair:Q")
        )
        st.altair_chart(
            (iri_bar + fair_line).properties(title=f"IRI vs Fair Share ({fair_share}%)", height=350),
            use_container_width=True,
        )

    # ---- FAIRNESS ----
    st.subheader("⚖️ Fairness Analysis")

    disparity = iri_df["IRI (%)"].std().round(1)

    col_fair, col_disp = st.columns(2)
    col_fair.metric("Fair Share per Person", f"{fair_share}%")
    col_disp.metric("Disparity Score", f"{disparity}",
                    help="Std deviation of IRI. Lower = more equitable.")

    for _, row in iri_df.iterrows():
        st.markdown(
            f"**{row['user']}** — IRI: {row['IRI (%)']}% "
            f"({row['Deviation']:+.1f}% from fair share) {row['Status']}"
        )

    # ---- DAILY TREND TIMELINE ----
    if num_days > 1:
        st.subheader("📅 Daily Mental Load Trend")

        timeline_df = df.groupby(["date", "user"])["mental_weight"].sum().reset_index()

        line_chart = (
            alt.Chart(timeline_df)
            .mark_line(point=True, strokeWidth=3)
            .encode(
                x=alt.X("date:N", title="Date", sort=sorted(df["date"].unique())),
                y=alt.Y("mental_weight:Q", title="Total Mental Weight"),
                color=alt.Color("user:N", legend=alt.Legend(title="Person")),
                tooltip=["date", "user", "mental_weight"],
            )
            .properties(title="Mental Load Over Time", height=400)
        )
        st.altair_chart(line_chart, use_container_width=True)

        # ---- IRI PER DAY ----
        st.subheader("📈 IRI Trend Over Time")

        daily_iri_rows = []
        for date in sorted(df["date"].unique()):
            day_df = df[df["date"] == date]
            day_total = day_df["mental_weight"].sum()
            if day_total > 0:
                for user in day_df["user"].unique():
                    user_weight = day_df[day_df["user"] == user]["mental_weight"].sum()
                    daily_iri_rows.append({
                        "date": date,
                        "user": user,
                        "IRI (%)": round(user_weight / day_total * 100, 1),
                    })

        daily_iri_df = pd.DataFrame(daily_iri_rows)

        iri_trend = (
            alt.Chart(daily_iri_df)
            .mark_line(point=True, strokeWidth=3)
            .encode(
                x=alt.X("date:N", title="Date", sort=sorted(df["date"].unique())),
                y=alt.Y("IRI (%):Q", title="IRI %", scale=alt.Scale(domain=[0, 100])),
                color=alt.Color("user:N", legend=alt.Legend(title="Person")),
                tooltip=["date", "user", "IRI (%)"],
            )
        )
        iri_fair_line = (
            alt.Chart(pd.DataFrame({"fair": [fair_share]}))
            .mark_rule(color="red", strokeDash=[4, 4], strokeWidth=2)
            .encode(y="fair:Q")
        )
        st.altair_chart(
            (iri_trend + iri_fair_line).properties(
                title=f"IRI Per Day (red line = {fair_share}% fair share)",
                height=400,
            ),
            use_container_width=True,
        )

        # ---- DAY-BY-DAY COMPARISON TABLE ----
        st.subheader("📋 Day-by-Day Comparison")

        day_comparison_rows = []
        for date in sorted(df["date"].unique()):
            day_df = df[df["date"] == date]
            day_total_weight = day_df["mental_weight"].sum()
            for user in st.session_state.members:
                user_day = day_df[day_df["user"] == user]
                user_weight = user_day["mental_weight"].sum()
                user_tasks = len(user_day)
                user_invisible = len(user_day[user_day["visibility"] == "Invisible"])
                user_iri = round(user_weight / day_total_weight * 100, 1) if day_total_weight > 0 else 0
                day_comparison_rows.append({
                    "Date": date,
                    "Person": user,
                    "Tasks": user_tasks,
                    "Invisible": user_invisible,
                    "Mental Weight": user_weight,
                    "IRI (%)": user_iri,
                })

        day_comparison_df = pd.DataFrame(day_comparison_rows)
        st.dataframe(day_comparison_df, use_container_width=True)

        # ---- DISPARITY TREND ----
        st.subheader("📉 Disparity Trend")

        disparity_rows = []
        for date in sorted(df["date"].unique()):
            day_iris = daily_iri_df[daily_iri_df["date"] == date]["IRI (%)"]
            if len(day_iris) > 1:
                disparity_rows.append({
                    "date": date,
                    "Disparity": round(day_iris.std(), 1),
                })

        if disparity_rows:
            disparity_trend_df = pd.DataFrame(disparity_rows)

            disp_chart = (
                alt.Chart(disparity_trend_df)
                .mark_bar(cornerRadiusEnd=6)
                .encode(
                    x=alt.X("date:N", title="Date", sort=sorted(df["date"].unique())),
                    y=alt.Y("Disparity:Q", title="Disparity Score"),
                    color=alt.condition(
                        alt.datum.Disparity > 20,
                        alt.value("#FF5722"),
                        alt.condition(
                            alt.datum.Disparity > 10,
                            alt.value("#FF9800"),
                            alt.value("#4CAF50"),
                        ),
                    ),
                    tooltip=["date", "Disparity"],
                )
                .properties(title="Is it getting more balanced over time?", height=300)
            )
            st.altair_chart(disp_chart, use_container_width=True)

    # ---- BEFORE vs AFTER ----
    st.subheader("🔬 Before vs After: Hidden Work Impact")
    st.markdown("How the picture changes once invisible work is accounted for.")

    before_df = pd.DataFrame(st.session_state.all_days_data)
    before_iri = before_df.groupby("user")["mental_weight"].sum().reset_index()
    before_total = before_iri["mental_weight"].sum()
    before_iri["IRI (%)"] = (before_iri["mental_weight"] / before_total * 100).round(1)

    after_iri_simple = iri_df[["user", "IRI (%)"]].copy()

    ba_col1, ba_col2 = st.columns(2)

    with ba_col1:
        st.markdown("**Before (only logged tasks):**")
        before_donut = (
            alt.Chart(before_iri)
            .mark_arc(innerRadius=50, stroke="#fff", strokeWidth=2)
            .encode(
                theta=alt.Theta("mental_weight:Q"),
                color=alt.Color("user:N", legend=None),
                tooltip=["user", "IRI (%)"],
            )
            .properties(height=300)
        )
        st.altair_chart(before_donut, use_container_width=True)

    with ba_col2:
        st.markdown("**After (hidden work uncovered):**")
        after_donut = (
            alt.Chart(iri_df)
            .mark_arc(innerRadius=50, stroke="#fff", strokeWidth=2)
            .encode(
                theta=alt.Theta("mental_weight:Q"),
                color=alt.Color("user:N", legend=None),
                tooltip=["user", "IRI (%)"],
            )
            .properties(height=300)
        )
        st.altair_chart(after_donut, use_container_width=True)

    impact = before_iri[["user", "IRI (%)"]].rename(columns={"IRI (%)": "Before IRI (%)"}).merge(
        after_iri_simple.rename(columns={"IRI (%)": "After IRI (%)"}),
        on="user", how="outer",
    ).fillna(0)
    impact["Shift"] = (impact["After IRI (%)"] - impact["Before IRI (%)"]).round(1)
    st.dataframe(impact, use_container_width=True)

    if st.session_state.all_days_hidden and len(impact) > 0:
        biggest_shift = impact.loc[impact["Shift"].abs().idxmax()]
        direction = "increased" if biggest_shift["Shift"] > 0 else "decreased"
        st.info(
            f"**{biggest_shift['user']}**'s share {direction} by "
            f"{abs(biggest_shift['Shift'])}pp once hidden work was accounted for."
        )

    # ---- VISIBLE vs INVISIBLE ----
    st.subheader("👁️‍🗨️ Visible vs Invisible Work")

    vis_col1, vis_col2 = st.columns(2)
    visibility_df = df.groupby(["user", "visibility"]).size().reset_index(name="count")

    with vis_col1:
        vis_stacked = (
            alt.Chart(visibility_df)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("user:N", title=""),
                y=alt.Y("count:Q", title="Number of Activities", stack="normalize"),
                color=alt.Color(
                    "visibility:N",
                    scale=alt.Scale(domain=["Visible", "Invisible"], range=["#4CAF50", "#FF5722"]),
                    legend=alt.Legend(title="Type"),
                ),
                tooltip=["user", "visibility", "count"],
            )
            .properties(title="Proportion of Work Type", height=350)
        )
        st.altair_chart(vis_stacked, use_container_width=True)

    with vis_col2:
        vis_grouped = (
            alt.Chart(visibility_df)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("user:N", title=""),
                y=alt.Y("count:Q", title="Count"),
                color=alt.Color(
                    "visibility:N",
                    scale=alt.Scale(domain=["Visible", "Invisible"], range=["#4CAF50", "#FF5722"]),
                    legend=None,
                ),
                xOffset="visibility:N",
                tooltip=["user", "visibility", "count"],
            )
            .properties(title="Activity Count by Type", height=350)
        )
        st.altair_chart(vis_grouped, use_container_width=True)

    # ---- CATEGORY BREAKDOWN ----
    st.subheader("🗂️ Mental Load by Category")

    category_df = df.groupby(["user", "category"])["mental_weight"].sum().reset_index()

    cat_col1, cat_col2 = st.columns(2)

    with cat_col1:
        heatmap = (
            alt.Chart(category_df)
            .mark_rect(cornerRadius=4)
            .encode(
                x=alt.X("category:N", title=""),
                y=alt.Y("user:N", title=""),
                color=alt.Color("mental_weight:Q", scale=alt.Scale(scheme="orangered"), title="Weight"),
                tooltip=["user", "category", "mental_weight"],
            )
            .properties(title="Mental Load Heatmap", height=300)
        )
        st.altair_chart(heatmap, use_container_width=True)

    with cat_col2:
        cat_bar = (
            alt.Chart(category_df)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("category:N", title=""),
                y=alt.Y("mental_weight:Q", title="Mental Weight"),
                color="user:N",
                xOffset="user:N",
                tooltip=["user", "category", "mental_weight"],
            )
            .properties(title="Mental Load by Category", height=300)
        )
        st.altair_chart(cat_bar, use_container_width=True)

    # ---- WHO DOES WHAT ----
    st.subheader("👤 Who Does What?")

    for member in sorted(df["user"].unique()):
        member_df = df[df["user"] == member]
        member_visible = len(member_df[member_df["visibility"] == "Visible"])
        member_invisible = len(member_df[member_df["visibility"] == "Invisible"])
        member_total_weight = member_df["mental_weight"].sum()

        with st.expander(f"**{member}** — {len(member_df)} activities, total weight: {member_total_weight}"):
            pcol1, pcol2, pcol3 = st.columns(3)
            pcol1.metric("Visible Tasks", member_visible)
            pcol2.metric("Invisible Tasks", member_invisible)
            pcol3.metric(
                "Invisible %",
                f"{round(member_invisible / max(len(member_df), 1) * 100)}%"
            )
            st.dataframe(
                member_df[["date", "activity", "category", "visibility", "mental_weight"]]
                .sort_values(["date", "mental_weight"], ascending=[True, False])
                .reset_index(drop=True),
                use_container_width=True,
            )

    # ---- TOP ACTIVITIES ----
    st.subheader("🏋️ Heaviest Mental Load Activities")

    top_df = df.sort_values(by="mental_weight", ascending=False).head(10)

    top_bar = (
        alt.Chart(top_df)
        .mark_bar(cornerRadiusEnd=6)
        .encode(
            x=alt.X("mental_weight:Q", title="Mental Weight"),
            y=alt.Y("activity:N", title="", sort="-x"),
            color=alt.Color("user:N", legend=alt.Legend(title="Person")),
            tooltip=["date", "user", "activity", "category", "mental_weight", "visibility"],
        )
        .properties(title="Top 10 Heaviest Activities", height=400)
    )
    st.altair_chart(top_bar, use_container_width=True)

    # ---- WHAT-IF REBALANCER ----
    st.subheader("🔄 What-If Rebalancer")
    st.markdown("Reassign activities and see how the balance shifts.")

    rebalance_df = df.copy().reset_index(drop=True)
    users = sorted(df["user"].unique())

    reassigned = []
    with st.expander("Reassign Activities", expanded=False):
        for i, row in rebalance_df.iterrows():
            col1, col2 = st.columns([3, 1])
            col1.markdown(
                f"**{row['activity']}** ({row['date']}, weight: {row['mental_weight']}, now: {row['user']})"
            )
            new_user = col2.selectbox(
                "→", users,
                index=users.index(row["user"]),
                key=f"rebalance_{i}",
                label_visibility="collapsed",
            )
            reassigned.append(new_user)

    rebalance_df["user"] = reassigned
    new_iri = rebalance_df.groupby("user")["mental_weight"].sum().reset_index()
    new_total = new_iri["mental_weight"].sum()
    new_iri["New IRI (%)"] = (new_iri["mental_weight"] / new_total * 100).round(1)

    comparison = (
        iri_df[["user", "IRI (%)"]]
        .merge(new_iri[["user", "New IRI (%)"]], on="user", how="outer")
        .fillna(0)
    )
    comparison["Change"] = (comparison["New IRI (%)"] - comparison["IRI (%)"]).round(1)
    st.dataframe(comparison, use_container_width=True)

    if comparison["Change"].abs().sum() > 0:
        new_disparity = new_iri["New IRI (%)"].std().round(1)
        delta = round(new_disparity - disparity, 1)
        dcol1, dcol2 = st.columns(2)
        dcol1.metric("Current Disparity", disparity)
        dcol2.metric("New Disparity", new_disparity, delta=f"{delta:+.1f}", delta_color="inverse")

    # ---- INSIGHT REPORT ----
    st.subheader("💡 Insight Report")

    highest = iri_df.sort_values("IRI (%)", ascending=False).iloc[0]
    lowest = iri_df.sort_values("IRI (%)", ascending=True).iloc[0]
    inv_pct = round(invisible_count / max(total_tasks, 1) * 100, 1)
    heaviest_category = (
        df.groupby("category")["mental_weight"]
        .sum()
        .sort_values(ascending=False)
        .index[0]
    )

    insights = [
        f"Across **{num_days} day(s)**, **{total_tasks} activities** were recorded.",

        f"**{highest['user']}** carries {highest['IRI (%)']}% of total mental load — "
        f"{highest['IRI (%)'] - fair_share:+.1f}pp from fair share. {highest['Status']}",

        f"**{lowest['user']}** carries the least at {lowest['IRI (%)']}%.",

        f"**{inv_pct}%** of all activities are invisible work — "
        f"{'⚠️ the majority of effort is unseen.' if inv_pct > 50 else 'a moderate split.'}",

        f"**{hidden_found} hidden tasks** were uncovered through follow-up analysis."
        if hidden_found > 0
        else "No hidden tasks were surfaced — try again and answer the follow-up prompts.",

        f"The heaviest category is **{heaviest_category}**.",

        f"Disparity score: **{disparity}** — "
        f"{'🔴 Highly unequal distribution' if disparity > 20 else '🟡 Moderate imbalance' if disparity > 10 else '🟢 Reasonably balanced'}.",
    ]

    for insight in insights:
        st.markdown(f"- {insight}")

    # ---- DOWNLOAD ----
    st.divider()

    with st.expander("📋 View Complete Dataset"):
        st.dataframe(df, use_container_width=True)

    col_dl1, col_dl2 = st.columns(2)

    col_dl1.download_button(
        "📥 Download Full Data",
        df.to_csv(index=False),
        "mindshare_data.csv",
        "text/csv",
        use_container_width=True,
    )

    col_dl2.download_button(
        "📥 Download IRI Report",
        iri_df.to_csv(index=False),
        "mindshare_iri_report.csv",
        "text/csv",
        use_container_width=True,
    )