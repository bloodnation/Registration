# Student Registration System

This is a web-based application for managing student registrations. It allows users to register students, check registration status, and export data in JSON, Excel, and PDF formats.

## Features

- **Student Registration**: Register new students with details such as name, mobile number, ID number, email, gender, residence, emergency contacts, and course.
- **Check Registration**: Check if a student is already registered using their ID number, email, or mobile number.
- **Data Export**: Export student data to JSON, Excel, or PDF formats.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Libraries**:
  - `pandas`: For data manipulation and exporting to JSON/Excel.
  - `reportlab`: For generating PDF files.
  - `xlsxwriter`: For exporting data to Excel files.

## Project Structure

```
student-registration-system/
│
├── app.py                  # Flask backend
├── static/                 # Static files (CSS, JS, etc.)
│   └── styles.css
├── templates/              # HTML templates
│   └── index.html
├── student_registration.db  # SQLite database
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- pandas
- reportlab
- xlsxwriter

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bloodnation/Registration.git
   cd Registration
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file, install the dependencies manually:
   ```bash
   pip install Flask pandas reportlab xlsxwriter
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Register a Student**:
   - Fill out the registration form and click **Submit**.
   - If successful, you'll receive a registration number.

2. **Check Registration**:
   - Enter the student's ID number, email, or mobile number and click **Check Registration**.

3. **Export Data**:
   - Click **Export to JSON**, **Export to Excel**, or **Export to PDF** to download the student data in the respective format.

## API Endpoints

- **`POST /register`**: Register a new student.
- **`POST /check-registration`**: Check if a student is already registered.
- **`GET /export-json`**: Export student data to JSON.
- **`GET /export-excel`**: Export student data to Excel.
- **`GET /export-pdf`**: Export student data to PDF.

## Screenshots

![Student Registration Form](screenshots/form.png)
![Exported Data](screenshots/export.png)

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
