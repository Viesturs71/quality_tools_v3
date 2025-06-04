/**
 * Document form controller for handling dynamic form behavior
 */
document.addEventListener('DOMContentLoaded', function() {
    // Document form controller
    const documentForm = {
        // Initialize the controller
        init: function() {
            this.setupEventListeners();
            this.setupInitialState();
            this.setupDebounce();
        },
        
        // Debounce function to limit API calls
        setupDebounce: function() {
            this.debounceTimeout = null;
            this.debounceDelay = 500; // ms
        },
        
        // Debounce method for the validation
        debounce: function(func) {
            if (this.debounceTimeout) {
                clearTimeout(this.debounceTimeout);
            }
            this.debounceTimeout = setTimeout(func, this.debounceDelay);
        },
        
        // Set up event listeners
        setupEventListeners: function() {
            const form = document.querySelector('form.document-form');
            if (!form) return;
            
            // Document type change
            const documentTypeSelect = form.querySelector('#id_document_type');
            if (documentTypeSelect) {
                documentTypeSelect.addEventListener('change', this.updateSections.bind(this));
            }
            
            // Company change
            const companySelect = form.querySelector('#id_company');
            if (companySelect) {
                companySelect.addEventListener('change', this.updateDocumentNumber.bind(this));
            }
            
            // Section change
            const sectionSelect = form.querySelector('#id_section');
            if (sectionSelect) {
                sectionSelect.addEventListener('change', this.updateDocumentNumber.bind(this));
            }
            
            // Generate number checkbox
            const generateNumberCheckbox = form.querySelector('#id_generate_number');
            if (generateNumberCheckbox) {
                generateNumberCheckbox.addEventListener('change', this.toggleDocumentNumberField.bind(this));
            }
            
            // Document number field validation
            const documentNumberField = form.querySelector('#id_document_number');
            if (documentNumberField) {
                documentNumberField.addEventListener('input', this.validateDocumentNumber.bind(this));
                documentNumberField.addEventListener('blur', this.validateDocumentNumber.bind(this));
            }
        },
        
        // Set up initial form state
        setupInitialState: function() {
            const form = document.querySelector('form.document-form');
            if (!form) return;
            
            // Set initial state of document number field based on generate_number checkbox
            this.toggleDocumentNumberField();
        },
        
        // Toggle document number field readonly attribute
        toggleDocumentNumberField: function() {
            const form = document.querySelector('form.document-form');
            const generateNumberCheckbox = form.querySelector('#id_generate_number');
            const documentNumberField = form.querySelector('#id_document_number');
            
            if (generateNumberCheckbox && documentNumberField) {
                if (generateNumberCheckbox.checked) {
                    documentNumberField.setAttribute('readonly', 'readonly');
                    // Generate preview of document number
                    this.updateDocumentNumber();
                } else {
                    documentNumberField.removeAttribute('readonly');
                    // Add validation feedback for manually entered number
                    this.validateDocumentNumber();
                }
            }
        },
        
        // Update document number preview
        updateDocumentNumber: function() {
            const form = document.querySelector('form.document-form');
            const generateNumberCheckbox = form.querySelector('#id_generate_number');
            const documentNumberField = form.querySelector('#id_document_number');
            const companySelect = form.querySelector('#id_company');
            const documentTypeSelect = form.querySelector('#id_document_type');
            const sectionSelect = form.querySelector('#id_section');
            
            // Only update if auto-generation is enabled
            if (!generateNumberCheckbox || !generateNumberCheckbox.checked) return;
            
            // Check if we have all necessary values
            if (!companySelect || !documentTypeSelect) return;
            
            const companyId = companySelect.value;
            const documentTypeId = documentTypeSelect.value;
            const sectionId = sectionSelect ? sectionSelect.value : '';
            
            if (!companyId || !documentTypeId) {
                documentNumberField.value = 'Select company and document type';
                return;
            }
            
            // Fetch document number preview from server
            fetch(`/api/generate-document-number-preview/?company=${companyId}&document_type=${documentTypeId}&section=${sectionId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.document_number) {
                        documentNumberField.value = data.document_number;
                        // Validate the generated number
                        this.validateDocumentNumber();
                    } else if (data.error) {
                        documentNumberField.value = data.error;
                    }
                })
                .catch(error => {
                    console.error('Error fetching document number preview:', error);
                    documentNumberField.value = 'Error generating number';
                });
        },
        
        // Validate document number
        validateDocumentNumber: function() {
            const form = document.querySelector('form.document-form');
            const documentNumberField = form.querySelector('#id_document_number');
            const documentIdField = form.querySelector('#id_id');
            
            if (!documentNumberField) return;
            
            // Get the document number
            const documentNumber = documentNumberField.value.trim();
            if (!documentNumber) return;
            
            // Get the document ID if editing an existing document
            const documentId = documentIdField ? documentIdField.value : '';
            
            // Create feedback element if it doesn't exist
            let feedbackElement = form.querySelector('.document-number-feedback');
            if (!feedbackElement) {
                feedbackElement = document.createElement('div');
                feedbackElement.className = 'document-number-feedback mt-1 text-sm';
                documentNumberField.parentNode.appendChild(feedbackElement);
            }
            
            // Debounce the validation to prevent too many API calls
            this.debounce(() => {
                // Send validation request to server
                const formData = new FormData();
                formData.append('document_number', documentNumber);
                if (documentId) {
                    formData.append('document_id', documentId);
                }
                
                fetch('/api/validate-document-number/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.valid) {
                        feedbackElement.className = 'document-number-feedback mt-1 text-sm text-green-600';
                        feedbackElement.textContent = data.message;
                        documentNumberField.classList.remove('border-red-500');
                        documentNumberField.classList.add('border-green-500');
                    } else {
                        feedbackElement.className = 'document-number-feedback mt-1 text-sm text-red-600';
                        feedbackElement.textContent = data.error;
                        documentNumberField.classList.remove('border-green-500');
                        documentNumberField.classList.add('border-red-500');
                    }
                })
                .catch(error => {
                    console.error('Error validating document number:', error);
                    feedbackElement.className = 'document-number-feedback mt-1 text-sm text-red-600';
                    feedbackElement.textContent = 'Error validating document number';
                    documentNumberField.classList.remove('border-green-500');
                    documentNumberField.classList.add('border-red-500');
                });
            });
        },
        
        // Update sections based on selected document type
        updateSections: function() {
            const form = document.querySelector('form.document-form');
            const documentTypeSelect = form.querySelector('#id_document_type');
            const sectionSelect = form.querySelector('#id_section');
            
            if (!documentTypeSelect || !sectionSelect) return;
            
            const documentTypeId = documentTypeSelect.value;
            
            if (!documentTypeId) return;
            
            // Fetch sections for selected document type
            fetch(`/api/document-type/${documentTypeId}/sections/`)
                .then(response => response.json())
                .then(data => {
                    // Clear current options
                    sectionSelect.innerHTML = '<option value="">---------</option>';
                    
                    // Add new options
                    data.sections.forEach(section => {
                        const option = document.createElement('option');
                        option.value = section.id;
                        option.textContent = section.name;
                        sectionSelect.appendChild(option);
                    });
                    
                    // Update document number after changing section options
                    this.updateDocumentNumber();
                })
                .catch(error => {
                    console.error('Error fetching sections:', error);
                });
        }
    };
    
    // Initialize the document form controller
    documentForm.init();
});
