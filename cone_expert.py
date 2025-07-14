
import streamlit as st
import math
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import base64

# ========== Language & Theme Setup ==========
st.set_page_config(page_title="Cone Expert", layout="centered", page_icon="🌀")

# --- Language toggle ---
lang = st.sidebar.radio("🌐 Language / زبان", ("English", "فارسی"))

# --- Theme switch (dark/light) ---
theme = st.sidebar.selectbox("🎨 Theme", ["Modern Light", "Engineering Dark"])
if theme == "Engineering Dark":
    st.markdown(
        "<style>body { background-color: #0e1117; color: white; }</style>",
        unsafe_allow_html=True
    )

# ========== Texts ==========
texts = {
    "English": {
        "title": "🌀 Cone Expert",
        "mode": "Calculation Mode",
        "mode1": "Calculate angle from D, d, l",
        "mode2": "Calculate D/d/l from angle",
        "inputs": {
            "D": "Large diameter D (mm)",
            "d": "Small diameter d (mm)",
            "l": "Cone length l (mm)",
            "alpha": "Cone angle α (degrees)"
        },
        "submit": "Calculate",
        "error": "⚠️ Please enter valid dimensions. D must be greater than d and l > 0.",
        "results": {
            "angle": "Cone angle α",
            "k": "Taper ratio k",
            "download": "📥 Download Graph as Image"
        }
    },
    "فارسی": {
        "title": "🌀 مخروط‌یار",
        "mode": "حالت محاسبه",
        "mode1": "محاسبه زاویه از D، d، l",
        "mode2": "محاسبه D یا d یا l از زاویه",
        "inputs": {
            "D": "قطر بزرگ D (میلی‌متر)",
            "d": "قطر کوچک d (میلی‌متر)",
            "l": "طول مخروط l (میلی‌متر)",
            "alpha": "زاویه مخروط α (درجه)"
        },
        "submit": "محاسبه",
        "error": "⚠️ لطفاً مقادیر معتبر وارد کنید. D باید از d بزرگ‌تر و l > ۰ باشد.",
        "results": {
            "angle": "زاویه مخروط α",
            "k": "ضریب مخروطی بودن k",
            "download": "📥 دانلود تصویر گراف"
        }
    }
}

T = texts[lang]

# ========== UI ==========
st.title(T["title"])
mode = st.selectbox(T["mode"], (T["mode1"], T["mode2"]))

# ========== Mode 1: D, d, l => α ==========
if mode == T["mode1"]:
    D = st.number_input(T["inputs"]["D"], min_value=0.0, value=50.0)
    d = st.number_input(T["inputs"]["d"], min_value=0.0, value=30.0)
    l = st.number_input(T["inputs"]["l"], min_value=0.1, value=100.0)

    if st.button(T["submit"]):
        if D > d and l > 0:
            delta = D - d
            tan_alpha_2 = delta / (2 * l)
            alpha_rad = math.atan(tan_alpha_2) * 2
            alpha_deg = math.degrees(alpha_rad)
            k = 1 / (2 * tan_alpha_2)

            st.success(f"🔺 {T['results']['angle']} = {alpha_deg:.2f}°")
            st.info(f"📏 {T['results']['k']} = {k:.3f}")

            # Plot
            fig, ax = plt.subplots()
            X = [0, l, 0]
            Y_top = [D / 2, 0, d / 2]
            Y_bottom = [-y for y in Y_top]
            ax.plot(X, Y_top, 'r', linewidth=2)
            ax.plot(X, Y_bottom, 'r', linewidth=2)
            ax.fill_between(X, Y_top, Y_bottom, color='orange', alpha=0.3)
            ax.set_title(T["title"])
            ax.set_xlabel("L")
            ax.set_ylabel("Diameter")
            ax.axis('equal')
            ax.grid(True)
            st.pyplot(fig)

            # Image Download
            buffer = BytesIO()
            fig.savefig(buffer, format="png")
            buffer.seek(0)
            b64 = base64.b64encode(buffer.read()).decode()
            href = f'<a href="data:file/png;base64,{b64}" download="cone_graph.png">{T["results"]["download"]}</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.error(T["error"])

# ========== Mode 2: α + 2 known => compute unknown ==========
elif mode == T["mode2"]:
    alpha_deg = st.number_input(T["inputs"]["alpha"], min_value=0.1, value=30.0)
    known = st.selectbox("🔧 Choose known parameters", ["D & d", "D & l", "d & l"])

    if known == "D & d":
        D = st.number_input(T["inputs"]["D"], min_value=0.0, value=50.0)
        d = st.number_input(T["inputs"]["d"], min_value=0.0, value=30.0)
        if D > d:
            tan_alpha_2 = math.tan(math.radians(alpha_deg / 2))
            l = (D - d) / (2 * tan_alpha_2)
            st.success(f"📏 {T['inputs']['l']} = {l:.2f} mm")
        else:
            st.error(T["error"])

    elif known == "D & l":
        D = st.number_input(T["inputs"]["D"], min_value=0.0, value=50.0)
        l = st.number_input(T["inputs"]["l"], min_value=0.1, value=100.0)
        tan_alpha_2 = math.tan(math.radians(alpha_deg / 2))
        d = D - 2 * l * tan_alpha_2
        st.success(f"📏 {T['inputs']['d']} = {d:.2f} mm")

    elif known == "d & l":
        d = st.number_input(T["inputs"]["d"], min_value=0.0, value=30.0)
        l = st.number_input(T["inputs"]["l"], min_value=0.1, value=100.0)
        tan_alpha_2 = math.tan(math.radians(alpha_deg / 2))
        D = d + 2 * l * tan_alpha_2
        st.success(f"📏 {T['inputs']['D']} = {D:.2f} mm")
