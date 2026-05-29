# System Issue: Frontend Restructure with Vue Router & Modern UI/UX

## Context
The current frontend uses a single-route architecture with all features on one page. We need to restructure this into a multi-route application with Vue Router and implement a modern, professional design using glass morphism effects with backdrop-filter blur.

---

## Task Breakdown

### Phase 1: Vue Router Setup
- Install and configure `vue-router`
- Create route structure:
  - `/` → Home (Introduction + Feature Groups)
  - `/jobseeker/scrape` → Scrape & Find Matches
  - `/jobseeker/analyze` → Detailed CV-JD Analysis
  - `/hr/rank` → Bulk CV Ranking

### Phase 2: Home Page Design
- Hero section with project introduction
- Two collapsible/accordion sections:
  1. **Job Seeker Features** (expandable)
     - Scrape & Find Matches card
     - Detailed CV-JD Analysis card
  2. **HR Features** (expandable)
     - Bulk CV Ranking card
- Each card links to its respective route

### Phase 3: UI/UX Implementation
- **Design System** (from ui-ux-pro-max):
  - Primary: `#0369A1`
  - Secondary: `#0EA5E9`
  - CTA: `#22C55E`
  - Background: `#F0F9FF`
  - Text: `#0C4A6E`
  - Font: Plus Jakarta Sans
- **Glass Morphism Effects**:
  - `backdrop-filter: blur(16px)`
  - `background: rgba(255, 255, 255, 0.7)`
  - Subtle borders with `border: 1px solid rgba(255, 255, 255, 0.3)`
- **Components**:
  - Navbar with route links
  - Collapsible accordion for feature groups
  - Feature cards with hover effects
  - Form components for each feature

### Phase 4: Responsive Design
- Mobile-first approach
- Breakpoints: 375px, 768px, 1024px, 1440px
- Collapsible menu for mobile

---

## Definition of Done (DoD)
- Vue Router installed and configured
- All 4 routes functional
- Home page with collapsible feature sections
- Glass morphism UI with backdrop-filter blur
- Responsive design works on all breakpoints
- Hot-reload still works in Docker
- No CORS errors

---

## Technical Notes
- Use Vue 3 Composition API (`<script setup>`)
- Keep existing backend endpoints unchanged
- Update `App.vue` as main layout with `<router-view>`
- Create `views/` folder for route components
- Create `components/` folder for reusable UI elements
