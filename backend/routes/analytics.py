from db import db
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_helpers import get_current_user
from services.analytic_service import get_analytics, AnalyticServiceError
import logging
from app.extensions import limiter

log = logging.getLogger(__name__)
analytic_bp = Blueprint('analytic', __name__)

@analytic_bp.route('/<uuid:workspace_id>/analytics')
@jwt_required()
@limiter.limit('60 per hour')
def get_analytics_route(workspace_id):
  user = get_current_user()
 
  try: 
    analytics = get_analytics(user, workspace_id)
  except AnalyticServiceError as e:
    return jsonify({'error': str(e)}), e.status_code
  except Exception as e:
    log.error(f"Error fetching analytics: {e}")
    return jsonify({'error': 'An error occured while fetching analytics'}), 500

  return jsonify(analytics), 200
  


'''
Updated todo list

I’ll map the analytics UI you already have to the backend data available, then give you a concrete checklist of dashboard metrics, required queries, and frontend chart sections. I’ll keep this as design guidance unless you ask me to implement it.

Read , lines 1 to 40

Read 

Read 

Read 

You already have the right base models:

```text
Task          → counts, statuses, priorities, completion dates
TaskActivity  → history and user actions
TimeBlock     → focus time and duration
Project       → project comparisons
Comment       → collaboration activity
```

Your current `Analytics.tsx` uses hardcoded `weeklyTasks`, so the next step is an analytics API.

## Dashboard summary cards

Return:

```json
{
  "summary": {
    "tasks_completed": 28,
    "tasks_created": 34,
    "tasks_in_progress": 5,
    "tasks_overdue": 3,
    "completion_rate": 82.35,
    "focus_minutes": 1125,
    "active_projects": 4
  }
}
```

Metrics:

- Tasks completed: `TaskActivity.activity_type == completed`
- Tasks created: `TaskActivity.activity_type == created`
- In progress: `Task.status == in_progress`
- Overdue: tasks with a due date before today
- Completion rate: completed tasks / created tasks × 100
- Focus time: sum of `TimeBlock.computed_duration`
- Active projects: projects containing non-archived tasks

Your `Task` model currently has no `due_date`, so overdue tasks cannot be calculated yet. Add one if you want that metric:

```python
due_date: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True),
    nullable=True,
)
```

## Charts to build

### 1. Completion trend

Line chart:

```json
[
  { "date": "2026-09-07", "completed": 4 },
  { "date": "2026-09-08", "completed": 7 },
  { "date": "2026-09-09", "completed": 5 }
]
```

Uses:

```text
TaskActivity
activity_type = completed
group by created_at date
```

This replaces your current `weeklyTasks`.

### 2. Tasks by project

Bar chart:

```json
[
  { "project": "Website", "total": 12, "completed": 8 },
  { "project": "Mobile App", "total": 9, "completed": 4 }
]
```

Uses:

```text
Project → Task
```

### 3. Tasks by status

Use a donut or bar chart:

```json
[
  { "status": "todo", "count": 12 },
  { "status": "in_progress", "count": 5 },
  { "status": "done", "count": 28 },
  { "status": "archived", "count": 3 }
]
```

Uses:

```text
Task.status
```

### 4. Tasks by priority

```json
[
  { "priority": "low", "count": 8 },
  { "priority": "medium", "count": 18 },
  { "priority": "high", "count": 9 },
  { "priority": "urgent", "count": 2 }
]
```

Uses:

```text
Task.priority
```

### 5. Focus time trend

Bar or line chart:

```json
[
  { "date": "2026-09-07", "minutes": 120 },
  { "date": "2026-09-08", "minutes": 240 },
  { "date": "2026-09-09", "minutes": 180 }
]
```

Uses:

```text
TimeBlock.start_time
TimeBlock.end_time
```

### 6. Activity breakdown

```json
[
  { "type": "created", "count": 34 },
  { "type": "completed", "count": 28 },
  { "type": "status_changed", "count": 42 },
  { "type": "priority_changed", "count": 8 },
  { "type": "time_block_added", "count": 19 }
]
```

Uses:

```text
TaskActivity.activity_type
```

### 7. Recent activity

```json
[
  {
    "type": "completed",
    "task_title": "Build dashboard",
    "user_name": "Abdo",
    "created_at": "2026-09-09T10:30:00Z"
  }
]
```

Your current `TaskActivity` has `task_id` and `user_id`, so you can join to `Task` and `User`.

## Recommended endpoint

```text
GET /api/workspaces/<workspace_id>/analytics?period=week
```

Possible periods:

```text
week
month
year
```

Return one response containing all dashboard data:

```json
{
  "period": {
    "name": "week",
    "from": "2026-09-07",
    "to": "2026-09-13"
  },
  "summary": {
    "tasks_completed": 28,
    "tasks_created": 34,
    "tasks_in_progress": 5,
    "completion_rate": 82.35,
    "focus_minutes": 1125
  },
  "completion_trend": [],
  "tasks_by_project": [],
  "tasks_by_status": [],
  "tasks_by_priority": [],
  "focus_trend": [],
  "activity_breakdown": [],
  "recent_activity": []
}
```

## Important issue in `TimeBlock`

Your `to_dict()` currently returns:

```python
"task": self.task
```

Do not return the raw SQLAlchemy object in JSON. Use:

```python
"task_id": str(self.task_id)
```

or a small task summary.

## Frontend flow

```tsx
const response = await axios.get(
  `${API_URL}/workspaces/${workspaceId}/analytics?period=week`,
  { withCredentials: true }
);

setAnalytics(response.data);
```

Then:

```tsx
<LineChart data={analytics.completion_trend}>
```

Replace your current hardcoded:

```tsx
const weeklyTasks = [...]
```

with API data.

The best first version is:

1. Summary cards
2. Completion trend
3. Tasks by status
4. Tasks by project
5. Focus time
6. Recent activity

That gives you useful analytics without overbuilding the dashboard.

Created 4 todos
'''
