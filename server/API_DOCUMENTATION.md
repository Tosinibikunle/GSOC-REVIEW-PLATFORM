# GSoC Review Platform - API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
The API uses Session Authentication and Basic Authentication. You can authenticate through:
- Django admin login at `/admin/`
- Browsable API login at `/api-auth/login/`

## API Endpoints Overview

### Organizations
- `GET /api/organizations/` - List all organizations
- `POST /api/organizations/` - Create a new organization
- `GET /api/organizations/{id}/` - Get organization details
- `PUT /api/organizations/{id}/` - Update organization
- `PATCH /api/organizations/{id}/` - Partial update organization
- `DELETE /api/organizations/{id}/` - Delete organization
- `GET /api/organizations/{id}/projects/` - Get all projects for organization
- `GET /api/organizations/{id}/members/` - Get all members of organization

### User Profiles
- `GET /api/profiles/` - List all user profiles
- `POST /api/profiles/` - Create a new user profile (with user account)
- `GET /api/profiles/{id}/` - Get profile details
- `PUT /api/profiles/{id}/` - Update profile
- `PATCH /api/profiles/{id}/` - Partial update profile
- `DELETE /api/profiles/{id}/` - Delete profile
- `GET /api/profiles/me/` - Get current user's profile
- `GET /api/profiles/{id}/proposals/` - Get all proposals by student
- `GET /api/profiles/{id}/reviews/` - Get all reviews by mentor

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `PATCH /api/projects/{id}/` - Partial update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/{id}/proposals/` - Get all proposals for project
- `GET /api/projects/by_year/?year=2024` - Get projects by year

### Proposals
- `GET /api/proposals/` - List proposals (filtered by user role)
- `POST /api/proposals/` - Create a new proposal
- `GET /api/proposals/{id}/` - Get proposal details
- `PUT /api/proposals/{id}/` - Update proposal
- `PATCH /api/proposals/{id}/` - Partial update proposal
- `DELETE /api/proposals/{id}/` - Delete proposal
- `POST /api/proposals/{id}/submit/` - Submit a proposal
- `GET /api/proposals/{id}/reviews/` - Get all reviews for proposal
- `GET /api/proposals/{id}/comments/` - Get all comments for proposal
- `GET /api/proposals/{id}/timeline/` - Get timeline/milestones for proposal

### Reviews
- `GET /api/reviews/` - List all reviews (filtered by user role)
- `POST /api/reviews/` - Create a new review
- `GET /api/reviews/{id}/` - Get review details
- `PUT /api/reviews/{id}/` - Update review
- `PATCH /api/reviews/{id}/` - Partial update review
- `DELETE /api/reviews/{id}/` - Delete review

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Get comment details
- `PUT /api/comments/{id}/` - Update comment
- `PATCH /api/comments/{id}/` - Partial update comment
- `DELETE /api/comments/{id}/` - Delete comment
- `GET /api/comments/{id}/replies/` - Get all replies to comment

### Project Timeline
- `GET /api/timelines/` - List all milestones
- `POST /api/timelines/` - Create a new milestone
- `GET /api/timelines/{id}/` - Get milestone details
- `PUT /api/timelines/{id}/` - Update milestone
- `PATCH /api/timelines/{id}/` - Partial update milestone
- `DELETE /api/timelines/{id}/` - Delete milestone
- `GET /api/timelines/overdue/` - Get all overdue milestones
- `POST /api/timelines/{id}/mark_complete/` - Mark milestone as complete

### Notifications
- `GET /api/notifications/` - List user's notifications
- `GET /api/notifications/{id}/` - Get notification details
- `POST /api/notifications/{id}/mark_read/` - Mark notification as read
- `POST /api/notifications/mark_all_read/` - Mark all notifications as read
- `GET /api/notifications/unread_count/` - Get count of unread notifications

## Query Parameters

### Filtering
All list endpoints support filtering:
```
GET /api/projects/?organization=1&difficulty=medium&year=2024
GET /api/proposals/?status=submitted
GET /api/reviews/?recommendation=accept
```

### Search
Most endpoints support search:
```
GET /api/organizations/?search=python
GET /api/projects/?search=machine+learning
GET /api/profiles/?search=john
```

### Ordering
```
GET /api/projects/?ordering=-created_at
GET /api/proposals/?ordering=submitted_at
GET /api/reviews/?ordering=-overall_score
```

### Pagination
```
GET /api/projects/?page=2
GET /api/proposals/?page=3&page_size=20
```

## Request/Response Examples

### 1. Create Organization
**Request:**
```http
POST /api/organizations/
Content-Type: application/json

