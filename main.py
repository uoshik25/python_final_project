import time
import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

FILES = {
    'users': 'users.txt',
    'grades': 'grades.txt',
    'eca': 'eca.txt',
    'passwords': 'passwords.txt'
}

def initialize_files():
    """Ensures all 4 text files exist with headers and dummy data."""
    if not os.path.exists(FILES['passwords']):
        with open(FILES['passwords'], 'w') as f:
            f.write("username,password\nadmin1,pass123\nstudent1,pass123\n")
    if not os.path.exists(FILES['users']):
        with open(FILES['users'], 'w') as f:
            f.write("user_id,username,role,name,age\nID001,admin1,admin,Admin Alice,30\nID002,student1,student,Bob Smith,20\n")
    if not os.path.exists(FILES['grades']):
        with open(FILES['grades'], 'w') as f:
            f.write("user_id,math,science,english,history,art\nID002,85,90,78,88,92\n")
    if not os.path.exists(FILES['eca']):
        with open(FILES['eca'], 'w') as f:
            f.write("user_id,activity,hours\nID002,Debate Club,10\n")


def wait_and_clear(seconds=1.5):
    time.sleep(seconds)
    os.system('cls' if os.name == 'nt' else 'clear')

def authorize(ad_user, ad_pass):
    return ad_user == "admin@123" and ad_pass == "admin123#"

def id_generator():
    """Safely generates a new ID like ID003 using Pandas."""
    try:
        df = pd.read_csv(FILES['users'])
        if df.empty: return "ID001"
        last_id = str(df.iloc[-1]['user_id'])
        number = int(last_id.replace("ID", "")) + 1
        return f"ID{number:03d}"
    except Exception:
        return "ID001"

def user_exists(username):
    try:
        df = pd.read_csv(FILES['passwords'])
        return username in df['username'].values
    except:
        return False



class User:
    def __init__(self, user_id, username, role, name):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.name = name

