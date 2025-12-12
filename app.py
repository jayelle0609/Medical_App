import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image

# ---------------------------
# CSV file storage
# ---------------------------

CSV_FILE = "default.csv"

# Load doctors CSV
def load_doctors() -> pd.DataFrame:
    try:
        df = pd.read_csv(CSV_FILE)
        return df
    except FileNotFoundError:
        cols = ["full_name","age","gender","nationality","medical_school","registration_id",
                "email","phone","year","rotations","teaching_hours","created_at","sponsoring_institution",
                "EPA1_Completed","EPA1_Level","EPA1_ExitMet",
                "EPA2_Completed","EPA2_Level","EPA2_ExitMet",
                "EPA3_Completed","EPA3_Level","EPA3_ExitMet",
                "EPA4_Completed","EPA4_Level","EPA4_ExitMet",
                "EPA5_Completed","EPA5_Level","EPA5_ExitMet",
                "EPA6_Completed","EPA6_Level","EPA6_ExitMet",
                "EPA7_Completed","EPA7_Level","EPA7_ExitMet",
                "EPA8_Completed","EPA8_Level","EPA8_ExitMet",
                "EPA1","EPA2","EPA3","EPA4","EPA5","EPA6","EPA7","EPA8"]
        return pd.DataFrame(columns=cols)

# Save doctors CSV
def save_doctors(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)

# ---------------------------
# Streamlit App UI
# ---------------------------
med_img = Image.open("med.jpg")
st.image(med_img, caption="**Making sense of hospital administration data.**")
st.set_page_config(page_title="Medical Education App", layout="wide")
st.title("Medical Education — Residency Training Management App")

menu = st.sidebar.radio("Sections", [
    "1. Add Doctor",
    "2. Rotations, EPA Tracking Dashboard",
    "3. Automated Email Reminders",
    "3. Update EPA",
    "4. Resident Portfolio"
])

df = load_doctors()

