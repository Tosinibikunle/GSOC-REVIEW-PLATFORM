# GSoC Review Platform - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Start the Server
```bash
cd server
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Create a Superuser
Open a new terminal and run:
```bash
cd server
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email: admin@example.com
Password: ********
Password (again): ********
```

### Step 3: Access the Admin Panel
1. Open your browser and go to: `http://localhost:8000/admin/`
2. Login with your superuser credentials
3. You'll see all the models available for management

### Step 4: Explore the Browsable API
1. Go to: `http://localhost:8000/api/`
2. You'll see the API root with all available endpoints
3. Click on any endpoint to explore (e.g., `/api/organizations/`)
4. Login using the "Log in" button in the top right

### Step 5: Create Sample Data

#### Create an Organization
1. Go to `http://localhost:8000/api/organizations/`
2. Scroll to the bottom to the HTML form
3. Fill in:
   - Name: "Python Software Foundation"
   - Description: "The PSF manages Python development"
   - Contact Email: "psf@python.org"
   - Tech Stack: `["Python", "Django", "Flask"]`
   - Year Joined: 2024
   - Is Active: ✓
4. Click "POST"

#### Create a Mentor Profile
1. Go to `http://localhost:8000/api/profiles/`
2. Fill in:
   - Username: "mentor1"
   - Email: "mentor@example.com"
   - Password: "securepass123"
   - First Name: "Jane"
   - Last Name: "Smith"
   - Role: "mentor"
   - Organization: 1 (select from dropdown)
   - Expertise: `["Python", "Django", "REST APIs"]`
3. Click "POST"

#### Create a Project
1. Go to `http://localhost:8000/api/projects/`
2. Fill in:
   - Organization ID: 1
   - Title: "Improve Django REST Framework Documentation"
   - Description: "Enhance DRF docs with examples"
   - Expected Outcomes: "Better documentation"
   - Skills Required: `["Python", "Django", "Technical Writing"]`
   - Difficulty: "medium"
   - Duration Weeks: 12
   - Mentor IDs: `[1]` (or select from dropdown)
   - Status: "published"
   - Year: 2024
   - Max Proposals: 2
3. Click "POST"

#### Create a Student Profile
1. Go to `http://localhost:8000/api/profiles/`
2. Fill in:
   - Username: "student1"
   - Email: "student@example.com"
   - Password: "securepass123"
   - First Name: "John"
   - Last Name: "Doe"
   - Role: "student"
   - University: "MIT"
   - Degree: "BS Computer Science"
   - Graduation Year: 2025
3. Click "POST"

#### Create a Proposal (as student)
1. Logout from admin account
2. Login as student1 (use the login form at top right)
3. Go to `http://localhost:8000/api/proposals/`
4. Fill in:
   - Project ID: 1
   - Title: "My Proposal for DRF Documentation"
   - Abstract: "I propose to improve the DRF documentation..."
   - Detailed Description: "I will add comprehensive examples..."
   - Implementation Plan: "Week 1-2: Research..."
   - Timeline: "12 weeks with milestones..."
   - Deliverables: "Updated docs, examples, tutorials"
   - Availability: "40 hours per week"
5. Click "POST"

#### Submit the Proposal
1. Go to `http://localhost:8000/api/proposals/1/`
2. Scroll down to find the "Submit" button
3. Click "POST" on the submit action
4. The status will change from "draft" to "submitted"

#### Create a Review (as mentor)
1. Logout and login as mentor1
2. Go to `http://localhost:8000/api/reviews/`
3. Fill in:
   - Proposal: 1
   - Technical Feasibility: 5
   - Understanding of Project: 4
   - Implementation Quality: 5
   - Timeline Realism: 4
   - Student Capability: 5
   - Recommendation: "accept"
   - Strengths: "Strong technical background"
   - Weaknesses: "Timeline needs more detail"
   - Suggestions: "Add more specific milestones"
   - Is Final: ✓
4. Click "POST"
5. Notice the Overall Score is automatically calculated (4.6)