class Student(User):
    def view_profile(self):
        print("\n"+ "="*45)
        print(f"📄 STUDENT PROFILE: {self.name}")
        print("="*45)
        '''print(f"\n--- Records for {self.name} ({self.user_id}) ---")'''
        try:
            df_g = pd.read_csv(FILES['grades'])
            my_g = df_g[df_g['user_id'].astype(str) == str(self.user_id)]
            
            if not my_g.empty:
                print("\n📘 Grades:")
                print("-"*45)
                for col in my_g.columns[1:]:
                    print(f"{col.capitalize():<15}: {my_g.iloc[0][col]}")
            else:
                print("\nNo grades found.")

            df_e = pd.read_csv(FILES['eca'])
            my_e = df_e[df_e['user_id'].astype(str) == str(self.user_id)]
            if not my_e.empty:
                print("\n🎯 ECA Activities:")
                print("-"*45)
                for _, row in my_e.iterrows():
                    print(f"Activity : {row['activity']}")
                    print(f"Hours    : {row['hours']}")
                    print("-"*30)
            else:
                print("\nNo ECA records found.")

        except Exception as e:
            print(f"Error loading data: {e}")

    def update_profile_name(self):
        new_name = input("Enter your new full name: ")
        try:
            df = pd.read_csv(FILES['users'])
            df.loc[df['user_id'].astype(str) == str(self.user_id), 'name'] = new_name
            df.to_csv(FILES['users'], index=False)
            self.name = new_name
            print("[✓] Name updated successfully.")
        except Exception as e:
            print(f"Error updating name: {e}")

    def performance_dashboard(self):
        try:
            print("\n" + "="*45)
            print("📊 YOUR PERFORMANCE DASHBOARD")
            print("="*45)

            df = pd.read_csv(FILES['grades'])

            student_data = df[df['user_id'].astype(str) == str(self.user_id)]

            if student_data.empty:
                print("No records found.")
                return

            subjects = df.columns[1:]
            scores = student_data.iloc[0, 1:]

            # TEXT SUMMARY
            print("\n📘 Subject-wise Marks:")
            print("-"*45)

            total = 0
            for sub, mark in zip(subjects, scores):
                print(f"{sub.capitalize():<15}: {mark}")
                total += mark

            avg = total / len(subjects)

            print("-"*45)
            print(f"📊 Average Score : {avg:.2f}")

            if avg >= 80:
                print("🏆 Performance   : Excellent")
            elif avg >= 60:
                print("👍 Performance   : Good")
            else:
                print("⚠️ Performance   : Needs Improvement")

            # GRAPH
            plt.figure(figsize=(8, 5))
            plt.bar(subjects, scores)
            plt.title('Your Subject Scores')
            plt.ylabel('Marks')
            plt.ylim(0, 100)
            plt.show()


        except Exception as e:
            print(f"Dashboard Error: {e}")

    def download_report_card(self):
            """Feature: Allows the student to generate and download their own PDF report card."""
            print("\n" + "="*45)
            print("📄 GENERATING YOUR OFFICIAL REPORT CARD")
            print("="*45)
            
            try:
                # 1. Fetch Data using self.user_id
                df_u = pd.read_csv(FILES['users'])
                df_g = pd.read_csv(FILES['grades'])
                df_e = pd.read_csv(FILES['eca'])

                student = df_u[df_u['user_id'] == self.user_id]
                grades = df_g[df_g['user_id'] == self.user_id]
                eca = df_e[df_e['user_id'] == self.user_id]

                if grades.empty:
                    print("[!] No grade records found to generate a report.")
                    return

                # 2. PDF Setup
                pdf = FPDF()
                pdf.add_page()
                
                # Header Styling
                pdf.set_font("Arial", 'B', 22)
                pdf.set_text_color(44, 62, 80) # Dark Blue
                pdf.cell(200, 15, "STUDENT PROGRESS REPORT", ln=True, align='C')
                pdf.ln(5)
                
                # Profile Section
                pdf.set_font("Arial", 'B', 12)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(100, 10, f"Name: {self.name}", ln=False)
                pdf.cell(100, 10, f"Student ID: {self.user_id}", ln=True)
                pdf.cell(100, 10, f"Age: {student.iloc[0]['age']}", ln=False)
                pdf.cell(100, 10, f"Status: Active", ln=True)
                pdf.ln(10)

                # Grades Table
                pdf.set_fill_color(52, 152, 219) # Professional Blue
                pdf.set_text_color(255, 255, 255) # White text
                pdf.cell(95, 10, "Subject", 1, 0, 'C', True)
                pdf.cell(95, 10, "Score", 1, 1, 'C', True)
                
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", '', 12)
                subjects = df_g.columns[1:]
                total = 0
                for sub in subjects:
                    val = grades.iloc[0][sub]
                    pdf.cell(95, 10, sub.capitalize(), 1)
                    pdf.cell(95, 10, str(val), 1, 1, 'C')
                    total += val
                
                # Summary Calculation
                avg = total / len(subjects)
                pdf.set_font("Arial", 'B', 12)
                pdf.set_fill_color(236, 240, 241) # Light Grey
                pdf.cell(95, 10, "OVERALL PERCENTAGE", 1, 0, 'L', True)
                pdf.cell(95, 10, f"{avg:.2f}%", 1, 1, 'C', True)
                pdf.ln(10)

                # ECA Section
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(200, 10, "Extracurricular Achievements", ln=True)
                pdf.set_font("Arial", '', 12)
                if not eca.empty:
                    for _, row in eca.iterrows():
                        pdf.cell(200, 10, f"• {row['activity']} - {row['hours']} Hours Participated", ln=True)
                else:
                    pdf.cell(200, 10, "No activities registered.", ln=True)

                # 3. Output
                filename = f"MyReport_{self.user_id}.pdf"
                pdf.output(filename)
                print(f"\n[✓] Success! Your report has been saved as: {filename}")

            except Exception as e:
                print(f"Error creating report: {e}")