{
  "name": "Python Software Foundation",
  "description": "The Python Software Foundation is dedicated to advancing open source technology related to Python.",
  "website": "https://www.python.org/psf/",
  "contact_email": "psf@python.org",
  "tech_stack": ["Python", "Django", "Flask"],
  "year_joined": 2024,
  "is_active": true
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Python Software Foundation",
  "description": "The Python Software Foundation is dedicated to advancing open source technology related to Python.",
  "website": "https://www.python.org/psf/",
  "logo_url": null,
  "tech_stack": ["Python", "Django", "Flask"],
  "contact_email": "psf@python.org",
  "is_active": true,
  "year_joined": 2024,
  "projects_count": 0,
  "created_at": "2024-10-24T18:00:00",
  "updated_at": "2024-10-24T18:00:00"
}
```

### 2. Create User Profile (Student)
**Request:**
```http
POST /api/profiles/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "student",
  "bio": "Computer Science student passionate about open source",
  "github_username": "johndoe",
  "university": "MIT",
  "degree": "Bachelor of Science in Computer Science",
  "graduation_year": 2025,
  "country": "USA",
  "timezone": "America/New_York"
}
```

**Response:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2024-10-24T18:00:00"
  },
  "role": "student",
  "bio": "Computer Science student passionate about open source",
  "github_username": "johndoe",
  "university": "MIT",
  "degree": "Bachelor of Science in Computer Science",
  "graduation_year": 2025,
  "organization": null,
  "organization_name": null,
  "country": "USA",
  "timezone": "America/New_York",
  "is_verified": false,
  "full_name": "John Doe",
  "created_at": "2024-10-24T18:00:00",
  "updated_at": "2024-10-24T18:00:00"
}
```

### 3. Create Project
**Request:**
```http
POST /api/projects/
Content-Type: application/json

{
  "organization_id": 1,
  "title": "Improve Django REST Framework Documentation",
  "description": "Enhance the documentation for Django REST Framework with more examples and tutorials",
  "expected_outcomes": "Comprehensive documentation with code examples, tutorials, and best practices",
  "skills_required": ["Python", "Django", "Technical Writing", "Markdown"],
  "difficulty": "medium",
  "duration_weeks": 12,
  "mentor_ids": [2, 3],
  "status": "published",
  "year": 2024,
  "max_proposals": 2
}
```

**Response:**
```json
{
  "id": 1,
  "organization": {
    "id": 1,
    "name": "Python Software Foundation",
    "description": "...",
    "projects_count": 1
  },
  "title": "Improve Django REST Framework Documentation",
  "description": "Enhance the documentation for Django REST Framework with more examples and tutorials",
  "expected_outcomes": "Comprehensive documentation with code examples, tutorials, and best practices",
  "skills_required": ["Python", "Django", "Technical Writing", "Markdown"],
  "difficulty": "medium",
  "duration_weeks": 12,
  "mentors": [...],
  "status": "published",
  "year": 2024,
  "max_proposals": 2,
  "created_at": "2024-10-24T18:00:00",
  "updated_at": "2024-10-24T18:00:00"
}
```

### 4. Create Proposal
**Request:**
```http
POST /api/proposals/
Content-Type: application/json

{
  "project_id": 1,
  "title": "Enhanced DRF Documentation with Interactive Examples",
  "abstract": "This proposal aims to improve Django REST Framework documentation by adding interactive code examples and comprehensive tutorials.",
  "detailed_description": "Detailed description of the approach...",
  "implementation_plan": "Week 1-2: Research existing documentation...",
  "timeline": "12 weeks breakdown with milestones...",
  "deliverables": "Updated documentation, code examples, tutorials",
  "prior_experience": "Contributed to Django documentation, technical writer for 2 years",
  "why_this_project": "Passionate about documentation and helping developers",
  "availability": "40 hours per week, no major commitments"
}
```

