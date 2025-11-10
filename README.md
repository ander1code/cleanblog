# 🧼 CleanBlog

> A clean, modern, and modular blog built with **Django 5.x** and **Python 3.x**, using **Generic Views** to ensure simplicity, reusability, and maintainability.

---

## 🏗️ Overview

**CleanBlog** is a web application focused on **clarity**, **modularity**, and **Django best practices**.  
It provides a complete blogging platform with:

- Custom user authentication  
- Post creation, editing, and deletion  
- Category-based organization  
- Author-based permissions  
- Friendly feedback through **Bootstrap modals**  
- Custom 404/500 error pages  
- Clean, scalable **Generic Views (CBVs)** structure with selective **Function-Based Views (FBVs)**  

---

## ⚙️ Core Technologies

| Layer | Technology | Purpose |
|--------|-------------|----------|
| **Backend** | Django 5.x | Main framework |
| **Language** | Python 3.x | Logic and business layer |
| **Database** | SQLite (default) | Data persistence |
| **Frontend** | HTML5 + Bootstrap 5 | UI and responsiveness |
| **Sessions** | Django Session Framework | Feedback and modal control |

---

## 🧩 System Architecture

The system is organized into five core layers that work together seamlessly.

---

### 1️⃣ Domain Models

At the heart of the application are three main entities:

#### 👤 Author
Represents a profile linked to a Django User.  
Includes name, email, occupation, description, and profile picture.  
Integrity is enforced through unique and length constraints.

#### 🏷️ Category
Defines content taxonomy, grouping posts by theme.  
Has a unique title and alphabetical ordering.

#### 📰 Post
The core content entity — represents each blog post.  
Contains title, summary, text, image, creation and update timestamps.  
Each post belongs to one author and one category.

🔗 **Relationships:**
User ───▶ Author ───▶ Post ◀─── Category

yaml
Copy code

Integrity constraints ensure:
- Consistent timestamps (created ≤ updated)  
- Unique author emails  
- Non-duplicated categories  

---

### 2️⃣ Validation Layer

All validation rules are centralized in a reusable validation layer.  
This ensures that **every piece of data is validated before reaching the database**.

Validations include:

- Non-empty, space-free text fields  
- Minimum and maximum length checks  
- Category existence validation  
- Required image uploads  
- Author-based edit permissions  

💡 This design keeps data **secure**, **consistent**, and **clean**, reducing redundancy and potential user errors.

---

### 3️⃣ Forms and User Input

Forms are fully styled with **Bootstrap**, using placeholders and custom validators.

- **Login Form** → handles user authentication  
- **Post Form** → handles post creation and editing  
- **Search Form** → handles keyword-based post search  

Each form integrates validation logic and user-friendly interface elements.

---

### 4️⃣ Views and Workflow

The control layer relies primarily on **Class-Based Views (CBVs)**, supported by FBVs where appropriate.  
Together, they define the full blogging workflow.

| View | Type | Protection | Purpose |
|------|------|-------------|----------|
| Post List | CBV (ListView) | Public | Lists and filters posts by title with pagination |
| Post Create | CBV (CreateView) | LoginRequired | Creates new posts linked to the logged-in author |
| Post Detail | CBV (DetailView) | Public | Displays a post’s full content |
| Post Update/Delete | CBV (UpdateView) | LoginRequired + Author Validation | Edits or deletes posts if owned by the current author |
| Login | FBV | Public | Authenticates user credentials |
| Logout | FBV | LoginRequired | Logs out and clears session |
| Clear Session Data | FBV (AJAX) | CSRF Exempt | Clears modal messages from session |
| Custom Errors | FBV | Public | Displays 404 and 500 custom pages |

🧠 **Typical user flow:**
Login → Create Post → View List → View Detail → Edit/Delete → Logout

php-template
Copy code

All actions provide real-time **feedback through Bootstrap modals** handled entirely by Django’s backend.

---

### 5️⃣ Feedback System (Bootstrap Modals)

All feedback messages are managed through the **Django Session Framework**, without complex JavaScript.

- The backend sets `open_modal = True` and `message = "Your message"` in the session.  
- The template detects those variables and displays a **Bootstrap modal** automatically.  
- After displaying, an AJAX route clears the session data.


🎯 Advantages:

Instant visual feedback

Fully backend-controlled

No external JavaScript required

🧭 Complete User Flow
text
Copy code
User visits → Post List → (Search / Detail)
                   ↓
           Logs in to the system
                   ↓
      Creates, edits, or deletes their posts
                   ↓
                Logs out
Throughout each step, Bootstrap modals display contextual feedback — success, error, or warning — creating a smooth and intuitive UX.

📘 Project Highlights
✨ CleanBlog stands out for its clarity, modularity, and maintainability, featuring:

✅ Fully Generic View–based architecture

🧠 Centralized validation system

💬 Dynamic feedback through Bootstrap modals

🔐 Strict author-based permissions

⚡ Smart search and pagination

🧩 Scalable and clean architecture

🧼 Well-structured, readable code