class Admin(User):
    def __init__(self, user_id, username, role, name):
        super().__init__(user_id, username, role, name)

    def top_3_students(self):
        df_g = pd.read_csv(FILES['grades'])
        df_u = pd.read_csv(FILES['users'])

        # calculate average
        df_g['avg'] = df_g.iloc[:, 1:].mean(axis=1)

        # merge to get names
        merged = pd.merge(df_g, df_u, on='user_id')

        # sort by average
        top = merged.sort_values(by='avg', ascending=False).head(3)

        medals = ["🥇", "🥈", "🥉"]

        print("\n🏆 TOP 3 STUDENTS")
        print("-" * 40)

        for i, (_, row) in enumerate(top.iterrows()):
            print(f"{medals[i]} {row['name']} {row['user_id']} → Average: {row['avg']:.2f}")
    

    def student_wise_performance(self):
        df = pd.read_csv(FILES['grades'])

        print("\nEnter Student ID to view performance:")
        sid = input("ID (e.g. ID002): ")

        student = df[df['user_id'].astype(str) == sid]

        if student.empty:
            print("Student not found.")
            return

        subjects = df.columns[1:]
        scores = student.iloc[0, 1:]

        print(f"\n📄 Performance for {sid}")
        print("-"*40)

        total = 0
        for sub, mark in zip(subjects, scores):
            print(f"{sub}: {mark}")
            total += mark

        avg = total / len(subjects)
        print("-"*40)
        print(f"Average: {avg:.2f}")
        percentage = (avg / 100) * 100
        print(f"Percentage: {percentage:.2f}%")

        plt.figure(figsize=(6,4))
        plt.bar(subjects, scores)
        plt.title(f"Performance of {sid}")
        plt.ylim(0,100)
        plt.show()


    def performance_dashboard(self):
        try:
            print("\n[📊] Generating Full Class Analytics Dashboard...")
            
            # =========================
            # 1. LOAD GRADES
            # =========================
            df_g = pd.read_csv(FILES['grades'])
            
            if df_g.empty:
                print("No grade data available.")
                return

            subjects = df_g.columns[1:]
            averages = df_g.drop('user_id', axis=1).mean()

            # =========================
            # 2. CLASS AVERAGES (BAR CHART)
            # =========================
            plt.figure(figsize=(8, 5))
            plt.bar(subjects, averages)
            plt.title("Class Subject Averages")
            plt.ylabel("Average Score")
            plt.xlabel("Subjects")
            plt.ylim(0, 100)
            plt.grid(axis='y')
            plt.show()

            # =========================
            # 3. GRADE TREND (LINE GRAPH)
            # =========================
            plt.figure(figsize=(8, 5))
            plt.plot(subjects, averages, marker='o')
            plt.title("Grade Trend Across Subjects")
            plt.ylabel("Average Score")
            plt.xlabel("Subjects")
            plt.grid()
            plt.show()

            # =========================
            # 4. ECA vs PERFORMANCE (SCATTER PLOT)
            # =========================
            try:
                df_e = pd.read_csv(FILES['eca'])

                df_g['avg_score'] = df_g.iloc[:, 1:].astype(float).mean(axis=1)
                df_e['hours'] = df_e['hours'].astype(float)

                merged = pd.merge(df_g, df_e, on='user_id')
                merged['avg_score'] = merged.iloc[:, 1:6].mean(axis=1)

                plt.figure(figsize=(8, 5))
                plt.scatter(merged['hours'], merged['avg_score'])
                plt.title("ECA Impact on Academic Performance")
                plt.xlabel("ECA Hours")
                plt.ylabel("Average Score")
                plt.grid()
                plt.show()

            except Exception as e:
                print("ECA analysis skipped (data mismatch):", e)

            # =========================
            # 5. PERFORMANCE ALERTS
            # =========================
            df_g['avg'] = df_g.iloc[:, 1:].mean(axis=1)

            weak_students = df_g[df_g['avg'] < 60]

            print("\n⚠️ Students Needing Improvement:")
            if weak_students.empty:
                print("All students are performing well 👍")
            else:
                for _, row in weak_students.iterrows():
                    print(f"{row['user_id']} → Avg: {row['avg']:.2f}")
                    print("Suggestion: Extra tutoring / revision plan")

        except Exception as e:
            print(f"Dashboard Error: {e}")

    def modify_student(self):
        """Update student name OR grades."""
        target_id = input("Enter Student ID to modify (e.g., ID002): ")

        try:
            df_users = pd.read_csv(FILES['users'])
            df_grades = pd.read_csv(FILES['grades'])

            if target_id not in df_users['user_id'].astype(str).values:
                print("[!] Student ID not found.")
                return

            print("\nWhat do you want to modify?")
            print("1. Name")
            print("2. Grades")

            choice = input("Select option: ")

            # ======================
            # 1. MODIFY NAME
            # ======================
            if choice == '1':
                new_name = input("Enter new name: ")
                df_users.loc[df_users['user_id'].astype(str) == target_id, 'name'] = new_name
                df_users.to_csv(FILES['users'], index=False)
                print("[✓] Name updated successfully.")

            # ======================
            # 2. MODIFY GRADES
            # ======================
            elif choice == '2':
                print("\nEnter new marks:")

                math = float(input("Math: "))
                science = float(input("Science: "))
                english = float(input("English: "))
                history = float(input("History: "))
                art = float(input("Art: "))

                df_grades.loc[df_grades['user_id'].astype(str) == target_id,
                            ['math', 'science', 'english', 'history', 'art']] = [math, science, english, history, art]
                df_grades.to_csv(FILES['grades'], index=False)
                print("[✓] Grades updated successfully.")

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Error modifying file: {e}")

    def delete_record(self):

        target_id = input("Enter Student ID to delete (e.g., ID002): ")
        
        try:
            df_users = pd.read_csv(FILES['users'])
            user_row = df_users[df_users['user_id'].astype(str) == target_id]
            if user_row.empty:
                print("[!] Student ID not found.")
                return
            target_username = user_row.iloc[0]['username']
        except:
            print("Error reading user records.")
            return

        for file_key, filepath in FILES.items():
            try:
                df = pd.read_csv(filepath)
                if file_key == 'passwords':
                    df = df[df['username'].astype(str) != target_username]
                else:
                    df = df[df['user_id'].astype(str) != target_id]
                df.to_csv(filepath, index=False)
            except Exception as e:
                pass 

        print(f"[✓] All records for {target_id} deleted.")

    def add_student_record(self):
        """Task: Add a new student and their academic/ECA data."""
        print("\n--- Register New Student ---")
        username = input("Enter Username: ")
        if user_exists(username):
            print("[!] Username already exists.")
            return

        password = input("Enter Password: ")
        name = input("Enter Full Name: ")
        age = input("Enter Age: ")
        
        # 1. Generate ID and Save Credentials
        new_id = id_generator()
        
        try:
            # Update passwords.txt
            with open(FILES['passwords'], "a") as f:
                f.write(f"{username},{password}\n")
            
            # Update users.txt
            with open(FILES['users'], "a") as f:
                f.write(f"{new_id},{username},student,{name},{age}\n")

            # 2. Collect Grades
            print("\n--- Enter Academic Grades ---")
            math = input("Math Score: ")
            science = input("Science Score: ")
            english = input("English Score: ")
            history = input("History Score: ")
            art = input("Art Score: ")
            
            with open(FILES['grades'], "a") as f:
                f.write(f"{new_id},{math},{science},{english},{history},{art}\n")

            # 3. Collect ECA
            print("\n--- Enter ECA Details ---")
            activity = input("Activity Name: ")
            hours = input("Total Hours: ")
            
            with open(FILES['eca'], "a") as f:
                f.write(f"{new_id},{activity},{hours}\n")

            print(f"\n[✓] Student {name} added successfully with ID: {new_id}")
            
        except Exception as e:
            print(f"Error adding record: {e}")

