from weasyprint import HTML

# Content for the README.md
readme_content = """# Student Performance & Management System

A Python-based Management Information System (MIS) designed to handle student academic records, extracurricular activities (ECA), and administrative analytics. This system features a dual-portal interface for **Admins** and **Students**, utilizing Object-Oriented Programming (OOP) principles and data persistence via CSV-formatted text files.

## 🚀 Key Features

### Admin Portal
- **Student Management:** Add, modify, or delete student records and academic grades.
- **Advanced Analytics:** Generate class-wide performance dashboards including:
  - Subject averages (Bar charts).
  - Grade trends (Line graphs).
  - ECA vs. Academic performance correlation (Scatter plots).
- **Automated Ranking:** View the top 3 students based on overall averages with a leaderboard.
- **Performance Alerts:** Identify students needing academic improvement based on a 60% threshold.

### Student Portal
- **Profile Management:** View personal details, subject-wise grades, and total ECA hours.
- **Personal Dashboard:** Visualize individual academic performance through interactive graphs.
- **Report Card Generation:** Download an official, professionally styled **PDF Report Card** containing grades and ECA achievements.
- **Self-Service:** Update personal profile details like full name.

## 🛠️ Technical Stack
- **Language:** Python 3.x
- **Data Handling:** `pandas` (for CSV manipulation and filtering)
- **Data Visualization:** `matplotlib` (for generating performance charts)
- **PDF Generation:** `fpdf` (for creating downloadable report cards)
- **Database:** Flat-file system (`.txt` files managed as CSVs)

## 📂 Project Structure
- `Main.py`: The core application script containing class definitions and system logic.
- `users.txt`: Stores user profile information (ID, Role, Name, Age).
- `passwords.txt`: Stores login credentials.
- `grades.txt`: Stores subject-wise academic scores.
- `eca.txt`: Stores extracurricular activity names and hours.

## 🔧 Installation & Setup

1. **Clone the repository or download the script.**
2. **Install the required dependencies:**
   ```bash
   pip install pandas matplotlib fpdf