**Response:**
```json
{
  "id": 1,
  "project": {...},
  "student": {...},
  "title": "Enhanced DRF Documentation with Interactive Examples",
  "abstract": "This proposal aims to improve Django REST Framework documentation...",
  "status": "draft",
  "submitted_at": null,
  "created_at": "2024-10-24T18:00:00",
  "updated_at": "2024-10-24T18:00:00"
}
```

### 5. Submit Proposal
**Request:**
```http
POST /api/proposals/1/submit/
```

**Response:**
```json
{
  "id": 1,
  "status": "submitted",
  "submitted_at": "2024-10-24T18:30:00",
  ...
}
```

### 6. Create Review
**Request:**
```http
POST /api/reviews/
Content-Type: application/json

{
  "proposal": 1,
  "technical_feasibility": 5,
  "understanding_of_project": 4,
  "implementation_quality": 5,
  "timeline_realism": 4,
  "student_capability": 5,
  "recommendation": "accept",
  "strengths": "Excellent understanding of the project, strong technical background, clear implementation plan",
  "weaknesses": "Timeline could be more detailed for the later phases",
  "suggestions": "Consider adding more specific milestones for weeks 8-12",
  "private_notes": "Strong candidate, recommend acceptance",
  "is_final": true
}
```

**Response:**
```json
{
  "id": 1,
  "proposal": 1,
  "proposal_title": "Enhanced DRF Documentation with Interactive Examples",
  "reviewer": {...},
  "technical_feasibility": 5,
  "understanding_of_project": 4,
  "implementation_quality": 5,
  "timeline_realism": 4,
  "student_capability": 5,
  "overall_score": 4.6,
  "recommendation": "accept",
  "strengths": "Excellent understanding of the project...",
  "weaknesses": "Timeline could be more detailed...",
  "suggestions": "Consider adding more specific milestones...",
  "private_notes": "Strong candidate, recommend acceptance",
  "is_final": true,
  "created_at": "2024-10-24T19:00:00",
  "updated_at": "2024-10-24T19:00:00"
}
```

### 7. Add Comment
**Request:**
```http
POST /api/comments/
Content-Type: application/json

{
  "proposal": 1,
  "content": "Great proposal! I have a few questions about the implementation timeline.",
  "is_internal": false,
  "parent": null
}
```

**Response:**
```json
{
  "id": 1,
  "proposal": 1,
  "author": {...},
  "author_name": "Jane Smith",
  "parent": null,
  "content": "Great proposal! I have a few questions about the implementation timeline.",
  "is_internal": false,
  "is_edited": false,
  "replies_count": 0,
  "created_at": "2024-10-24T19:15:00",
  "updated_at": "2024-10-24T19:15:00"
}
```

### 8. Create Milestone
**Request:**
```http
POST /api/timelines/
Content-Type: application/json

{
  "proposal": 1,
  "title": "Complete documentation structure",
  "description": "Create the overall structure for the new documentation",
  "expected_completion_date": "2024-06-15",
  "status": "pending",
  "progress_percentage": 0,
  "deliverables": "Documentation outline, table of contents, section templates",
  "order": 1
}
```

**Response:**
```json
{
  "id": 1,
  "proposal": 1,
  "title": "Complete documentation structure",
  "description": "Create the overall structure for the new documentation",
  "expected_completion_date": "2024-06-15",
  "actual_completion_date": null,
  "status": "pending",
  "progress_percentage": 0,
  "deliverables": "Documentation outline, table of contents, section templates",
  "notes": "",
  "pull_request_url": null,
  "documentation_url": null,
  "order": 1,
  "is_overdue": false,
  "created_at": "2024-10-24T19:30:00",
  "updated_at": "2024-10-24T19:30:00"
}
```

## Data Models

### Organization
```json
{
  "id": integer,
  "name": string (unique),
  "description": text,
  "website": url (optional),
  "logo_url": url (optional),
  "tech_stack": array of strings,
  "contact_email": email,
  "is_active": boolean,
  "year_joined": integer,
  "projects_count": integer (read-only),
  "created_at": datetime,
  "updated_at": datetime
}
```

