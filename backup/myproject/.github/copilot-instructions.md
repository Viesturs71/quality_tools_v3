# Quality Tools Project Coding Guidelines

## Application Structure
The application is divided into two main sections:

### 1. Administrative Section
- Defines core application requirements and settings
- Manages user roles and permissions
- Configures workflows and approval processes
- Sets up document templates and categories
- Manages equipment types and categories
- Establishes company structure and departments
- Configures system-wide settings and preferences
- Accessible only to administrators and managers
- Allows adding and removing modules
- Language selection (interface can be multilingual, but core terminology is in English)

#### Administrative Modules
1. **Account Management** - User accounts, permissions, and access control
2. **Documentation** - Document templates, categories, and workflow configuration
   - **Standards Registry** - Manages standards with their sections and subsections
     - Each standard includes:
       - Standard Number (unique identifier)
       - Title in English (primary language)
       - Title in selected language (secondary language)
       - Publication year
     - Standards have hierarchical sections and subsections
     - Section text is stored in both English and the selected language
     - Searchable and filterable standards database
     - Version tracking for standards updates
   - **Company Documents** - Manages internal company documentation
     - Document Types (e.g., Work Instructions, Procedures, Forms, etc.)
       - Document Type Name
       - Abbreviation
       - Description (explanation of document purpose and development requirements)
     - Document Sections (based on company's desired structure similar to file nomenclature)
       - Section Identifier
       - Section Name
       - Title
       - Hierarchical structure with subsections and sub-subsections
     - Document workflows with approval stages
     - Version control and revision history
     - Search and filter capabilities
3. **Equipment Management** - Equipment types, categories, and maintenance schedules
4. **Staff Management** - Personnel records, qualifications, and training
5. **Companies Management** - Each company has access to its own structure and data
6. **Risk Management** - Risk assessment, mitigation planning, and monitoring
7. **Audits** - Audit planning, execution, and reporting
8. **KPI** - Key Performance Indicators tracking and reporting

### 2. User Section
- Interface for entering information based on user access levels
- Electronic document submission, coordination, editing, and approval
- Equipment registry management and status tracking
- User profiles and personal settings
- Dashboard with personalized views based on role
- Document workflows with notifications
- Search and filtering capabilities
- Reporting and analytics features

#### User Modules
1. **User Information and Rights** - Personal profile and permissions overview
   - View assigned permissions and roles
   - Update personal information
   - Change password and security settings
   - View access history
   - Request additional permissions

2. **Documents Register (Dokumentu reģistrs)** - Access and manage organization's documentation
   - View documents organized by sections and categories
   - Each section contains approved documents related to that section
   - Documents become visible in the register only after approval
   - Document categorization based on department, type, and purpose
   - Search and filter capabilities for finding specific documents
   - Document hierarchy view showing relationships between documents
   - Version tracking and history for all registered documents
   - Access controls based on user permissions and roles
   - Download documents in various formats (PDF, DOC, etc.)
   - Recent documents section showing newly added or updated items
   - Structured registry layout:
     - Main sections (e.g., Quality, Safety, Operations)
       - Sub-sections (e.g., Procedures, Work Instructions)
         - Document entries with metadata and download options

3. **Equipment Management** - Monitor and update equipment information
   - View equipment status and requirements
   - Receive reminders about maintenance and metrological checks
   - Update equipment status changes
   - Record completed maintenance, repairs, and calibrations
   - Report equipment issues and malfunctions
   - Access equipment history and documentation

4. **Staff Management** - Maintain personnel information
   - View own personnel record
   - Update qualifications and certifications
   - View and register for training opportunities
   - Complete assigned training activities
   - Track qualification status and expirations
   - For managers: oversee team qualifications and training needs

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

6. **Risk Management** - Participate in risk management activities
   - Report potential risks and issues
   - Participate in risk assessments
   - View assigned risk mitigation actions
   - Update progress on risk controls
   - Receive alerts about critical risks

7. **Audits** - Engage in audit processes
   - View upcoming and scheduled audits
   - Prepare required documentation for audits
   - Respond to audit findings
   - Track corrective actions
   - Update action status and evidence

8. **KPI** - Monitor performance indicators
   - View relevant KPIs for area of responsibility
   - Input performance data as required
   - Generate reports on performance metrics
   - Analyze trends and patterns
   - Receive alerts for metrics outside acceptable ranges

### Equipment Documentation Requirements
- Each equipment can have attached documentation in PDF format up to 1MB
- Documentation section includes:
  - Document Type (User Manual, Certificate, Calibration Document, Maintenance Record, Warranty, Other)
  - Document Title
  - PDF File Upload (max 1MB, validates file size and extension)
  - External URL (optional, for linking to external resources)
  - Internal Reference (optional, for linking to internal documents in the system)
  - Description (optional)
- Automatic organization of documents:
  - Files are stored in structured paths: equipment_docs/{equipment_id}/{document_type}/{document_id}.pdf
  - Automatic cleanup when equipment or documents are deleted
  - Validation to ensure only valid PDF files are uploaded
- Integration with document management:
  - Equipment maintenance records linked to maintenance schedules
  - Equipment certificates linked to metrological control requirements
  - Warranty documents linked to equipment lifecycle management

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes

5. **Companies Management** - Access company-specific information
   - View organizational structure (based on permissions)
   - Access company documents and policies
   - View relevant company contacts and departments
   - Update information within authorized areas

## Color scheme
- Primary: blue-600 (#2563eb)
- Secondary: gray-200 (#e5e7eb)
- Accent: indigo-500 (#6366f1)
- Success: green-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Danger: red-500 (#ef4444)
- Info: sky-500 (#0ea5e9)
- Text: gray-700 (#374151)
- Background: white (#ffffff)
- Card background: gray-50 (#f9fafb)

## Header
- Full width with primary background color (blue-600)
- Logo on the left side
- Navigation menu in the center
- User profile/login on the right side
- Responsive, collapses to hamburger menu on mobile
- Fixed height of 64px (h-16)
- Shadow effect (shadow-md)
- z-index: 50

## Footer
- Full width with light background (gray-100)
- Copyright text in center/left
- Links to important pages on the right
- Container with max-width of 1280px (max-w-7xl)
- Padding: py-6 px-4
- Divide sections with dividers (divide-y)

## Navigation Panel
- Left-side vertical navigation for desktop
- Collapsible sections for grouped menu items
- Current active page highlighted (bg-blue-700)
- Hover effect on menu items (hover:bg-blue-700)
- Icons for each menu item from Heroicons
- Mobile: Bottom navigation bar or slide-in drawer
- Main sections:
  - Dashboard
  - Equipment Registry
  - Documents Register
  - Personnel
  - Standards
  - Administration

## Forms
- Labels above form fields
- Required fields marked with asterisk (*)
- Validation errors in red beneath the field
- Submit buttons using primary color
- Cancel buttons using secondary color
- Button order: Submit/Save on right, Cancel on left
- Form sections separated with headings and dividers
- Input padding: px-4 py-2
- Input borders: border border-gray-300 rounded

## Typography
- Base font: Times New Roman for all text content
- Font classes: font-serif
- Heading sizes:
  - h1: text-3xl (30px)
  - h2: text-2xl (24px)
  - h3: text-xl (20px)
  - h4: text-lg (18px)
- Body text: text-base (16px)
- Small text: text-sm (14px)
- Font weights:
  - Headings: font-bold
  - Body: font-normal
  - Emphasis: font-medium
- Line height: leading-normal for text, leading-tight for headings

## Tables
- Full width, responsive with horizontal scroll on small screens
- Striped rows (even:bg-gray-50)
- Hover effect on rows (hover:bg-gray-100)
- Headers with light background (bg-gray-100) and bold text
- Borders: border-collapse border border-gray-200
- Pagination controls below table
- Action buttons aligned right in last column

## Cards
- Rounded corners (rounded-lg)
- Shadow effect (shadow)
- Padding: p-6
- Header with title and optional action buttons
- Body with content and padding
- Footer with action buttons or meta information
- Hover effect on interactive cards (hover:shadow-lg)

## Modals
- Centered on screen with overlay (bg-black bg-opacity-50)
- Maximum width of 500px for forms, 800px for content
- Close button in top-right corner
- Header with title
- Body with content and padding
- Footer with action buttons (Save/Cancel)
- Animation: fade-in and slide-up

## Responsiveness
- Mobile-first approach
- Breakpoints:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
  - 2xl: 1536px
- Stack columns on mobile views
- Hide less important elements on smaller screens
- Use responsive text sizes and spacing

### Project Structure Requirements
- All Django models should be organized in a 'models' folder within their respective app directory
- Each model should be in a separate file within the models folder
- The models package should have an __init__.py file that imports and exposes all models
- All Django templates should be located in a 'templates/[app_name]' directory structure
  - For example, equipment templates should be in 'templates/equipment/'
  - This ensures proper template namespacing and avoids conflicts

#### Equipment Entry Form
1. **General Information**
   - Equipment Name* (required)
   - Equipment/Measuring Instrument Type* (required)
     - When selecting equipment: maintenance plan is prepared
     - When selecting measuring instrument: metrological control plan is prepared
     - Select equipment type - metrological control is required for measuring instruments
   - Model
   - Type
   - Manufacturer
   - Inventory Number* (required)
   - Serial Number* (required)
   - Location* (required)

2. **Documentation**
   - User Manual (file upload)
   - User Manual (URL)
   - Additional Documentation

3. **Department Information**
   - Department/Structural Unit
   - Person Responsible

4. **Dates and Financial Information**
   - Manufacture Date
   - Purchase Date
   - Purchase Price

5. **Metrological Control** (for measuring instruments)
   - Metrological Control Type
   - Metrological Control Institution
   - Certificate Number/Date
   - Metrological Control Periodicity
   - Next Verification Date

6. **Status Information**
   - Technical Status
   - Additional Information
   - Notes