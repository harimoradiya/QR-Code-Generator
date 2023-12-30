import qrcode
import streamlit as st
import io
import base64
import os
from datetime import datetime

def generate_qr_code(data, size=300, fg_color="black", bg_color="white", error_correction=qrcode.constants.ERROR_CORRECT_L):
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color, back_color=bg_color)
    img = img.resize((size, size))

    return img


# Function to display history
def display_history(history):
    if history:
        st.subheader("History")
        for item in history:
            st.image(item["image"], caption=item["caption"], use_column_width=False)
            st.markdown(f"**Generated on:** {item['generated_on']}")


os.makedirs('qrcodes', exist_ok=True)

# Streamlit UI
st.set_page_config(
    page_title="QR Code Generator",
    page_icon=":sunglasses:",
    layout="wide"
)

# Navigation Drawer
st.sidebar.title("QR Code Generator")

# Input text for the QR code
text_input = st.sidebar.text_input("Enter text for QR code")

qr_size = st.sidebar.slider("QR Code Size", 100, 500, 300)
fg_color = st.sidebar.color_picker("Foreground Color", "#000000")
bg_color = st.sidebar.color_picker("Background Color", "#FFFFFF")
error_correction = st.sidebar.selectbox("Error Correction Level", ["L", "M", "Q", "H"])

generate_history = st.sidebar.checkbox("Generate QR Code History")

col1, col2 = st.columns([1,2])


if text_input:
    
    qr_code = generate_qr_code(text_input, size=qr_size, fg_color=fg_color, bg_color=bg_color,
                                error_correction=qrcode.constants.ERROR_CORRECT_L if error_correction == "L" else
                                                 qrcode.constants.ERROR_CORRECT_M if error_correction == "M" else
                                                 qrcode.constants.ERROR_CORRECT_Q if error_correction == "Q" else
                                                 qrcode.constants.ERROR_CORRECT_H)



    #Display generated qr code 
    col2.image(qr_code, caption="Generated QR Code", use_column_width=False)

    
    file_name = f"qrcodes/{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    qr_code.save(file_name, format="PNG")

    # For downloading the image we need to convert that image object into the byte array
    img_byte_array = io.BytesIO()
    qr_code.save(img_byte_array, format="PNG")
    img_bytes = img_byte_array.getvalue()

    # Encode as base64
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    href = f'<a href="data:application/octet-stream;base64,{img_base64}" download="qrcode.png">Download QR Code</a>'
    
    col2.markdown(href, unsafe_allow_html=True)


    # Generate QR Code History
    if generate_history:
        # Get the cached history or initialize an empty list
        qr_history = st.session_state.get("qr_history", [])

        # Append the current QR code to the history
        qr_history.append({"image": qr_code, "caption": "Generated QR Code", "generated_on": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

        # Update the cached history
        st.session_state.qr_history = qr_history

        # Display the history
        display_history(qr_history)