## 📚 What You Can Do Now

### As a Student
- ✅ Create proposals for published projects
- ✅ Edit your draft proposals
- ✅ Submit proposals for review
- ✅ View reviews on your proposals
- ✅ Comment on your proposals
- ✅ Track your proposal status

### As a Mentor
- ✅ View proposals for your projects
- ✅ Create detailed reviews with scoring
- ✅ Add comments (public and internal)
- ✅ Track student progress
- ✅ Manage project timelines

### As an Organization Admin
- ✅ Create and manage projects
- ✅ Add mentors to projects
- ✅ View all proposals for your organization
- ✅ Review and approve proposals

### As an Admin
- ✅ Full access to all features
- ✅ Manage all organizations
- ✅ Manage all users
- ✅ View all proposals and reviews

## 🔍 Exploring the API

### Using the Browsable API
The browsable API at `http://localhost:8000/api/` provides:
- Interactive forms for POST/PUT/PATCH requests
- Formatted JSON responses
- Filtering and search options
- Pagination controls
- Authentication status

### Using cURL
```bash
# Get all organizations
curl http://localhost:8000/api/organizations/

# Get a specific project
curl http://localhost:8000/api/projects/1/

# Create an organization (with auth)
curl -X POST http://localhost:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{"name": "Test Org", "description": "Test", "contact_email": "test@example.com", "year_joined": 2024}'
```

### Using Python
```python
import requests

# Setup
base_url = "http://localhost:8000/api"
session = requests.Session()
session.auth = ('admin', 'password')

# Get organizations
response = session.get(f"{base_url}/organizations/")
orgs = response.json()
print(orgs)

# Create a project
project_data = {
    "organization_id": 1,
    "title": "New Project",
    "description": "Description",
    "expected_outcomes": "Outcomes",
    "skills_required": ["Python"],
    "difficulty": "easy",
    "duration_weeks": 12,
    "mentor_ids": [1],
    "status": "published",
    "year": 2024
}
response = session.post(f"{base_url}/projects/", json=project_data)
project = response.json()
print(project)
```

### Using JavaScript (Fetch API)
```javascript
// Get organizations
fetch('http://localhost:8000/api/organizations/')
  .then(response => response.json())
  .then(data => console.log(data));

// Create a proposal (with auth)
fetch('http://localhost:8000/api/proposals/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Basic ' + btoa('student1:password')
  },
  body: JSON.stringify({
    project_id: 1,
    title: 'My Proposal',
    abstract: 'Abstract text',
    // ... other fields
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🎯 Common Tasks

### Filter Proposals by Status
```
GET /api/proposals/?status=submitted
```

### Search Projects
```
GET /api/projects/?search=django
```

### Get Projects by Year
```
GET /api/projects/by_year/?year=2024
```

### Get Current User Profile
```
GET /api/profiles/me/
```

### Get Unread Notifications
```
GET /api/notifications/?is_read=false
```

### Mark All Notifications as Read
```
POST /api/notifications/mark_all_read/
```

## 📖 Documentation

- **API_DOCUMENTATION.md** - Complete API reference with all endpoints
- **API_README.md** - Detailed features and usage guide
- **API_SETUP_SUMMARY.md** - What was built and how it works
- **SETUP.md** - Installation and setup instructions

## 🐛 Troubleshooting

### Can't login to browsable API
- Make sure you created a superuser
- Use the "Log in" link at the top right
- Enter your username and password

### Getting 403 Forbidden errors
- You need to be logged in
- Check if your user role has permission for that action
- Students can only edit their own proposals

### Can't see any proposals
- Make sure you're logged in
- Students only see their own proposals
- Mentors only see proposals for their projects
- Create some sample data first

### API returns empty results
- Check if you have any data in the database
- Use the admin panel to create sample data
- Check your filters - you might be filtering out all results

## 🎉 You're Ready!

You now have a fully functional GSoC Review Platform API. Start building your frontend or mobile app!

For more details, check out the other documentation files in this directory.

