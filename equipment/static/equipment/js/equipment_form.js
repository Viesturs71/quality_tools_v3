document.addEventListener('DOMContentLoaded', function() {
    const equipmentTypeField = document.getElementById('id_equipment_type');
    const metrologicalSection = document.querySelector('#metrological-section');
    const maintenanceSection = document.querySelector('#maintenance-section');
    
    function toggleSections() {
        if (!equipmentTypeField) return;
        
        // Get the selected option text
        const selectedOption = equipmentTypeField.options[equipmentTypeField.selectedIndex];
        const selectedText = selectedOption ? selectedOption.text.trim() : '';
        
        // Check if "Measuring Instrument" is selected
        const isMeasuringInstrument = selectedText.toLowerCase().includes('measuring instrument');
        
        // Show/hide the appropriate sections
        if (metrologicalSection) {
            metrologicalSection.style.display = isMeasuringInstrument ? 'block' : 'none';
        }
        
        if (maintenanceSection) {
            // For regular equipment, show maintenance schedule
            // For measuring instruments, hide maintenance (they use metrological control instead)
            maintenanceSection.style.display = isMeasuringInstrument ? 'none' : 'block';
        }
    }
    
    // Set initial state
    toggleSections();
    
    // Add event listener for changes
    if (equipmentTypeField) {
        equipmentTypeField.addEventListener('change', toggleSections);
    }
});
