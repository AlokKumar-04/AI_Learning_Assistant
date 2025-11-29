# 🎓 AI Learning Assistant

An intelligent educational content generator powered by AI that creates comprehensive learning materials for any topic. Built with Django and integrated with Hugging Face's free AI models.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-blue?style=for-the-badge)](https://Alokkumar72.pythonanywhere.com)
[![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?style=flat&logo=django)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)](LICENSE)

## 🌟 Live Demo

**Visit the app:** [https://Alokkumar72.pythonanywhere.com](https://Alokkumar72.pythonanywhere.com)

---

## 📖 Overview

AI Learning Assistant is a web application that generates comprehensive educational content using artificial intelligence. Simply enter any topic, and the app will create:

- 📚 **Detailed Explanations** - In-depth coverage with real-world applications
- 📝 **Quick Summaries** - Concise 3-sentence overviews
- 💡 **Key Concepts** - 5-7 essential concepts with descriptions
- ❓ **Practice Questions** - 5 questions with detailed answers
- 💼 **Interview Q&A** - Professional interview questions and model answers

Perfect for students, professionals, and anyone looking to learn something new!

---

## ✨ Features

### 🤖 AI-Powered Content Generation
- Utilizes Hugging Face's Qwen 2.5 72B model
- Generates unique, contextual content for any topic
- Free to use with no API costs

### 🎨 Modern User Interface
- Beautiful gradient design
- Responsive layout (mobile, tablet, desktop)
- Smooth animations and transitions
- Clean, intuitive user experience

### ⚡ Fast & Efficient
- Asynchronous content generation
- Loading indicators for better UX
- Optimized API calls
- Fallback mechanisms for reliability

### 🔒 Secure & Professional
- Environment variable management
- CSRF protection
- Production-ready deployment
- Best security practices

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Django 4.2
- **Language:** Python 3.10
- **API Integration:** Hugging Face Inference API
- **Environment Management:** python-decouple

### Frontend
- **UI Framework:** Bootstrap 5.3
- **Icons:** Font Awesome 6.4
- **Styling:** Custom CSS with gradients & animations
- **JavaScript:** Vanilla JS (async/await)

### Deployment
- **Hosting:** PythonAnywhere (Free Tier)
- **WSGI Server:** Production-ready configuration
- **Static Files:** Collected and served separately

---

## 📸 Screenshots

### Home Page
![Home Page](/Images/img1.png)

### Generated Content
![Generated Content](/Images/img3.png)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git
- Hugging Face account (free)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AlokKumar-04/AI_Learning_Assistant.git
   cd AI_Learning_Assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   HUGGINGFACE_TOKEN=your_huggingface_token_here
   ```
   
   Get your free token at: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the app**
   
   Open your browser and go to: `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
AI_Learning_Assistant/
├── AI_Learning_Assistant/       # Django project settings
│   ├── settings.py             # Configuration
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI config
├── content_gen/                # Main Django app
│   ├── views.py                # Business logic & API integration
│   ├── urls.py                 # App URL routing
│   └── templates/              # HTML templates
│       └── index.html          # Frontend interface
├── static/                     # Static files (CSS, JS, images)
├── .env                        # Environment variables (not in repo)
├── .gitignore                  # Git ignore rules
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Hugging Face API Token (Required)
HUGGINGFACE_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Django Settings (Optional - for production)
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com
```

### Django Settings

Key settings in `settings.py`:

```python
# Security
DEBUG = False  # Set to True for development
ALLOWED_HOSTS = ['yourdomain.com', 'localhost']

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

# CSRF Protection
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
```

---

## 🌐 Deployment

### Deploy to PythonAnywhere (Free)

1. **Create account** at [PythonAnywhere](https://www.pythonanywhere.com/)

2. **Clone repository**
   ```bash
   git clone https://github.com/AlokKumar-04/AI_Learning_Assistant.git
   ```

3. **Set up virtual environment**
   ```bash
   cd AI_Learning_Assistant
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure settings**
   - Update `ALLOWED_HOSTS` in `settings.py`
   - Create `.env` file with your Hugging Face token
   - Run migrations and collect static files

5. **Configure Web App**
   - Create new web app (Manual configuration)
   - Set virtualenv path
   - Configure WSGI file
   - Set static files mapping

6. **Reload and test**

Detailed deployment guide available in the repository.

---

## 📚 API Documentation

### Generate Content Endpoint

**POST** `/api/generate/`

**Request Body:**
```json
{
  "topic": "Machine Learning"
}
```

**Response:**
```json
{
  "explanation": "Detailed explanation text...",
  "summary": "Brief summary text...",
  "key_concepts": [
    {
      "concept": "Concept Name",
      "description": "Concept description"
    }
  ],
  "practice_questions": [
    {
      "question": "Question text?",
      "answer": "Answer text"
    }
  ],
  "interview_qa": [
    {
      "question": "Interview question?",
      "answer": "Professional answer"
    }
  ]
}
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Test your changes thoroughly
- Update documentation as needed

---

## 🐛 Known Issues & Limitations

- First API request may take 20-30 seconds (model loading)
- Free tier has rate limits (30,000 requests/month)
- JSON parsing may occasionally fail (fallback content provided)
- Some complex topics may require multiple attempts

---

## 🔮 Future Enhancements

- [ ] User authentication and saved topics
- [ ] Export content to PDF/Word
- [ ] Custom AI model selection
- [ ] Topic difficulty levels
- [ ] Multilingual support
- [ ] Flashcard generation
- [ ] Quiz mode with scoring
- [ ] Share functionality
- [ ] Dark mode toggle
- [ ] Mobile app version

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Alok Kumar**

- GitHub: [@AlokKumar-04](https://github.com/AlokKumar-04)
- LinkedIn: [Your LinkedIn Profile](https://www.linkedin.com/in/alok-kumar-panda-864b421a4/)

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing free AI model access
- [Django](https://www.djangoproject.com/) for the amazing web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components
- [PythonAnywhere](https://www.pythonanywhere.com/) for free hosting
- [Font Awesome](https://fontawesome.com/) for the icons

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/AlokKumar-04/AI_Learning_Assistant/issues) page
2. Create a new issue with details
3. Contact via [email](mailto:alokkumarpanda72@gmail.com)

---

## ⭐ Show Your Support

If you found this project helpful, please consider:

- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing to the codebase
- Reporting bugs or suggesting features

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/AlokKumar-04/AI_Learning_Assistant?style=social)
![GitHub forks](https://img.shields.io/github/forks/AlokKumar-04/AI_Learning_Assistant?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/AlokKumar-04/AI_Learning_Assistant?style=social)

---

<div align="center">

**Made with ❤️ by Alok Kumar**

[⬆ Back to Top](#-ai-learning-assistant)

</div>