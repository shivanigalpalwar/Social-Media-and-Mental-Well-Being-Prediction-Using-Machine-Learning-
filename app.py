import pickle
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Social Media & Mental Well-Being Prediction", page_icon="🌿", layout="wide")

with open("regression.pkl", "rb") as file:
    regression_model = pickle.load(file)
with open("classification.pkl", "rb") as file:
    classification_model = pickle.load(file)
with open("clustering.pkl", "rb") as file:
    clustering_model = pickle.load(file)

# --- Visual design and project header ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #FBF9FF 0%, #F8F6FC 100%);
    color: #292442;
}
.block-container {
    max-width: 1600px;
    width: 100%;
    padding: 3.5rem clamp(1rem, 3vw, 3rem) 2.5rem;
}
.hero {
    background: linear-gradient(125deg, #EEE6FF 0%, #FFF4EF 100%);
    border: 1px solid #DED1F7;
    border-radius: 22px;
    padding: clamp(24px, 3vw, 48px);
    min-height: 320px;
    height: 320px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
div[data-testid="stImage"] img {
    height: 320px;
    width: 100%;
    object-fit: cover;
    border-radius: 22px;
    border: 1px solid #DED1F7;
}
.hero h1 {
    color: #503783;
    font-size: clamp(1.8rem, 3vw, 2.55rem);
    line-height: 1.15;
    margin: 0 0 13px 0;
}
.hero p {
    color: #5E5570;
    font-size: 1rem;
    line-height: 1.6;
    margin: 0 0 8px 0;
}
.section-note {
    color: #766C87;
    font-size: 0.9rem;
    margin: 0.15rem 0 1rem 0;
}
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid #E5DDF0;
    border-radius: 18px;
    padding: 22px 22px 16px 22px;
}
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5DDF0;
    border-radius: 16px;
    padding: 18px 18px 14px 18px;
    box-shadow: 0 4px 16px rgba(83, 57, 130, 0.05);
}
div[data-testid="stMetricLabel"] p {
    color: #6B5C86;
    font-weight: 600;
}
div[data-testid="stMetricValue"] {
    color: #503783;
    font-weight: 650;
}
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stWidgetLabel"] label {
    color: #403456 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Improve visibility of slider and input labels */
.stApp [data-testid="stSlider"] label,
.stApp [data-testid="stNumberInput"] label,
.stApp [data-testid="stSelectbox"] label {
    color: #403456 !important;
    opacity: 1 !important;
}

