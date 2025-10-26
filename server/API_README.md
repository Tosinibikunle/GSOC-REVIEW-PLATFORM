# GSoC Review Platform - REST API

## Overview

A comprehensive REST API for managing Google Summer of Code (GSoC) proposals, reviews, and project tracking. Built with Django and Django REST Framework.

## Features

✅ **Complete CRUD Operations** for all entities
✅ **Role-based Access Control** (Students, Mentors, Org Admins, Admins)
✅ **Advanced Filtering & Search** on all endpoints
✅ **Pagination** for efficient data loading
✅ **Nested Relationships** with proper serialization
✅ **Custom Actions** (submit proposals, mark milestones complete, etc.)
✅ **Browsable API** for easy testing and exploration
✅ **CORS Support** for frontend integration

## Database Models

### Core Entities

1. **Organization** - GSoC participating organizations
2. **UserProfile** - Extended user profiles with role-based fields
3. **Project** - Project ideas from organizations
4. **Proposal** - Student proposals for projects
5. **Review** - Mentor reviews with scoring system
6. **Comment** - Discussion threads on proposals
7. **ProjectTimeline** - Milestones and progress tracking
8. **Notification** - User notifications system

### Relationships

```
Organization (1) ──→ (N) Project
Organization (1) ──→ (N) UserProfile (mentors/org_admins)
Project (1) ──→ (N) Proposal
Project (N) ←──→ (N) UserProfile (mentors)
UserProfile (1) ──→ (N) Proposal (students)
Proposal (1) ──→ (N) Review
Proposal (1) ──→ (N) Comment
Proposal (1) ──→ (N) ProjectTimeline
UserProfile (1) ──→ (N) Notification
```

## API Endpoints Summary

| Resource | Endpoints | Custom Actions |
|----------|-----------|----------------|
| Organizations | 6 standard CRUD | `/projects/`, `/members/` |
| User Profiles | 6 standard CRUD | `/me/`, `/proposals/`, `/reviews/` |
| Projects | 6 standard CRUD | `/proposals/`, `/by_year/` |
| Proposals | 6 standard CRUD | `/submit/`, `/reviews/`, `/comments/`, `/timeline/` |
| Reviews | 5 standard CRUD | - |
| Comments | 6 standard CRUD | `/replies/` |
| Timelines | 6 standard CRUD | `/overdue/`, `/mark_complete/` |
| Notifications | 4 standard CRUD | `/mark_read/`, `/mark_all_read/`, `/unread_count/` |

**Total: 50+ API endpoints**

## Quick Start

### 1. Start the Server
```bash
cd server
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

### 2. Create a Superuser
```bash
python manage.py createsuperuser
```

### 3. Access the Admin Panel
Visit `http://localhost:8000/admin/` and login with your superuser credentials.

### 4. Explore the Browsable API
Visit `http://localhost:8000/api/` to use the interactive API browser.

### 5. Test the API
```bash
python test_api.py
```

## Usage Examples

### Creating a Complete Workflow

#### 1. Create an Organization
```bash
curl -X POST http://localhost:8000/api/organizations/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{
    "name": "Python Software Foundation",
    "description": "PSF manages Python development",
    "contact_email": "psf@python.org",
    "tech_stack": ["Python", "Django"],
    "year_joined": 2024,
    "is_active": true
  }'
```

#### 2. Create a Mentor Profile
```bash
curl -X POST http://localhost:8000/api/profiles/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mentor1",
    "email": "mentor@example.com",
    "password": "securepass123",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "mentor",
    "organization": 1,
    "expertise": ["Python", "Django", "REST APIs"]
  }'
```

#### 3. Create a Project
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{
    "organization_id": 1,
    "title": "Improve Django REST Framework",
    "description": "Enhance DRF with new features",
    "expected_outcomes": "Better API development experience",
    "skills_required": ["Python", "Django", "REST"],
    "difficulty": "medium",
    "duration_weeks": 12,
    "mentor_ids": [1],
    "status": "published",
    "year": 2024
  }'
```

#### 4. Create a Student Profile
```bash
curl -X POST http://localhost:8000/api/profiles/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "student",
    "university": "MIT",
    "degree": "BS Computer Science",
    "graduation_year": 2025
  }'
```

#### 5. Create and Submit a Proposal
```bash
# Create proposal
curl -X POST http://localhost:8000/api/proposals/ \
  -H "Content-Type: application/json" \
  -u student1:securepass123 \
  -d '{
    "project_id": 1,
    "title": "My Proposal for DRF Improvements",
    "abstract": "I propose to enhance DRF...",
    "detailed_description": "Detailed plan...",
    "implementation_plan": "Week by week plan...",
    "timeline": "12 weeks timeline...",
    "deliverables": "Code, docs, tests",
    "availability": "40 hours/week"
  }'