# ---------------------------
# Section 1: Add Doctor
# ---------------------------
if menu == "1. Add Doctor":
    st.header("Add Doctor — Full Information")

    with st.form(key='add_doctor_form'):
        st.subheader("Basic Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            full_name = st.text_input("Full name")
            age = st.number_input("Age", min_value=18, max_value=80, value=28)
            gender = st.selectbox("Gender", ["Female","Male","Other","Prefer not to say"]) 
            nationality = st.text_input("Nationality")
        with col2:
            medical_school = st.text_input("Medical school graduated")
            registration_id = st.text_input("Medical registration ID")
            email = st.text_input("Email")
            phone = st.text_input("Phone (optional)")
        with col3:
            year = st.selectbox("Resident year (1-5)", [1,2,3,4,5])
            st.caption("Add rotations for the year below")
            rotations_raw = st.text_area("Rotations (semicolon separated)", value="")
            teaching_hours = st.number_input("Teaching hours (initial)", min_value=0.0, value=0.0)
            sponsoring_institution = st.selectbox("Sponsoring Institution", ["SingHealth","NHG","NUHS"])

        st.subheader("Ultrasound / Clinical / Teaching / Exam Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            ultrasound_trauma_done = st.number_input("Sonography in Trauma Ultrasound Done", min_value=0, value=0)
            ultrasound_trauma_total = st.number_input("Sonography in Trauma Ultrasound Total Requirement", min_value=0, value=25)
            ultrasound_cardiac_done = st.number_input("Ultrasound Cardiac Done", min_value=0, value=0)
            ultrasound_cardiac_total = st.number_input("Ultrasound Cardiac Total Requirement", min_value=0, value=25)
            ultrasound_lung_done = st.number_input("Ultrasound Lung Done", min_value=0, value=0)
            ultrasound_lung_total = st.number_input("Ultrasound Lung Total Requirement", min_value=0, value=25)
        with col2:
            adult_med_done = st.number_input("Adult Medical Resuscitation Done", min_value=0, value=0)
            adult_med_total = st.number_input("Adult Medical Resuscitation Total Requirement", min_value=0, value=45)
            adult_trauma_done = st.number_input("Adult Trauma Resuscitation Done", min_value=0, value=0)
            adult_trauma_total = st.number_input("Adult Trauma Resuscitation Total Requirement", min_value=0, value=35)
            ed_ultrasound_done = st.number_input("ED Bedside Ultrasound Done", min_value=0, value=0)
            ed_ultrasound_total = st.number_input("ED Bedside Ultrasound Total Requirement", min_value=0, value=165)
        with col3:
            MMed_A_Status = st.selectbox("MMed A Status", ["Pass", "Fail", "Pending"])
            MMed_B_Status = st.selectbox("MMed B Status", ["Pass", "Fail", "Pending"])
            MMed_C_Status = st.selectbox("MMed C Status", ["Pass", "Fail", "Pending"])
            Teaching_Admin_Status = st.selectbox("Teaching Admin Status", ["Pass", "Fail", "Pending"])
            Clinical_Viva_Status = st.selectbox("Clinical Viva Status", ["Pass", "Fail", "Pending"])
            CAT_Status = st.selectbox("CAT Status", ["Pass", "Fail", "Pending"])
            ABMS_MCQs_Status = st.selectbox("ABMS MCQs Status", ["Pass", "Fail", "Pending"])


        st.subheader("Tracking EPA Grades and Completion Status")
        st.success(
    "Necessary EPA Entrustment Level to be attained for exit: "
    "[EPA Passing Level Requirements](https://isomer-user-content.by.gov.sg/91/c65aeb46-a34c-4c92-8d36-12070f9690d8/emergency-medicine-epasd8f2c4aebc15419b8729ec17766476f7.pdf)"
)

        col1, col2 = st.columns(2)
        with col1:
            EPA1 = st.selectbox("EPA1", [1,2,3,4,5])
            EPA2 = st.selectbox("EPA2", [1,2,3,4,5])
            EPA3 = st.selectbox("EPA3", [1,2,3,4,5])
            EPA4 = st.selectbox("EPA4", [1,2,3,4,5])
            EPA5 = st.selectbox("EPA5", [1,2,3,4,5])
            EPA6 = st.selectbox("EPA6", [1,2,3,4,5])
            EPA7 = st.selectbox("EPA7", [1,2,3,4,5])
            EPA8 = st.selectbox("EPA8", [1,2,3,4,5])
        with col2:
            EPA1_Completed = st.selectbox("EPA1 Completed", ["No", "Yes"])
            EPA2_Completed = st.selectbox("EPA2 Completed", ["No", "Yes"])
            EPA3_Completed = st.selectbox("EPA3 Completed", ["No", "Yes"])
            EPA4_Completed = st.selectbox("EPA4 Completed", ["No", "Yes"])
            EPA5_Completed = st.selectbox("EPA5 Completed", ["No", "Yes"])
            EPA6_Completed = st.selectbox("EPA6 Completed", ["No", "Yes"])
            EPA7_Completed = st.selectbox("EPA7 Completed", ["No", "Yes"])
            EPA8_Completed = st.selectbox("EPA8 Completed", ["No", "Yes"])

        submit = st.form_submit_button("Save Doctor Information")

    if submit:
        rotations = [r.strip() for r in rotations_raw.split(";") if r.strip()]
        new_row = {
            "full_name": full_name,
            "age": int(age),
            "gender": gender,
            "nationality": nationality,
            "medical_school": medical_school,
            "registration_id": registration_id,
            "email": email,
            "phone": str(phone).replace(',', ''),
            "year": int(year),
            "rotations": ";".join(rotations),
            "teaching_hours": float(teaching_hours),
            "created_at": datetime.utcnow().isoformat(),
            "sponsoring_institution": sponsoring_institution,
            "ultrasound_trauma_done": ultrasound_trauma_done,
            "ultrasound_trauma_total": ultrasound_trauma_total,
            "ultrasound_cardiac_done": ultrasound_cardiac_done,
            "ultrasound_cardiac_total": ultrasound_cardiac_total,
            "ultrasound_lung_done": ultrasound_lung_done,
            "ultrasound_lung_total": ultrasound_lung_total,
            "adult_med_done": adult_med_done,
            "adult_med_total": adult_med_total,
            "adult_trauma_done": adult_trauma_done,
            "adult_trauma_total": adult_trauma_total,
            "ed_ultrasound_done": ed_ultrasound_done,
            "ed_ultrasound_total": ed_ultrasound_total,
            "MMed_A_Status": MMed_A_Status,
            "MMed_B_Status": MMed_B_Status,
            "MMed_C_Status": MMed_C_Status,
            "Teaching_Admin_Status": Teaching_Admin_Status,
            "Clinical_Viva_Status": Clinical_Viva_Status,
            "CAT_Status": CAT_Status,
            "ABMS_MCQs_Status": ABMS_MCQs_Status,
            "EPA1": EPA1, "EPA2": EPA2, "EPA3": EPA3, "EPA4": EPA4, 
            "EPA5": EPA5, "EPA6": EPA6, "EPA7": EPA7, "EPA8": EPA8,
            "EPA1_Completed": EPA1_Completed, "EPA2_Completed": EPA2_Completed,
            "EPA3_Completed": EPA3_Completed, "EPA4_Completed": EPA4_Completed,
            "EPA5_Completed": EPA5_Completed, "EPA6_Completed": EPA6_Completed,
            "EPA7_Completed": EPA7_Completed, "EPA8_Completed": EPA8_Completed
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_doctors(df)
        st.success(f"Saved doctor: {full_name}")

    st.markdown("---")
    st.subheader("All doctors in system")
    pd.set_option('display.max_colwidth', None)
    df['phone'] = df['phone'].astype(str).str.replace(',', '')
    st.dataframe(df, width=2500, height=500)



# ---------------------------
# Section 2: Rotations, EPA Tracking Dashboard
# ---------------------------
elif menu == "2. Rotations, EPA Tracking Dashboard":
    st.header("Rotations, EPA Completion & Teaching Hours")
    if df.empty:
        st.info("No doctors yet — add doctors in Section 1.")
    else:
        # Resident counts by year
        st.subheader("Resident counts by year")
        counts = df['year'].value_counts().sort_index()
        st.bar_chart(counts)

        # Top rotations by department (Top 8)
        st.subheader("Top rotations by department (Top 8)")
        all_rots = df['rotations'].dropna().apply(lambda x: str(x).split(';'))
        exploded = pd.Series([item for sub in all_rots for item in sub if item!=''])
        if not exploded.empty:
            top_rot = exploded.value_counts().head(8).reset_index()
            top_rot.columns = ['Rotation','Count']
            fig_rot = px.bar(top_rot, x='Rotation', y='Count', color='Rotation', 
                             title="Top 8 Rotations by Department", color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig_rot, use_container_width=True)

        # Rotations by Sponsoring Institution
        st.subheader("Rotations by Sponsoring Institution")
        inst_counts = df['sponsoring_institution'].value_counts().reset_index()
        inst_counts.columns = ['Institution','Count']
        fig_inst = px.bar(inst_counts, x='Institution', y='Count', color='Institution', 
                          title="Doctor Rotations at Sponsoring Institution", color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_inst, use_container_width=True)

        # ---------------------------
        # EPA completion chart (no hover)
        # ---------------------------
        st.subheader("EPA Completion Status")
        epa_cols = [f"EPA{i}_Completed" for i in range(1,9)]
        epa_completed = df[epa_cols].apply(lambda x: x=="Yes").sum()
        epa_total = len(df)

        epa_df = pd.DataFrame({
            "EPA": [f"EPA{i}" for i in range(1,9)]*2,
            "Status": ["Completed / Pass"]*8 + ["Not Completed / Fail"]*8,
            "Count": list(epa_completed) + list(epa_total - epa_completed)
        })

        fig_epa = px.bar(
            epa_df,
            x="EPA",
            y="Count",
            color="Status",
            barmode="group",
            color_discrete_map={"Completed / Pass":"green","Not Completed / Fail":"red"},
            title="EPA Completion by Residents"
        )

        st.plotly_chart(fig_epa, use_container_width=True)


# ---------------------------
# Section 3: Automated Email Reminders
# ---------------------------
elif menu == "3. Automated Email Reminders":
    st.success("This section highlights doctors whose teaching hours are below average (across all residents).")
    st.header("Doctors with Insufficient Teaching Hours")
    st.info(f"Average teaching hours: {df['teaching_hours'].mean():.1f}")
    if df.empty:

        st.info("No doctors yet.")
    else:
        avg_hours = df['teaching_hours'].mean()
        below = df[df['teaching_hours'] < avg_hours]
        st.dataframe(below[['full_name','email','teaching_hours','sponsoring_institution']])
        st.header("Automated reminder emails to clock in additional tutoring hours")
        st.markdown("⚠️ **Note:** Configure a real email and password to send emails via SMTP.")
        sender_email = st.text_input("Sender email", value="jayelleteo@gmail.com")
        sender_password = st.text_input("Email password", type="password")
        st.warning("Full Name, Teaching Hours, and Average Hours are automatically filled in based on each respective doctor from the data table above.")
        custom_msg = st.text_area(
            "Custom email message",
            value="""Dear {full_name},

We hope this message finds you well. 
We noticed that your current teaching hours ({teaching_hours}) are below the average ({avg_hours:.1f}). 

We would like to encourage you to schedule additional teaching hours to meet your portfolio requirements.
Please feel free to contact our administration if you encounter any difficulties scheduling your teaching hours.
Thank you for your dedication and contribution to resident education. 

Yours Sincerely,
Group Education Administration
""", height = 280
        )

        if st.button("Send Emails") and sender_email and sender_password:
            for _, row in below.iterrows():
                try:
                    receiver_email = row['email']
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = receiver_email
                    message["Subject"] = "Teaching Hours Reminder"
                    body = custom_msg.format(full_name=row['full_name'], teaching_hours=row['teaching_hours'], avg_hours=avg_hours)
                    message.attach(MIMEText(body, "plain"))

                    # SMTP setup
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                    server.quit()
                    st.success(f"Email sent to {row['full_name']}")
                except Exception as e:
                    st.error(f"Failed to send email to {row['full_name']}: {e}")

# ---------------------------
# Section 3 (Duplicate number): Update EPA
# ---------------------------
elif menu == "3. Update EPA":
    st.header("Update EPA Levels")
    if df.empty:
        st.info("No doctors yet — add doctors in Section 1.")
    else:
        resident = st.selectbox("Select resident", df['full_name'].tolist())
        res_row = df[df['full_name']==resident].iloc[0]

        entrustment_levels = ["1","2","2a","2b","3","3a","3b","3c","4","4a","4b","5"]
        epas = {
            "EPA 1: Resuscitating and Care of Critically Ill Adult Medical/Surgical Patients":"EPA1",
            "EPA 2: Resuscitating and Care of Critically Ill Adult Trauma Patients":"EPA2",
            "EPA 3: Resuscitating and Care of Critically Ill or Injured Paediatric Patients":"EPA3",
            "EPA 4: Managing Adult Ambulatory Patients":"EPA4",
            "EPA 5: Managing Paediatric Ambulatory Patients":"EPA5",
            "EPA 6: Managing Adult Patients with Emergent or Urgent Conditions":"EPA6",
            "EPA 7: Managing Patients Who Need End-Of-Life Care":"EPA7",
            "EPA 8: Managing Patients in Extended Observation Facility (Optional)":"EPA8"
        }

        updated_epas = {}
        for title, col in epas.items():
            current_val = res_row[col] if col in res_row else ""
            updated_epas[col] = st.selectbox(title, options=entrustment_levels,
                                             index=entrustment_levels.index(current_val) if current_val in entrustment_levels else 0)

        if st.button("Save EPA Levels"):
            for col, val in updated_epas.items():
                df.loc[df['full_name']==resident, col] = val
            save_doctors(df)
            st.success(f"EPA levels for {resident} updated successfully!")

# ---------------------------
# Section 4: Resident Portfolio
# ---------------------------
elif menu == "4. Resident Portfolio":
    st.header("Resident Portfolio — Progress & Milestones")
    if df.empty:
        st.info("No doctors yet — add doctors in Section 1.")
    else:
        resident = st.selectbox("Select resident", df['full_name'].tolist())
        res_row = df[df['full_name']==resident].iloc[0]
        st.success(f"{resident} Portfolio Overview")

        # Teaching Progress
        st.markdown("### Teaching Progress")
        teaching_hours = res_row['teaching_hours']
        target_hours = 50
        st.progress(min(teaching_hours/target_hours,1.0))
        st.write(f"{teaching_hours} Hours / Target: {target_hours} hours/year")

        # ------------------- Ultrasound Scans -------------------
        st.markdown("### Ultrasound Scans")
        st.write("**Sonography in Trauma**")
        st.progress(res_row['ultrasound_trauma_done'] / res_row['ultrasound_trauma_total'])
        st.write(f"{res_row['ultrasound_trauma_done']}/{res_row['ultrasound_trauma_total']}")

        st.write("**Cardiac Ultrasound**")
        st.progress(res_row['ultrasound_cardiac_done'] / res_row['ultrasound_cardiac_total'])
        st.write(f"{res_row['ultrasound_cardiac_done']}/{res_row['ultrasound_cardiac_total']}")

        st.write("**Lung Ultrasound**")
        st.progress(res_row['ultrasound_lung_done'] / res_row['ultrasound_lung_total'])
        st.write(f"{res_row['ultrasound_lung_done']}/{res_row['ultrasound_lung_total']}")

        # ------------------- Resuscitations & Procedures -------------------
        st.markdown("### Compulsory Procedures")
        st.write("**Adult Medical Resuscitation**")
        st.progress(res_row['adult_med_done'] / res_row['adult_med_total'])
        st.write(f"{res_row['adult_med_done']}/{res_row['adult_med_total']}")

        st.write("**Adult Trauma Resuscitation**")
        st.progress(res_row['adult_trauma_done'] / res_row['adult_trauma_total'])
        st.write(f"{res_row['adult_trauma_done']}/{res_row['adult_trauma_total']}")

        st.write("**ED Bedside Ultrasound**")
        st.progress(res_row['ed_ultrasound_done'] / res_row['ed_ultrasound_total'])
        st.write(f"{res_row['ed_ultrasound_done']}/{res_row['ed_ultrasound_total']}")

        # ------------------- Summative Assessments -------------------
        st.markdown("### Summative Assessments (Pass M.Med or Equivalent)")
        assessments = pd.DataFrame([
            ["MMed (EM) Part A", res_row['MMed_A_Status']],
            ["MMed (EM) Part B", res_row['MMed_B_Status']],
            ["MMed (EM) Part C", res_row['MMed_C_Status']],
            ["Teaching and Administration Portfolio", res_row['Teaching_Admin_Status']],
            ["Clinical Viva (9 stations)", res_row['Clinical_Viva_Status']],
            ["CAT (2 hr written paper)", res_row['CAT_Status']],
            ["ABMS MCQ Exam (200 MCQ, 6h 10min)", res_row['ABMS_MCQs_Status']]
        ], columns=["Assessment", "Status"])

        # Highlight Fail and Pending with nude colors
        def highlight_status(val):
            if val == 'Fail':
                return 'background-color: #F5B7B1'  # soft nude red
            elif val == 'Pending':
                return 'background-color: #FFF3C4'  # soft nude yellow
            else:
                return ''

        st.dataframe(assessments.style.applymap(highlight_status, subset=['Status']))


        # ------------------- EPA Milestones -------------------
        st.markdown("### EPA Milestone Tracking")
        epa_cols = ['EPA1','EPA2','EPA3','EPA4','EPA5','EPA6','EPA7','EPA8']
        epa_completed_cols = ['EPA1_Completed','EPA2_Completed','EPA3_Completed','EPA4_Completed',
                            'EPA5_Completed','EPA6_Completed','EPA7_Completed','EPA8_Completed']
        epa_targets = {"EPA1": "4b", "EPA2": "4b", "EPA3": "3a", "EPA4": "4b",
                    "EPA5": "3b", "EPA6": "4b", "EPA7": "4b", "EPA8": "4b"}

        epa_df = pd.DataFrame({
            "EPA ID": [f"EPA{i}" for i in range(1,9)],
            "Current Level": [res_row[col] for col in epa_cols],
            "Target Level": [epa_targets[col] for col in epa_cols],
            "Completed": [res_row[col] for col in epa_completed_cols]
        })

        # Highlight not completed in light orange
        def highlight_not_completed(val):
            if val != "Yes":
                return 'background-color: #FFF3C4'  # light orange
            else:
                return ''

        st.dataframe(epa_df.style.applymap(highlight_not_completed, subset=['Completed']))

