# SkillSwap 🎓🤝

SkillSwap is a Django-based web platform where users can offer and request skills.  
It enables people to connect, learn from each other, and share knowledge through skill swaps.

---

## 🚀 Features

- ✅ User Signup, Login & Logout  
- ✅ User Profiles (including skills offered & requested)  
- ✅ Post a Skill (Offer or Request)  
- ✅ Browse & Search Skills by Type or Category  
- ✅ Contact Users via Basic Messaging  
- ✅ Leave Reviews & Star Ratings after a Skill Session  

---

## 🎯 Project Scope

This project focuses on Django fundamentals:
- Models
- Views
- Templates
- Forms
- User Authentication (leveraging Django’s built-in tools)

---

## 🏗️ Tech Stack

- **Backend:** Django (Python)  
- **Database:** SQLite (default, for simplicity)  
- **Frontend:** Django Templates + Basic CSS (optional Bootstrap)  
- **Tools Used:**  
  - GitHub (version control)  
  - Trello (task tracking)  
  - Figma / Paper Sketch (mockups)

---

## 📋 Setup Instructions (Local Development)

1. Clone the repository:
   ```bash
   git clone https://github.com/d3noDL/dj_skillswap.git
   cd dj_skillswap

2. Create a new conda environment:
   ```bash
  conda create --name skillswap python=3.12
  conda activate skillswap

3. Install dependencies:
   ```bash
  pip install -r requirements.txt

4. Apply database migrations:
   ```bash
  python manage.py migrate

5. Create a superuser (admin account):
   ```bash
  python manage.py createsuperuser

6. Run the development server:
   ```bash
  python manage.py runserver

7. Access the local site at:
  http://127.0.0.1:8000/
  
---

## 🧑‍🤝‍🧑 Team & Credits

Built collaboratively over an 8-day sprint using Scrum methodology by:
- Denise Muniz
- Dino Cuturdic
- Miliyard Tassew Reda
- Preethiallala
- Sonja Rojin Yilmaz
  
---

## 📅 Project Timeline

| Day | Focus                                  |
| --- | -------------------------------------- |
| 1   | Planning, GitHub/Trello setup, Mockups |
| 2   | Django Setup & User Authentication     |
| 3   | Home Page & Navigation                 |
| 4   | User Profiles                          |
| 5   | Skill Listings (Offer & Request)       |
| 6   | Browse & Search Skills                 |
| 7   | Messaging & Reviews                    |
| 8   | Demo Day                               |

 
---

## ✅ Status

✅ In Development

---

## 📄 License

This project is licensed under the MIT License.