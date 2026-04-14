import streamlit as st
import pandas as pd
import joblib
import re
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Health Assistant", page_icon="🏥", layout="wide")

# --- CSS (DARK THEME + WHITE TEXT + HIDE METRICS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

/* DARK THEME */
.stApp {
    background-color: #0f0f23 !important;
    color: white !important;
}

/* ALL TEXT WHITE */
label, p, span, div, h1, h2, h3, h4, h5, h6,
.stMarkdown, .stText, .stSelectbox label, 
[data-testid="stMultiselect"] label,
[data-testid="stMultiselect"] span,
.stMultiSelect label,
.element-container label {
    color: white !important;
}

/* HERO */
.hero-container {
    background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white !important;
    margin-bottom: 20px;
}

/* INPUT BOX - DARK */
.input-box {
    background: #1e1e3f !important;
    color: white !important;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #333366;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(135deg, #8B5CF6, #3B82F6) !important;
    color: white !important;
    border-radius: 10px;
    font-weight: 700;
    border: none;
    padding: 0.8rem 1.5rem;
}

/* Result cards - DARK + HIDE METRICS */
.result-card {
    background: #1e1e3f !important;
    color: white !important;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #333366;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    margin-bottom: 16px;
}

.result-card p {
    display: none !important;
}

/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #8B5CF6, #3B82F6) !important;
}

/* Rank badge */
.rank-badge {
    background: rgba(139, 92, 246, 0.2);
    color: #c9b6ff !important;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
}

/* Disease type */
.disease-type {
    color: #8B5CF6 !important;
    font-weight: 600;
    font-size: 14px;
}