### UserProfile
```json
{
  "id": integer,
  "user": {
    "id": integer,
    "username": string,
    "email": email,
    "first_name": string,
    "last_name": string,
    "date_joined": datetime
  },
  "role": "student" | "mentor" | "admin" | "org_admin",
  "bio": text,
  "avatar_url": url (optional),
  "github_username": string,
  "linkedin_url": url (optional),
  "portfolio_url": url (optional),
  "university": string (for students),
  "degree": string (for students),
  "graduation_year": integer (for students),
  "organization": integer (for mentors/org_admins),
  "expertise": array of strings (for mentors),
  "phone_number": string,
  "country": string,
  "timezone": string,
  "is_verified": boolean,
  "full_name": string (read-only),
  "created_at": datetime,
  "updated_at": datetime
}
```

### Project
```json
{
  "id": integer,
  "organization": integer,
  "title": string,
  "description": text,
  "expected_outcomes": text,
  "skills_required": array of strings,
  "difficulty": "easy" | "medium" | "hard",
  "duration_weeks": integer,
  "mentors": array of integers,
  "status": "draft" | "published" | "archived",
  "year": integer,
  "max_proposals": integer,
  "created_at": datetime,
  "updated_at": datetime
}
```

### Proposal
```json
{
  "id": integer,
  "project": integer,
  "student": integer,
  "title": string,
  "abstract": text,
  "detailed_description": text,
  "implementation_plan": text,
  "timeline": text,
  "deliverables": text,
  "prior_experience": text,
  "why_this_project": text,
  "availability": text,
  "status": "draft" | "submitted" | "under_review" | "accepted" | "rejected" | "withdrawn",
  "submitted_at": datetime (nullable),
  "reviewed_at": datetime (nullable),
  "proposal_document_url": url (optional),
  "github_repo_url": url (optional),
  "created_at": datetime,
  "updated_at": datetime
}
```

### Review
```json
{
  "id": integer,
  "proposal": integer,
  "reviewer": integer,
  "technical_feasibility": integer (1-5),
  "understanding_of_project": integer (1-5),
  "implementation_quality": integer (1-5),
  "timeline_realism": integer (1-5),
  "student_capability": integer (1-5),
  "overall_score": float (calculated, read-only),
  "recommendation": "strongly_accept" | "accept" | "neutral" | "reject" | "strongly_reject",
  "strengths": text,
  "weaknesses": text,
  "suggestions": text,
  "private_notes": text,
  "is_final": boolean,
  "created_at": datetime,
  "updated_at": datetime
}
```

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Testing the API

### Using cURL
```bash
# Get all organizations
curl http://localhost:8000/api/organizations/

# Create organization (with authentication)
curl -X POST http://localhost:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{"name": "Test Org", "description": "Test", "contact_email": "test@example.com", "year_joined": 2024}'

# Get current user profile
curl http://localhost:8000/api/profiles/me/ \
  -u username:password
```

### Using Python requests
```python
import requests

# Base URL
base_url = "http://localhost:8000/api"

# Login
session = requests.Session()
session.auth = ('username', 'password')

# Get organizations
response = session.get(f"{base_url}/organizations/")
organizations = response.json()

# Create proposal
proposal_data = {
    "project_id": 1,
    "title": "My Proposal",
    "abstract": "Abstract text",
    # ... other fields
}
response = session.post(f"{base_url}/proposals/", json=proposal_data)
proposal = response.json()
```

### Using the Browsable API
Navigate to `http://localhost:8000/api/` in your browser to use the interactive browsable API interface provided by Django REST Framework.

## Notes

1. **Authentication Required**: Most endpoints require authentication. Students can only see/edit their own proposals, mentors can see proposals for their projects.

2. **Permissions**: Different user roles have different permissions:
   - **Students**: Can create and edit their own proposals
   - **Mentors**: Can review proposals for their projects, add comments
   - **Org Admins**: Can manage their organization's projects and mentors
   - **Admins**: Full access to all resources

3. **Pagination**: All list endpoints are paginated with 20 items per page by default.

4. **Filtering**: Use query parameters to filter results (see Query Parameters section).

5. **Browsable API**: The API includes a browsable interface at `/api/` for easy testing and exploration.

