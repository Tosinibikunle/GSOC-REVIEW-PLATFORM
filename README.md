<div align="center">

# GSoC Review Platform

**A comprehensive platform for Google Summer of Code proposal review and collaboration**

[![GitHub Issues](https://img.shields.io/github/issues/nst-sdc/GSOC-REVIEW-PLATFORM)](https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/nst-sdc/GSOC-REVIEW-PLATFORM)](https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM/pulls)
[![License](https://img.shields.io/github/license/nst-sdc/GSOC-REVIEW-PLATFORM)](LICENSE)

[Features](#features) • [Tech Stack](#tech-stack) • [Getting Started](#getting-started) • [Contributing](#contributing) • [License](#license)

</div>

---

## About

The **GSoC Review Platform** streamlines the Google Summer of Code proposal review process by providing an intuitive, collaborative environment for students, mentors, and organizations. 

This platform enhances transparency, facilitates structured feedback, and provides valuable analytics to improve the quality of GSoC applications and project outcomes.

---

## Features

### Authentication & Security
- **Role-based access control** for Students, Mentors, and Admins
- **Secure JWT authentication** with optional GitHub OAuth integration
- Protected routes and data encryption

### Proposal Management
- **Rich proposal submission** supporting Markdown and PDF formats
- Version history tracking for proposal revisions
- Tagging and categorization for easy discovery

### Review & Collaboration
- **Structured review system** with ratings and detailed feedback
- **Discussion threads** for collaborative reviews on each proposal
- Inline commenting and suggestion features
- Real-time notifications for updates and deadlines

### Analytics & Insights
- **Interactive dashboard** with visual metrics and progress tracking
- Performance analytics for students and mentors
- Proposal quality scores and trends
- Export functionality for comprehensive reports

### GitHub Integration
- Automatic fetching of student commits and contributions
- Repository activity tracking
- Direct links to student projects

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React.js with modern hooks and context API |
| **Backend** | Django REST Framework for robust API endpoints |
| **Database** | MongoDB for flexible document storage |
| **Authentication** | JWT tokens + GitHub OAuth |
| **Deployment** | Vercel / Render / Railway |
| **Version Control** | Git & GitHub |

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm ([Download](https://nodejs.org/))
- **MongoDB** ([Installation Guide](https://docs.mongodb.com/manual/installation/))
- **Git** ([Download](https://git-scm.com/downloads))

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM.git
cd GSOC-REVIEW-PLATFORM
```

#### 2. Backend Setup (Django + MongoDB)

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your MongoDB connection string and other settings

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

#### 3. Frontend Setup (React)

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env with your API endpoint (default: http://localhost:8000)

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

### Configuration

Create a `.env` file in both `backend/` and `frontend/` directories:

**Backend `.env`:**
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/gsoc_platform
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

**Frontend `.env`:**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GITHUB_OAUTH_ENABLED=true
```

---

## Documentation

- **[API Documentation](docs/API.md)** - Complete API endpoint reference
- **[User Guide](docs/USER_GUIDE.md)** - How to use the platform
- **[Developer Guide](docs/DEVELOPER.md)** - Architecture and development guidelines

---

## Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting pull requests.

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

Please ensure your PR:
- ✅ Comes from a feature branch (not `main`)
- ✅ Follows our coding standards
- ✅ Includes tests for new features
- ✅ Updates documentation as needed

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Team

**NST Software Development Club (NST-SDC)**

- Maintainer: [@nst-sdc](https://github.com/nst-sdc)
- Contributors: [View all contributors](https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM/graphs/contributors)

---

## Acknowledgments

- Google Summer of Code program for inspiration
- All contributors who help improve this platform
- Open source community for amazing tools and libraries

---

## Support

- **Issues:** [GitHub Issues](https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM/issues)
- **Discussions:** [GitHub Discussions](https://github.com/nst-sdc/GSOC-REVIEW-PLATFORM/discussions)
- **Email:** [Contact us](mailto:support@nst-sdc.org)

---

<div align="center">

**[Back to Top](#gsoc-review-platform)**

Made with ❤️ by NST-SDC

</div>





