from flask import Flask, request, jsonify, send_file
import fitz  # PyMuPDF
import os

app = Flask(__name__)

TEXT_FILE = "text.txt"
IMG_FOLDER = "images"

os.makedirs(IMG_FOLDER, exist_ok=True)


@app.route("/process", methods=["POST"])
def process_pdf():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["file"]
    pdf_path = "uploaded.pdf"
    pdf_file.save(pdf_path)

    doc = fitz.open(pdf_path)

    texts = []
    img_count = 0
    seen_xrefs = set()

    for page in doc:

        # Extract text
        text = page.get_text()
        lines = text.split("\n")
        texts.extend([line for line in lines if line.strip()])

        # Extract images
        images = page.get_images(full=True)

        for img in images:
            xref = img[0]

            if xref in seen_xrefs:
                continue

            seen_xrefs.add(xref)

            base_img = doc.extract_image(xref)
            img_bytes = base_img["image"]
            img_ext = base_img["ext"]

            img_name = f"{IMG_FOLDER}/img_{img_count}.{img_ext}"

            with open(img_name, "wb") as f:
                f.write(img_bytes)

            img_count += 1

    # Save text file
    with open(TEXT_FILE, "w", encoding="utf-8") as f:
        for line in texts:
            f.write(line + "\n")

    # Close PDF
    doc.close()

    # Delete uploaded pdf
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return jsonify({
        "message": "PDF processed successfully",
        "text_lines": len(texts),
        "images_extracted": img_count
    })

@app.route("/stats", methods=["GET"])
def stats():

    text_lines = 0
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r", encoding="utf-8") as f:
            text_lines = len(f.readlines())

    img_count = len(os.listdir(IMG_FOLDER))

    return jsonify({
        "total_text_lines": text_lines,
        "total_images": img_count
    })


@app.route("/img/<int:no>", methods=["GET"])
def get_image(no):

    files = sorted(os.listdir(IMG_FOLDER))

    if no >= len(files):
        return jsonify({"error": "Image not found"}), 404

    img_path = os.path.join(IMG_FOLDER, files[no])
    return send_file(img_path)


@app.route("/text/<int:no>", methods=["GET"])
def get_text(no):

    if not os.path.exists(TEXT_FILE):
        return jsonify({"error": "Text file not found"}), 404

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if no >= len(lines):
        return jsonify({"error": "Line not found"}), 404

    return jsonify({
        "line_number": no,
        "text": lines[no].strip()
    })

@app.route("/cleared", methods=["POST"])
def clear_data():

    
    if os.path.exists(TEXT_FILE):
        os.remove(TEXT_FILE)

    
    if os.path.exists(IMG_FOLDER):
        for file in os.listdir(IMG_FOLDER):
            file_path = os.path.join(IMG_FOLDER, file)
            os.remove(file_path)

    return jsonify({
        "message": "Stored text and images cleared successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)