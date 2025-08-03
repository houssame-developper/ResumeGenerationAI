# ResumeGenerationAI

🇺🇸 **AI-Powered Resume Generator using FastAPI, LangChain, GPT-4o, and Vanilla TypeScript**  
🇲🇦 **مولد السيرة الذاتية بالذكاء الاصطناعي باستخدام FastAPI و LangChain و GPT-4o**

---

## 🔍 Description | الوصف

**EN:**  
ResumeGenerationAI is a web application that generates professional resumes using AI. The backend is built with **FastAPI**, **LangChain**, **SQLModel**, and **GPT-4o** from OpenAI. The frontend is developed using **Vanilla TypeScript** and styled with **Tailwind CSS CDN**.  

**AR:**  
ResumeGenerationAI هو تطبيق ويب يقوم بإنشاء سيرة ذاتية احترافية باستخدام الذكاء الاصطناعي. يعتمد في الخلفية على **FastAPI** و **LangChain** و **SQLModel**، ويستخدم نموذج GPT-4o من OpenAI. أما الواجهة الأمامية فهي مبنية بـ **TypeScript بدون إطار عمل** مع استخدام **Tailwind CSS عبر CDN**.

---

## ⚙️ Technologies Used | التقنيات المستخدمة

### 🖥️ Frontend:
- Vanilla TypeScript
- Tailwind CSS (CDN)

### 🔙 Backend:
- FastAPI
- LangChain
- OpenAI GPT-4o
- SQLModel
- OS (لإدارة الملفات)

---

## 🚀 Features | الميزات

- Generate resumes in seconds using GPT-4o  
- Supports dynamic AI chaining via LangChain  
- Simple and clean frontend using TypeScript and Tailwind  
- Stores user data using SQLModel  
- File management with `os` module  

---

## 📦 Installation | التثبيت

### Backend:
```bash
pip install -r requirements.txt
uvicorn app:app --reload