/* Keep section headings readable */
.stApp h1,
.stApp h2,
.stApp h3 {
    color: #352653 !important;
}
.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(90deg, #7654BC, #A184DC);
    color: white;
    border: 0;
    border-radius: 11px;
    min-height: 44px;
    font-weight: 600;
}
.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(90deg, #6846AE, #9273D0);
    color: white;
    border: 0;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background-color: #8D6BD0;
}
@media (max-width: 700px) {
    .hero { padding: 20px; min-height: auto; height: auto; }
    div[data-testid="stImage"] img { height: auto; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)

hero_left, hero_right = st.columns([1, 1], gap="medium", vertical_alignment="top")

with hero_left:
    st.markdown("""
    <div class="hero">
        <h1>Social Media &amp; Mental Well-Being Prediction</h1>
        <p>Discover how your digital habits, daily routines, and social connections relate to wellbeing.</p>
        <p>✨ Every habit tells a story. Explore yours through data.</p>
    </div>
    """, unsafe_allow_html=True)
with hero_right:
    image_path = Path(__file__).resolve().parent / "mindscope_hero.png"
    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    else:
        st.info("Add mindscope_hero.png beside app.py to display the project illustration.")

st.markdown("<div class='section-note'>Your daily habits, your digital world, your personal insights.</div>", unsafe_allow_html=True)

with st.form("mindscope_form"):
    st.subheader("Step 1 — About you")
    c1, c2, c3 = st.columns(3)
    with c1:
        Age = st.number_input("Age", min_value=18, max_value=30, value=22)
        Gender = st.selectbox("Gender", ["Female", "Male", "Non-binary"])
        Country = st.selectbox("Country", ["India", "United States", "United Kingdom", "Canada", "Australia", "Other"])
    with c2:
        Academic_Level = st.selectbox("Academic level", ["Undergraduate", "Postgraduate", "Doctoral", "Other"])
        Most_Used_Platform = st.selectbox("Most used platform", ["Instagram", "TikTok", "YouTube", "Facebook", "WhatsApp", "Snapchat", "X", "Other"])
        Purpose_Of_Use = st.selectbox("Main purpose", ["Entertainment", "Communication", "Networking", "Mixed", "Learning", "News"])
    with c3:
        Cyberbullying_Exposure = st.selectbox("Cyberbullying exposure", ["No", "Yes"])
        Avg_Daily_Usage_Hours = st.slider("Daily social-media usage (hours)", 0.0, 12.0, 3.0, 0.1)
        Daily_Unlocks = st.number_input("Daily phone unlocks", 0, 300, 60)
    st.subheader("Step 2 — Daily habits and support")
    c1, c2, c3 = st.columns(3)
    with c1:
        Study_Hours = st.slider("Study hours per day", 0.0, 16.0, 3.0, 0.1)
        Physical_Activity_Hours = st.slider("Physical activity hours per day", 0.0, 8.0, 1.0, 0.1)
        Sleep_Hours_Per_Night = st.slider("Sleep hours per night", 0.0, 14.0, 7.0, 0.1)
    with c2:
        Social_Support_Score = st.slider("Social support score (0–10)", 0.0, 10.0, 5.0, 0.1)
        Social_Comparison_Level = st.slider("Social comparison level (1–5)", 1, 5, 3)
        Exercise_Days_Per_Week = st.slider("Exercise days per week", 0, 7, 3)
    with c3:
        st.info("Complete both steps, then select **Analyze my profile** to see the model outputs.")
    submitted = st.form_submit_button("Analyze my profile", use_container_width=True)
if submitted:
    user_data = pd.DataFrame([{
        "Age": Age, "Gender": Gender, "Country": Country, "Academic_Level": Academic_Level,
        "Most_Used_Platform": Most_Used_Platform, "Purpose_Of_Use": Purpose_Of_Use,
        "Avg_Daily_Usage_Hours": Avg_Daily_Usage_Hours, "Daily_Unlocks": Daily_Unlocks,
        "Study_Hours": Study_Hours, "Physical_Activity_Hours": Physical_Activity_Hours,
        "Sleep_Hours_Per_Night": Sleep_Hours_Per_Night, "Social_Support_Score": Social_Support_Score,
        "Cyberbullying_Exposure": Cyberbullying_Exposure, "Social_Comparison_Level": Social_Comparison_Level,
        "Exercise_Days_Per_Week": Exercise_Days_Per_Week
    }])
    # 1. Predict stress first
    stress = classification_model.predict(user_data)[0]

# 2. Add predicted stress to the input features
    user_data["Stress_Level"] = stress

# 3. Predict the mental health score
    score = float(regression_model.predict(user_data)[0])

# 4. Predict the lifestyle cluster
    cluster_number = int(clustering_model.predict(user_data)[0])
    cluster_names = {
        0: "Balanced Routine",
        1: "Active Lifestyle",
        2: "Younger, Low-Activity Routine",
        3: "High Social-Media Use",
    }
    cluster = cluster_names.get(cluster_number, f"Lifestyle Pattern {cluster_number + 1}")

    st.markdown("## ✨ Your Well-Being Insights")
    st.markdown(
        "<div class='section-note'>Your results at a glance — based on the information you entered.</div>",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3, gap="medium")
    c1.metric("🌿 Predicted Well-Being Score", f"{score:.2f} / 100")
    c2.metric("📊 Predicted Stress Category", str(stress))
    c3.metric("🔎 Lifestyle Cluster", cluster)

    # --- Visual analytics based on the user's actual inputs ---
    st.markdown("## 📈 Your Habit Analytics")
    st.markdown(
        "<div class='section-note'>Explore how your reported daily routine and support factors are distributed.</div>",
        unsafe_allow_html=True,
    )
    # Shared styling keeps the charts consistent with the lavender interface.
    chart_layout = dict(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color="#403456", size=12),
        margin=dict(l=12, r=18, t=28, b=42),
        height=310,
        showlegend=False,
        xaxis=dict(
            showgrid=True,
            gridcolor="#EEEAF5",
            zeroline=False,
            showline=False,
            tickfont=dict(color="#766C87"),
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(color="#403456"),
            automargin=True,
        ),
    )

    chart_left, chart_right = st.columns(2, gap="large")

    with chart_left:
        st.subheader("⏰ Daily Time Allocation")
        time_labels = ["Sleep", "Study", "Physical activity", "Social media"]
        time_values = [
            Sleep_Hours_Per_Night,
            Study_Hours,
            Physical_Activity_Hours,
            Avg_Daily_Usage_Hours,
        ]
        time_fig = go.Figure(
            go.Bar(
                x=time_labels,
                y=time_values,
                marker=dict(
                    color=["#A78BDB", "#C4A7E7", "#E5B8C8", "#8B6BCB"],
                    line=dict(color="#FFFFFF", width=1),
                ),
                text=[f"{value:.1f} h" for value in time_values],
                textposition="outside",
                cliponaxis=False,
                hovertemplate="%{x}: %{y:.1f} hours/day<extra></extra>",
            )
        )
        time_fig.update_layout(**chart_layout)
        time_fig.update_layout(
            height=330,
            bargap=0.42,
            xaxis_title="Daily activity",
            yaxis_title="Hours per day",
        )
        time_fig.update_yaxes(rangemode="tozero")
        st.plotly_chart(time_fig, use_container_width=True, config={"displayModeBar": False})
        st.caption(
            "Compares the number of hours you reported for sleep, study, physical activity "
            "and social-media use."
        )
    with chart_right:
        st.subheader("💜 Social Support vs Comparison")
        # Scatter plot preserves the original scales: support 0–10 and comparison 1–5.
        # It displays this user's profile only; no population or trend is implied.
        factor_fig = go.Figure()
        factor_fig.add_trace(
            go.Scatter(
                x=[Social_Comparison_Level],
                y=[Social_Support_Score],
                mode="markers+text",
                marker=dict(
                    size=22,
                    color="#8B6BCB",
                    line=dict(color="#E9DDF8", width=4),
                ),
                text=["Your profile"],
                textposition="top center",
                hovertemplate=(
                    "Social comparison: %{x} / 5<br>"
                    "Social support: %{y:.1f} / 10<extra></extra>"
                ),
                showlegend=False,
            )
        )
        factor_fig.update_layout(
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font=dict(family="Arial, sans-serif", color="#403456", size=12),
            margin=dict(l=45, r=20, t=35, b=48),
            height=330,
            xaxis=dict(
                title="Social comparison level (1–5)",
                range=[0.7, 5.3],
                dtick=1,
                showgrid=True,
                gridcolor="#EEEAF5",
                zeroline=False,
            ),
            yaxis=dict(
                title="Social support score (0–10)",
                range=[0, 10],
                dtick=2,
                showgrid=True,
                gridcolor="#EEEAF5",
                zeroline=False,
            ),
        )
        st.plotly_chart(factor_fig, use_container_width=True, config={"displayModeBar": False})
        st.caption(
            "The point locates your reported social comparison level and social support score. "
            "It is a snapshot of your answers, not a relationship estimated from multiple people."
        )

    st.subheader("🌿 Predicted Well-Being Score")
    score_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": " / 100", "font": {"size": 34, "color": "#503783"}},
            title={"text": "Model-predicted score", "font": {"size": 14, "color": "#6B5C86"}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": "#B8A9CF",
                    "tickfont": {"color": "#766C87"},
                },
                "bar": {"color": "#8B6BCB", "thickness": 0.28},
                "bgcolor": "#FFFFFF",
                "borderwidth": 1,
                "bordercolor": "#E5DDF0",
                "steps": [
                    {"range": [0, 100], "color": "#F2EDF9"},
                ],
                "threshold": {
                    "line": {"color": "#E5A6BD", "width": 4},
                    "thickness": 0.8,
                    "value": max(0.0, min(100.0, score)),
                },
            },
            domain={"x": [0.08, 0.92], "y": [0.05, 0.95]},
        )
    )
    score_gauge.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial, sans-serif", color="#403456"),
        margin=dict(l=20, r=20, t=35, b=12),
        height=260,
    )
    st.plotly_chart(score_gauge, use_container_width=True, config={"displayModeBar": False})
    st.caption(
        "The gauge displays your model's predicted score on its 0–100 output scale. "
        "It is not a clinical assessment or a comparison with other people."
    )

    st.markdown("## 🔍 Additional Profile Details")
    detail_left, detail_right = st.columns(2)
    with detail_left:
        st.metric("📱 Daily phone unlocks", f"{Daily_Unlocks}")
        st.metric("🏃 Exercise days per week", f"{Exercise_Days_Per_Week} / 7")
    with detail_right:
        st.metric("🌐 Most-used platform", Most_Used_Platform)
        st.metric("🛡️ Cyberbullying exposure", Cyberbullying_Exposure)