# Submit the proposal
curl -X POST http://localhost:8000/api/proposals/1/submit/ \
  -u student1:securepass123
```

#### 6. Create a Review
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -u mentor1:securepass123 \
  -d '{
    "proposal": 1,
    "technical_feasibility": 5,
    "understanding_of_project": 4,
    "implementation_quality": 5,
    "timeline_realism": 4,
    "student_capability": 5,
    "recommendation": "accept",
    "strengths": "Strong technical skills",
    "weaknesses": "Timeline needs more detail",
    "suggestions": "Add more milestones",
    "is_final": true
  }'
```

## Advanced Features

### Filtering
```bash
# Get projects by organization and difficulty
GET /api/projects/?organization=1&difficulty=medium

# Get submitted proposals
GET /api/proposals/?status=submitted

# Get reviews with high scores
GET /api/reviews/?overall_score__gte=4.0
```

### Search
```bash
# Search organizations by name
GET /api/organizations/?search=python

# Search projects by title or description
GET /api/projects/?search=machine+learning
```

### Ordering
```bash
# Get newest proposals first
GET /api/proposals/?ordering=-created_at

# Get reviews by score (highest first)
GET /api/reviews/?ordering=-overall_score
```

### Pagination
```bash
# Get page 2 with 10 items per page
GET /api/projects/?page=2&page_size=10
```

### Nested Resources
```bash
# Get all projects for an organization
GET /api/organizations/1/projects/

# Get all proposals for a project
GET /api/projects/1/proposals/

# Get all reviews for a proposal
GET /api/proposals/1/reviews/

# Get current user's profile
GET /api/profiles/me/
```

## Role-Based Access Control

### Student Role
- ✅ Create and edit own proposals
- ✅ View own proposals and reviews
- ✅ Comment on own proposals
- ❌ Cannot review proposals
- ❌ Cannot see other students' proposals

### Mentor Role
- ✅ View proposals for their projects
- ✅ Create reviews for proposals
- ✅ Add comments (including internal)
- ✅ Manage project timelines
- ❌ Cannot edit other mentors' reviews

### Organization Admin Role
- ✅ All mentor permissions
- ✅ Manage organization projects
- ✅ Add/remove mentors
- ✅ View all proposals for organization

### Admin Role
- ✅ Full access to all resources
- ✅ Manage all organizations
- ✅ Manage all users
- ✅ Override any permissions

## Data Validation

### Proposal Validation
- Title, abstract, and description are required
- Can only submit proposals in "draft" status
- Students can only create proposals for published projects

### Review Validation
- All rating fields must be between 1-5
- Overall score is automatically calculated
- One review per reviewer per proposal (unique constraint)
- Only mentors can create reviews

### Timeline Validation
- Only for accepted proposals
- Expected completion date required
- Progress percentage must be 0-100

## Performance Optimizations

1. **Select Related**: Reduces database queries for foreign keys
2. **Prefetch Related**: Optimizes many-to-many relationships
3. **Pagination**: Limits data transfer
4. **Filtering at Database Level**: Efficient queries
5. **Read-Only Fields**: Prevents unnecessary updates

## Security Features

1. **Authentication Required**: Most endpoints require authentication
2. **Role-Based Permissions**: Users can only access authorized data
3. **CSRF Protection**: Enabled for state-changing operations
4. **CORS Configuration**: Controlled cross-origin access
5. **Password Hashing**: Secure password storage

## Testing

### Manual Testing
1. Use the browsable API at `/api/`
2. Use the admin panel at `/admin/`
3. Run the test script: `python test_api.py`

### Automated Testing
```bash
python manage.py test gsoc_review
```

## Documentation

- **API Documentation**: See `API_DOCUMENTATION.md` for detailed endpoint documentation
- **Setup Guide**: See `SETUP.md` for installation instructions
- **Browsable API**: Visit `/api/` for interactive documentation

## Common Issues & Solutions

### Issue: "Authentication credentials were not provided"
**Solution**: Login through `/api-auth/login/` or provide credentials in requests

### Issue: "You do not have permission to perform this action"
**Solution**: Check user role and permissions for the endpoint

### Issue: "This field is required"
**Solution**: Check API documentation for required fields

### Issue: Pagination not working
**Solution**: Use `?page=1` parameter, default page size is 20

## Next Steps

1. ✅ API is fully functional
2. 📝 Create sample data using admin panel
3. 🧪 Test all endpoints with different user roles
4. 🎨 Build a frontend application
5. 🚀 Deploy to production

## Support

For detailed API documentation, see `API_DOCUMENTATION.md`
For setup instructions, see `SETUP.md`
For model details, see `gsoc_review/models.py`