def sign_up_logic(user, password, re_pass, role):
    if password != re_pass:
        return "Passwords do not match."
    if user_exists(user):
        return "Username already exists."
    
    try:
        user_id = id_generator()
        name = input("Enter Full Name: ")
        age = input("Enter Age: ")

        # Append to files
        with open(FILES['passwords'], "a") as pw:
            pw.write(f"{user},{password}\n")
        with open(FILES['users'], "a") as us:
            us.write(f"{user_id},{user},{role.lower()},{name},{age}\n")
        
        return f"Signed Up Successfully! Assigned ID: {user_id}"
    except Exception as e:
        return f"Error during signup: {e}"

def login_system():
    print("======= LogIn =======\n")
    att = 3
    for i in range(att):
        u = input("Username: ").strip()
        p = input("Password: ").strip()

        print(f"\nAttempts remaining: {att-1}")
        att -=1 
    
        try:
            df_p = pd.read_csv(FILES['passwords'])
            match = df_p[(df_p['username'] == u) & (df_p['password'] == p)]
            
            if not match.empty:
                df_u = pd.read_csv(FILES['users'])
                user_data = df_u[df_u['username'] == u].iloc[0]
                
                if user_data['role'] == 'admin':
                    return Admin(user_data['user_id'], u, 'admin', user_data['name'])
                else:
                    return Student(user_data['user_id'], u, 'student', user_data['name'])
                
        except Exception:
            pass
    
    print("[!] Invalid username or password.")
    return None