/* Hide info messages */
.stInfo {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOAD FILES (CLEAN - NO DEBUG INFO) ---
@st.cache_resource
def load_resources():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # ✅ CORRECT PATHS (NO DEBUG PRINTS)
    model_path = os.path.join(BASE_DIR, '..', 'train_model', 'models', 'best_model.joblib')
    encoder_path = os.path.join(BASE_DIR, '..', 'train_model', 'models', 'label_encoder.joblib')
    data_path = os.path.join(BASE_DIR, '..', 'data', 'diseases_dataset.csv')
    
    model = joblib.load(model_path)
    le = joblib.load(encoder_path)
    df = pd.read_csv(data_path)
    
    return model, le, df

try:
    model, le, disease_info = load_resources()
except Exception as e:
    st.error(f"⚠️ Model or data not found: {str(e)}")
    st.stop()

# --- DOCTOR DB ---
doctor_db = {
    "General Physician": {"name": "Dr. Sameer Mehta", "phone": "+91 98765-43210", "icon": "🩺"},
    "Cardiologist": {"name": "Dr. Anjali Sharma", "phone": "+91 91234-56789", "icon": "🫀"},
    "Neurologist": {"name": "Dr. Vikram Seth", "phone": "+91 99887-76655", "icon": "🧠"},
    "Dermatologist": {"name": "Dr. Priya Rai", "phone": "+91 94433-22110", "icon": "🧴"},
    "Gastroenterologist": {"name": "Dr. Kunal Verma", "phone": "+91 90011-22334", "icon": "🫃"},
    "Pulmonologist": {"name": "Dr. Riya Thomas", "phone": "+91 95544-22331", "icon": "🫁"}
}

def get_specialist(disease_name):
    disease_name = disease_name.lower()

    if any(word in disease_name for word in ["skin", "eczema", "acne", "psoriasis", "dermatitis", "fungal", "ringworm"]):
        return "Dermatologist"

    elif any(word in disease_name for word in ["heart", "cardio", "angina", "attack", "arrhythmia"]):
        return "Cardiologist"

    elif any(word in disease_name for word in ["brain", "neuro", "stroke", "migraine", "epilepsy", "dementia"]):
        return "Neurologist"

    elif any(word in disease_name for word in ["asthma", "copd", "lung", "pneumonia", "breathing"]):
        return "Pulmonologist"

    elif any(word in disease_name for word in ["stomach", "liver", "ulcer", "gastritis", "crohn", "ibs", "hepatitis"]):
        return "Gastroenterologist"

    else:
        return "General Physician"

def get_disease_type(disease_name):
    disease_row = disease_info[disease_info['Disease'].str.contains(disease_name, case=False, na=False)]
    if not disease_row.empty:
        return disease_row['Type'].iloc[0] if 'Type' in disease_row.columns else "Normal"
    return "Normal"

# --- PREPARE ALL SYMPTOMS ---
all_syms = set()
for s in disease_info['Symptoms']:
    all_syms.update([i.strip().lower() for i in str(s).split(',') if i.strip()])

# --- HERO ---
st.markdown("""
<div class="hero-container">
    <h2>🏥 AI Health Suggestion</h2>
    <p>Smart symptom analysis with doctor recommendation</p>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
left, right = st.columns([1, 1.2])

# --- LEFT SIDE ---
with left:
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    st.subheader("🧾 Select Symptoms")
    user_symptoms = st.multiselect("Choose symptoms:", sorted(list(all_syms)))
    btn = st.button("Run Diagnosis", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RIGHT SIDE ---
with right:
    if btn:
        if not user_symptoms:
            st.warning("⚠️ Please select symptoms first.")
        else:
            user_set = set(user_symptoms)
            disease_scores = []

            # Rank diseases by symptom overlap
            for disease, group in disease_info.groupby('Disease'):
                disease_syms = set()
                for s in group['Symptoms']:
                    disease_syms.update([i.strip().lower() for i in str(s).split(',') if i.strip()])

                matches = len(user_set & disease_syms)
                total_disease_syms = len(disease_syms)
                match_percent = (matches / total_disease_syms * 100) if total_disease_syms > 0 else 0
                user_match_percent = (matches / len(user_set) * 100) if len(user_set) > 0 else 0

                disease_scores.append({
                    "disease": disease,
                    "matches": matches,
                    "total_symptoms": total_disease_syms,
                    "match_percent": match_percent,
                    "user_match_percent": user_match_percent
                })

            # Sort top diseases
            disease_scores = sorted(
                disease_scores,
                key=lambda x: (x["matches"], x["user_match_percent"], x["match_percent"]),
                reverse=True
            )

            top_3 = disease_scores[:3]
            best_match = top_3[0]["disease"] if top_3 else "General Condition"

            # Get disease types for top 3
            disease_types = [get_disease_type(item["disease"]) for item in top_3]

            # Doctor Recommendation
            spec = get_specialist(best_match)
            doc = doctor_db.get(spec, doctor_db["General Physician"])

            # --- RESULT UI ---
            st.markdown("## 🧾 Diagnosis Result")
            st.subheader("🏆 Top 3 Predicted Diseases")

            # TOP 3 CARDS
            for idx, item in enumerate(top_3, start=1):
                disease_name = item["disease"]
                percent = item["user_match_percent"]
                disease_type = disease_types[idx-1]
                
                st.markdown(f"""
                <div class="result-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span class="rank-badge">#{idx}</span>
                    <h4 style="margin: 0; flex: 1;">{disease_name}</h4>
                    <span style="font-size: 22px; font-weight: 800; color: #8B5CF6;">{percent:.0f}%</span>
                    </div>
                    <div class="disease-type">Disease Type: {disease_type}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("🩺 Most Likely Disease")
            st.write(f"**{best_match}**")
            
            best_percent = top_3[0]["user_match_percent"] if top_3 else 0
            st.progress(min(best_percent/100, 1.0))
            
            best_disease_type = disease_types[0]
            if best_disease_type == "Normal":
                st.success(f"Disease Type: {best_disease_type}")
            elif best_disease_type == "Serious":
                st.warning(f"Disease Type: {best_disease_type}")
            else:
                st.error(f"Disease Type: {best_disease_type}")

            st.markdown("---")
            st.subheader("👨‍⚕️ Recommended Specialist")
            colA, colB = st.columns([1, 4])
            with colA:
                st.write(doc["icon"])
            with colB:
                st.write(f"**Doctor:** {doc['name']}")
                st.write(f"**Specialist:** {spec}")
                st.write(f"📞 {doc['phone']}")

            st.markdown("---")
            st.warning("⚠️ This is AI-based suggestion. Please consult a real doctor.")
    else:
        st.markdown('<div style="opacity: 0.7; padding: 20px; border-radius: 10px; background: rgba(139,92,246,0.1);">👈 Select symptoms and click "Run Diagnosis"</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #8B5CF6; font-weight: 600;'>Built with ❤️ for healthcare awareness</p>", unsafe_allow_html=True)