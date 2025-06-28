# Files to Delete from Documents App

1. **Redundant model files:**
   - `c:\Users\Viesturs\anaconda_projects\quality_tools_v3\myproject\apps\documents\models\document_section.py`
     - Reason: Duplicates functionality in section.py

2. **Files with deprecated QualityDocument references:**
   - `c:\Users\Viesturs\anaconda_projects\quality_tools_v3\myproject\apps\documents\signals.py`
     - Reason: Has references to QualityDocument which is no longer needed
   - `c:\Users\Viesturs\anaconda_projects\quality_tools_v3\myproject\apps\documents\models\comment.py`
     - Reason: References QualityDocument; should be updated to use Document instead
   - `c:\Users\Viesturs\anaconda_projects\quality_tools_v3\myproject\apps\documents\utils\document_numbering.py`
     - Reason: Contains functions specific to QualityDocument

3. **Duplicate model file:**
   - `c:\Users\Viesturs\anaconda_projects\quality_tools_v3\myproject\apps\documents\models\document_attachment.py`
     - Reason: Duplicates functionality in attachment.py

## Update These Files

1. **models/document.py:**
   - Remove QualityDocument class
   - Keep only the Document model

2. **models/__init__.py:**
   - Remove QualityDocument import and from __all__ list

3. **admin.py:**
   - Remove QualityDocumentAdmin class and registration

4. **tests.py:**
   - Update to remove QualityDocument tests
