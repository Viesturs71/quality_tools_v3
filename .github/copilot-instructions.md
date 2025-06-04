# Quality Tools Project Development Guidelines

## Admin Login Specifications

The admin login page follows a compact, focused design with the following specifications:

### Container and Layout
- Container width: max-width of 28rem
- Container margin: 3rem auto (reduced vertical spacing)
- Container padding: 1.5rem
- Container background: white (#ffffff)
- Container shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)
- Container border radius: 0.5rem

### Typography
- Font family: "Times New Roman", Times, serif
- Login title: 1.5rem font size, bold weight
- Form labels: 0.875rem font size
- Input fields: Inherit font family from container

### Form Elements
- Form labels: Block display, 0.25rem bottom margin, medium (500) weight
- Input fields: Full width, 0.4rem vertical and 0.75rem horizontal padding
- Input field margins: 0.75rem bottom margin
- Input borders: 1px solid var(--border-color), border-radius 0.25rem
- Submit button: Full width, primary color background, 0.4rem vertical and 0.75rem horizontal padding
- Password reset link: Right-aligned, 0.5rem bottom margin, 0.875rem font size

### Colors
- Primary color: #3E7391
- Primary hover color: #2c5269
- Text light color: #ffffff (white)
- Background light color: #f9fafb
- Border color: #e5e7eb
- Error container: #fee2e2 background, #ef4444 border, #b91c1c text

### Language Selector
- Positioned at the top right of the form
- 0.75rem bottom margin
- Label font size: 0.875rem
- Select input: White background, border-radius 0.25rem, 0.25rem vertical and 0.5rem horizontal padding
- Select font size: 0.875rem
- Auto-submit on change via JavaScript

### Compact Spacing
- Compact form rows with 0.5rem bottom margin
- Reduced vertical spacing throughout the form
- No header title duplication - only "Log in" title shown
- Overall compact layout to minimize scrolling and height

### Key Features
- Language selector before login form
- Clear error messaging when applicable
- Accessible form controls with appropriate labeling
- Responsive layout that works on various screen sizes
- Clean, professional appearance with consistent styling

## Project Structure Requirements

### Model Organization
- All Django models should be organized in a 'models' folder within their respective app directory
- Confirmed working structure in: equipment, methods, quality_docs, standards
- Each model should be in a separate file within the models folder (e.g., `document.py`, `equipment.py`)
- The models package must have an __init__.py file that imports and exposes all models
- Use relative imports like `from .document import Document, QualityDocument`

### Template Structure
- Templates should be located in a 'templates/[app_name]' directory structure
- Confirmed working directories: templates/accounts, templates/dashboard, templates/equipment, 
  templates/personnel, templates/quality_docs, templates/standards
- For example, equipment templates should be in 'templates/equipment/'

### URL Organization
- URLs should be organized with proper namespaces that match the app names
- Use 'namespace' parameter when including URLs in the main urls.py file
- For example: `path('documents/', include('quality_docs.urls', namespace='quality_docs'))`

## Admin Navigation Structure

The admin interface is organized into these main sections:
1. **Authentication and Authorization**
   - Users
   - Groups
   - Permissions
2. **Companies**
   - Companies
   - Departments
   - Locations
3. **Equipment Management**
   - Equipment Registry
   - Equipment Categories
   - Maintenance Records
4. **Management Documentation (Documents)**
   - Quality Documents
   - Document Types
   - Document Sections
5. **Personnel Management**
   - Staff Records
   - Qualifications
   - Training Records
6. **Standards**
   - Standards
   - Standard Sections
7. **User Accounts**
   - User Profiles
   - User Roles
   - User Permissions

Each section should be collapsible with proper FontAwesome icons and the appropriate styling.

## Color Scheme
- Primary: #3E7391 (custom blue)
- Primary hover: #2c5269 (darker blue)
- Secondary: gray-200 (#e5e7eb)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Form field labels: 0.875rem font size
- Required fields marked with asterisk (*)