def admin_menu(admin_obj):
    while True:
        wait_and_clear(1)
        print(f"======= Admin Dashboard: {admin_obj.name} =======")
        print("1. View All Records")
        print("2. Modify Student Record")
        print("3. Delete Student Record")
        print("4. Analytics Dashboard (Task 2)")
        print("5. Add Student Record")
        print("6. View student-wise performance")
        print("7. View Top 3 Students")
        print("8. Log Out")
        
        ch = input("\nSelect an option: ")
        if ch == '1':
            try:
                df = pd.read_csv(FILES['users'])

                df = df[df['role'] == 'student']

                print("\n" + "="*60)
                print("📋 ALL STUDENT RECORDS")
                print("="*60)

                for _, row in df.iterrows():
                    print("-"*60)
                    print(f"ID       : {row['user_id']}")
                    print(f"Username : {row['username']}")
                    print(f"Role     : {row['role']}")
                    print(f"Name     : {row['name']}")
                    print(f"Age      : {row['age']}")

            except Exception as e:
                print(f"[Error] Unable to load records: {e}")
                
            input("\nPress Enter to return...")
        elif ch == '2':
            admin_obj.modify_student()
            input("\nPress Enter to return...")
        elif ch == '3':
            admin_obj.delete_record()
            input("\nPress Enter to return...")
        elif ch == '4':
            admin_obj.performance_dashboard()
            input("\nPress Enter to return...")
        elif ch == '5':
            admin_obj.add_student_record()
            input("\nPress Enter to return...")
        elif ch == '6':
            admin_obj.student_wise_performance()
            input("\nPress Enter to return...")
        elif ch == '7':
            admin_obj.top_3_students()
            input("\nPress Enter to return...")
        elif ch== '8':
            break

def student_menu(student_obj):
    while True:
        wait_and_clear(1)
        print(f"======= Student Portal: {student_obj.name} =======")
        print("1. View My Profile, Grades & ECA")
        print("2. Update My Name")
        print("3. View my performance")
        print("4. Download Report Card")
        print("5. Log Out")
        
        ch = input("\nSelect an option: ")
        if ch == '1':
            student_obj.view_profile()
            input("\nPress Enter to return...")
        elif ch == '2':
            student_obj.update_profile_name()
            input("\nPress Enter to return...")
        elif ch == '3':
            student_obj.performance_dashboard()
            input("\nPress Enter to return...")
        elif ch == '4':
            student_obj.download_report_card()
            input("\nPress Enter to return...")
        elif ch == '5':
            break


def main():
    initialize_files()
    while True:
        wait_and_clear(1)
        print("======= System Main Menu =======")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            wait_and_clear(0.5)
            print("--- Sign Up ---")
            print("1. Admin | 2. Student")
            role_choice = input("Select role for signup: ")
            
            if role_choice == '1':
                u, p = input("Auth User: "), input("Auth Pass: ")
                if authorize(u, p):
                    user = input("New Admin Username: ")
                    pw = input("Password: ")
                    repw = input("Re-enter: ")
                    print(sign_up_logic(user, pw, repw, "admin"))
                else:
                    print("[!] Unauthorized! Incorrect Auth details.")
            elif role_choice == '2':
                user = input("New Student Username: ")
                pw = input("Password: ")
                repw = input("Re-enter: ")
                print(sign_up_logic(user, pw, repw, "student"))
            else:
                print("Invalid choice.")
            
            input("\nPress Enter to return to main menu...")

        elif choice == '2':
            wait_and_clear(0.5)
            user_instance = login_system()
            if user_instance:
                print(f"\nWelcome, {user_instance.name}!")
                time.sleep(1)
                if isinstance(user_instance, Admin):
                    admin_menu(user_instance)
                else:
                    student_menu(user_instance)
            else:
                input("\nPress Enter to try again...")

        elif choice == '3':
            print("Shutting down system. Goodbye!")
            break

if __name__ == "__main__":
    main()
