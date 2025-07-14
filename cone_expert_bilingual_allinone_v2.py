
import streamlit as st
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.graph_objects as go

st.set_page_config(page_title="Cone Expert - دو زبانه", layout="centered", page_icon="🌀")

# Language Selection
lang = st.sidebar.radio("🌐 Language / زبان", ["English", "فارسی"])

# Translations
T = {
    "English": {
        "title": "🌀 Cone Expert - All Features",
        "inputs": {
            "D": "Large Diameter D (mm)",
            "d": "Small Diameter d (mm)",
            "l": "Cone Length l (mm)",
            "rpm": "Spindle Speed (rpm)",
            "feed": "Feed Rate (mm/rev)",
            "realD": "Real Measured D (optional)",
            "support": "Support Angle (degrees)"
        },
        "sections": {
            "input": "🔢 Input Parameters",
            "angle": "📐 Cone Angle & Taper Ratio",
            "support": "📏 Support Angle",
            "support_rev": "🔄 Reverse Support Calculation",
            "cutting": "⚙️ Cutting Speed & Feed",
            "plot2d": "📊 2D Cone Profile",
            "plot3d": "🧱 3D Cone View"
        },
        "results": {
            "angle": "• Cone Angle α",
            "k": "• Taper Ratio k",
            "error": "• Error from Real D",
            "support": "• Calculated Support Angle",
            "support_rev": "• Calculated small diameter d",
            "cutting": "• Cutting Speed",
            "feed": "• Feed Rate"
        },
        "errors": {
            "invalid": "❗ Invalid input: D > d and l > 0 required.",
            "support_invalid": "❗ Invalid input for reverse support."
        },
        "download": "📥 Download 2D Image"
    },
    "فارسی": {
        "title": "🌀 مخروط‌یار - همه امکانات",
        "inputs": {
            "D": "قطر بزرگ D (میلی‌متر)",
            "d": "قطر کوچک d (میلی‌متر)",
            "l": "طول مخروط l (میلی‌متر)",
            "rpm": "دور اسپیندل (rpm)",
            "feed": "میزان پیشروی (میلی‌متر/دور)",
            "realD": "قطر واقعی D (اختیاری)",
            "support": "زاویه ساپورت (درجه)"
        },
        "sections": {
            "input": "🔢 ورودی‌ها",
            "angle": "📐 زاویه مخروط و نسبت مخروطی",
            "support": "📏 زاویه ساپورت",
            "support_rev": "🔄 محاسبه معکوس ساپورت",
            "cutting": "⚙️ سرعت برش و پیشروی",
            "plot2d": "📊 نمای دو بعدی مخروط",
            "plot3d": "🧱 نمای سه‌بعدی مخروط"
        },
        "results": {
            "angle": "• زاویه مخروط α",
            "k": "• نسبت مخروطی k",
            "error": "• خطا نسبت به مقدار واقعی",
            "support": "• زاویه ساپورت محاسبه‌شده",
            "support_rev": "• قطر کوچک d محاسبه‌شده",
            "cutting": "• سرعت برش",
            "feed": "• نرخ پیشروی"
        },
        "errors": {
            "invalid": "❗ ورودی نادرست: D باید > d و l > 0 باشد.",
            "support_invalid": "❗ ورودی‌های معکوس ساپورت نادرست."
        },
        "download": "📥 دانلود تصویر ۲ بعدی"
    }
}[lang]

st.title(T["title"])

# ========== User Inputs ==========
st.header(T["sections"]["input"])
col1, col2 = st.columns(2)
with col1:
    D = st.number_input(T["inputs"]["D"], value=50.0)
    d = st.number_input(T["inputs"]["d"], value=30.0)
    l = st.number_input(T["inputs"]["l"], value=100.0)
with col2:
    spindle_speed = st.number_input(T["inputs"]["rpm"], value=600)
    feed_per_rev = st.number_input(T["inputs"]["feed"], value=0.2)
    real_D = st.number_input(T["inputs"]["realD"], value=0.0)

# ========== Cone Angle Calculation ==========
st.subheader(T["sections"]["angle"])
if D > d and l > 0:
    delta = D - d
    tan_alpha_2 = delta / (2 * l)
    alpha_deg = math.degrees(math.atan(tan_alpha_2) * 2)
    k = 1 / (2 * tan_alpha_2)

    st.success(f"{T['results']['angle']} = {alpha_deg:.2f}°")
    st.info(f"{T['results']['k']} = {k:.3f}")
    if real_D > 0:
        error_percent = abs(real_D - D) / D * 100
        st.warning(f"{T['results']['error']}: {error_percent:.2f}%")
else:
    st.error(T["errors"]["invalid"])

# ========== Support Angle ==========
st.subheader(T["sections"]["support"])
if D > d and l > 0:
    support_angle = alpha_deg / 2
    st.info(f"{T['results']['support']} ≈ {support_angle:.2f}°")
else:
    st.info("")

# ========== Reverse Support Calculation ==========
st.subheader(T["sections"]["support_rev"])
support_input = st.number_input(T["inputs"]["support"], value=15.0)
mode_rev = st.selectbox("", [T["inputs"]["support"] + " -> d"], index=0)
if st.button(T["sections"]["support_rev"]):
    # calculate small diameter d from support angle and D & l
    if support_input > 0 and D > 0 and l > 0:
        tan_sup = math.tan(math.radians(support_input))
        d_calc = D - 2 * l * tan_sup
        st.success(f"{T['results']['support_rev']} = {d_calc:.2f} mm")
    else:
        st.error(T["errors"]["support_invalid"])

# ========== Cutting Speed & Feed ==========
st.subheader(T["sections"]["cutting"])
V = (math.pi * D * spindle_speed) / 1000
feed_mm_min = feed_per_rev * spindle_speed
st.info(f"{T['results']['cutting']} = {V:.2f} m/min")
st.info(f"{T['results']['feed']} = {feed_mm_min:.2f} mm/min")

# ========== 2D Plot ==========
st.subheader(T["sections"]["plot2d"])
if D > d and l > 0:
    fig, ax = plt.subplots()
    X = [0, l, 0]
    Y_top = [D / 2, 0, d / 2]
    Y_bottom = [-y for y in Y_top]
    ax.plot(X, Y_top, 'r', linewidth=2)
    ax.plot(X, Y_bottom, 'r', linewidth=2)
    ax.fill_between(X, Y_top, Y_bottom, color='orange', alpha=0.3)
    ax.set_title("Cone Profile")
    ax.set_xlabel("Length (mm)")
    ax.set_ylabel("Radius (mm)")
    ax.axis('equal')
    ax.grid(True)
    st.pyplot(fig)
    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="cone_graph.png">{T["download"]}</a>'
    st.markdown(href, unsafe_allow_html=True)

# ========== 3D Plot ==========
st.subheader(T["sections"]["plot3d"])
if D > d and l > 0:
    steps = 50
    height = l
    r1 = D / 2
    r2 = d / 2
    theta = [2 * math.pi * i / steps for i in range(steps)]
    X = []
    Y = []
    Z = []
    for i in range(steps):
        X.append(r1 * math.cos(theta[i]))
        Y.append(r1 * math.sin(theta[i]))
        Z.append(0)
    for i in range(steps):
        X.append(r2 * math.cos(theta[i]))
        Y.append(r2 * math.sin(theta[i]))
        Z.append(height)

    fig3d = go.Figure(data=[go.Mesh3d(x=X, y=Y, z=Z, opacity=0.5, color='orange')])
    fig3d.update_layout(scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z',
    ), title="3D Cone Model")
    st.plotly_chart(fig3d)
