# A Task Manager Application


frontend/
├── public/                      # Static assets (favicons, images)
│   └── vite.svg
├── src/                         # Main source code
│   ├── assets/                  # Images, SVGs, global styles for specific components
│   ├── components/              # Reusable UI components (Dumb components)
│   │   ├── layout/
│   │   │   ├── Navbar.tsx       # Top navigation bar
│   │   │   ├── Sidebar.tsx      # Sidebar for navigation (optional)
│   │   │   └── Layout.tsx       # Wraps pages with Navbar + Main content area
│   │   ├── tasks/
│   │   │   ├── TaskCard.tsx     # Single task item
│   │   │   ├── TaskModal.tsx    # Modal to create/edit a task
│   │   │   └── TaskList.tsx     # Maps over tasks and renders TaskCards
│   │   └── ui/                  # Basic reusable UI elements (Buttons, Inputs)
│   │       ├── Button.tsx
│   │       ├── Input.tsx
│   │       └── Spinner.tsx
│   ├── pages/                   # Route-level components (Smart components)
│   │   ├── Home.tsx             # Landing page / Dashboard
│   │   ├── Login.tsx            # Login form
│   │   ├── Register.tsx         # (Optional) Sign up page
│   │   ├── TaskPage.tsx         # Main task board (Kanban/List)
│   │   └── NotFound.tsx         # 404 page
│   ├── context/                 # Global state (React Context API)
│   │   └── AuthContext.tsx      # Manages user login status and token
│   ├── hooks/                   # Custom React hooks
│   │   ├── useAuth.ts           # Hook to easily access AuthContext
│   │   └── useTasks.ts          # Hook to fetch and manage tasks
│   ├── services/ (or utils/)    # API calls, external logic
│   │   ├── api.ts               # Axios/fetch instance (base URL, interceptors)
│   │   └── taskService.ts       # Functions like getTasks, createTask, deleteTask
│   ├── types/                   # TypeScript interfaces/types
│   │   └── index.ts             # Task, User, AuthResponse interfaces
│   ├── App.css                  # Global CSS
│   ├── App.tsx                  # Main Router setup & Route definitions
│   ├── main.tsx                 # React entry point (ReactDOM.createRoot)
│   └── vite-env.d.ts
├── .gitignore
├── eslint.config.js
├── index.html                   # Root HTML
├── package-lock.json
├── package.json
├── README.md
├── tsconfig.app.json
├── tsconfig.json
└── tsconfig.node.json