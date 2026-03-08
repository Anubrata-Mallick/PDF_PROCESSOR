# PDF_PROCESSOR
It will extract all text and images from a pdf and store it locally


# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/<<YOUR_USERNAME>>/PDF_PROCESSOR.git
```

```bash
cd PDF_PROCESSOR
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

### Linux / Mac

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the Flask server:

```bash
python app.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---

# API Workflow

Typical workflow:

```
1. POST /process
   Upload a PDF file

2. GET /stats
   Check extracted text and images

3. GET /img/<n>
   Retrieve specific image

4. GET /text/<n>
   Retrieve specific text line

5. POST /cleared
   Remove stored data
```

---


# 1. Process PDF

Uploads a PDF file and extracts text and images.

### Endpoint

```
POST /process
```

### What it does

* Accepts a PDF file
* Extracts all text lines
* Extracts all images
* Saves text in `text.txt`
* Saves images in `images/`

### Example using curl

```bash
curl -X POST http://127.0.0.1:5000/process \
-F "file=@sample.pdf"
```

---

### Example using Express.js

Install dependency:

```bash
npm install axios form-data fs
```

Example code:

```javascript
const axios = require("axios")
const FormData = require("form-data")
const fs = require("fs")

async function uploadPDF(){

    const form = new FormData()
    form.append("file", fs.createReadStream("sample.pdf"))

    const response = await axios.post(
        "http://127.0.0.1:5000/process",
        form,
        { headers: form.getHeaders() }
    )

    console.log(response.data)
}

uploadPDF()
```

---

# 2. Get Statistics

Returns number of extracted text lines and images.

### Endpoint

```
GET /stats
```

### Example response

```json
{
  "total_text_lines": 120,
  "total_images": 3
}
```

---

### Example using curl

```bash
curl http://127.0.0.1:5000/stats
```

---

### Example using Express.js

```javascript
const axios = require("axios")

async function getStats(){

    const response = await axios.get("http://127.0.0.1:5000/stats")

    console.log(response.data)
}

getStats()
```

---

# 3. Get Image

Returns a specific extracted image.

### Endpoint

```
GET /img/<number>
```

Example:

```
GET /img/0
GET /img/1
```

---

### Example using curl

```bash
curl http://127.0.0.1:5000/img/0 --output img0.png
```

---

### Example using Express.js

```javascript
const axios = require("axios")
const fs = require("fs")

async function getImage(){

    const response = await axios.get(
        "http://127.0.0.1:5000/img/0",
        { responseType: "stream" }
    )

    response.data.pipe(fs.createWriteStream("image0.png"))
}

getImage()
```

---

# 4. Get Text Line

Returns a specific extracted text line.

### Endpoint

```
GET /text/<number>
```

Example:

```
GET /text/5
```

---

### Example Response

```json
{
  "line_number": 5,
  "text": "This is an extracted sentence."
}
```

---

### Example using curl

```bash
curl http://127.0.0.1:5000/text/5
```

---

### Example using Express.js

```javascript
const axios = require("axios")

async function getText(){

    const response = await axios.get("http://127.0.0.1:5000/text/5")

    console.log(response.data)
}

getText()
```

---

# 5. Clear Stored Data

Deletes extracted text and images.

### Endpoint

```
POST /cleared
```

### What it does

* Deletes `text.txt`
* Deletes all images in `images/`

---

### Example using curl

```bash
curl -X POST http://127.0.0.1:5000/cleared
```

---

### Example using Express.js

```javascript
const axios = require("axios")

async function clearData(){

    const response = await axios.post("http://127.0.0.1:5000/cleared")

    console.log(response.data)
}

clearData()
```

---


