// Real-time QR Code Generator
// Handles live preview and instant QR code generation

(function() {
    'use strict';

    let debounceTimer = null;
    let currentQRData = null;
    const DEBOUNCE_DELAY = 800; // milliseconds

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeQRGenerator();
    });

    function initializeQRGenerator() {
        const form = document.getElementById('qrCodeForm');
        if (!form) return;

        // Get CSRF token
        const csrfToken = document.querySelector('input[name="csrf_token"]')?.value;
        if (!csrfToken) {
            console.error('CSRF token not found');
            return;
        }

        // Attach event listeners to all form inputs
        attachFormListeners(form);

        // Initialize with default QR type
        const qrTypeSelect = document.getElementById('qrType');
        if (qrTypeSelect) {
            showFieldsForType(qrTypeSelect.value);
            generatePreview(); // Generate initial preview
        }

        // Handle QR type changes
        if (qrTypeSelect) {
            qrTypeSelect.addEventListener('change', function() {
                showFieldsForType(this.value);
                generatePreview();
            });
        }

        // Handle gradient toggle
        const gradientCheckbox = document.querySelector('input[name="gradient_enabled"]');
        if (gradientCheckbox) {
            gradientCheckbox.addEventListener('change', function() {
                const gradientOptions = document.getElementById('gradientOptions');
                if (gradientOptions) {
                    gradientOptions.style.display = this.checked ? 'block' : 'none';
                }
                generatePreview();
            });
        }

        // Handle frame style changes
        const frameStyleSelect = document.getElementById('frameStyle');
        if (frameStyleSelect) {
            frameStyleSelect.addEventListener('change', function() {
                const frameTextContainer = document.getElementById('frameTextContainer');
                const frameColorContainer = document.getElementById('frameColorContainer');
                if (frameTextContainer && frameColorContainer) {
                    const showFrameOptions = this.value !== 'none';
                    frameTextContainer.style.display = showFrameOptions ? 'block' : 'none';
                    frameColorContainer.style.display = showFrameOptions ? 'block' : 'none';
                }
                generatePreview();
            });
        }
    }

    function attachFormListeners(form) {
        // Get all input elements that should trigger preview updates
        const inputs = form.querySelectorAll('input:not([type="submit"]), textarea, select');

        inputs.forEach(input => {
            // Skip certain inputs that shouldn't trigger preview
            if (input.name === 'csrf_token' || input.name === 'submit') {
                return;
            }

            // Add event listener based on input type
            if (input.type === 'checkbox' || input.type === 'radio' || input.tagName === 'SELECT') {
                input.addEventListener('change', debounceGeneratePreview);
            } else if (input.type === 'color') {
                input.addEventListener('input', debounceGeneratePreview);
            } else {
                input.addEventListener('input', debounceGeneratePreview);
            }
        });
    }

    function debounceGeneratePreview() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(generatePreview, DEBOUNCE_DELAY);
    }

    async function generatePreview() {
        const form = document.getElementById('qrCodeForm');
        if (!form) return;

        // Show loading state
        showLoadingState();

        try {
            // Collect form data
            const formData = collectFormData(form);

            // Validate required fields based on QR type
            if (!validateFormData(formData)) {
                showPlaceholder('Please fill in required fields');
                return;
            }

            // Prepare API request
            const requestData = {
                qr_type: formData.qr_type,
                form_data: formData,
                size: parseInt(formData.size) || 300,
                foreground_color: formData.foreground_color || '#000000',
                background_color: formData.background_color || '#FFFFFF',
                error_correction: formData.error_correction || 'H',
                border: parseInt(formData.border) || 4,
                qr_style: formData.qr_style || 'square',
                gradient_enabled: formData.gradient_enabled === 'y',
                gradient_color: formData.gradient_color,
                gradient_type: formData.gradient_type || 'linear',
                frame_style: formData.frame_style || 'none',
                frame_text: formData.frame_text,
                frame_color: formData.frame_color || '#000000',
                eye_style: formData.eye_style || 'square',
                data_style: formData.data_style || 'square'
            };

            // Get CSRF token
            const csrfToken = document.querySelector('input[name="csrf_token"]').value;

            // Make API request
            const response = await fetch('/api/preview-qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to generate preview');
            }

            const result = await response.json();

            if (result.success) {
                currentQRData = result;
                displayPreview(result.image);
            } else {
                throw new Error(result.error || 'Unknown error');
            }

        } catch (error) {
            console.error('Preview error:', error);
            showError(error.message);
        }
    }

    function collectFormData(form) {
        const formData = {};
        const elements = form.elements;

        for (let i = 0; i < elements.length; i++) {
            const element = elements[i];

            if (element.name && element.name !== 'csrf_token' && element.name !== 'submit') {
                if (element.type === 'checkbox') {
                    formData[element.name] = element.checked ? 'y' : 'n';
                } else if (element.type === 'radio') {
                    if (element.checked) {
                        formData[element.name] = element.value;
                    }
                } else {
                    formData[element.name] = element.value;
                }
            }
        }

        return formData;
    }

    function validateFormData(formData) {
        const qrType = formData.qr_type;

        // Basic validation based on QR type
        switch (qrType) {
            case 'url':
                return formData.url && formData.url.trim() !== '';
            case 'text':
                return formData.text_content && formData.text_content.trim() !== '';
            case 'email':
                return formData.email_address && formData.email_address.trim() !== '';
            case 'phone':
                return formData.phone_number && formData.phone_number.trim() !== '';
            case 'sms':
                return formData.sms_phone && formData.sms_phone.trim() !== '';
            case 'wifi':
                return formData.wifi_ssid && formData.wifi_ssid.trim() !== '';
            case 'vcard':
                return formData.contact_name && formData.contact_name.trim() !== '';
            case 'event':
                return formData.event_title && formData.event_title.trim() !== '';
            case 'location':
                return formData.location_latitude && formData.location_longitude;
            default:
                return formData.social_url || formData.app_url || true;
        }
    }

    function showFieldsForType(type) {
        const allFields = document.querySelectorAll('.qr-type-fields');
        allFields.forEach(field => field.style.display = 'none');

        const fieldsToShow = document.getElementById('fields-' + type);
        if (fieldsToShow) {
            fieldsToShow.style.display = 'block';
        }
    }

    function showLoadingState() {
        const previewBox = document.getElementById('qrPreviewBox');
        if (previewBox) {
            previewBox.innerHTML = '<div class="qr-preview-loading"></div>';
        }

        // Show progress bar
        showProgress();
    }

    function displayPreview(imageData) {
        const previewBox = document.getElementById('qrPreviewBox');
        if (previewBox) {
            previewBox.innerHTML = `
                <img src="data:image/png;base64,${imageData}"
                     alt="QR Code Preview"
                     class="qr-preview-image"
                     id="qrPreviewImage">
            `;
        }

        // Hide progress bar
        hideProgress();

        // Show download hint
        showToast('QR Code generated! Submit form to save and download.', 'info');
    }

    function showPlaceholder(message) {
        const previewBox = document.getElementById('qrPreviewBox');
        if (previewBox) {
            previewBox.innerHTML = `
                <div class="qr-preview-placeholder">
                    <i class="bi bi-qr-code"></i>
                    <p>${message || 'Your QR code will appear here'}</p>
                </div>
            `;
        }
        hideProgress();
    }

    function showError(message) {
        const previewBox = document.getElementById('qrPreviewBox');
        if (previewBox) {
            previewBox.innerHTML = `
                <div class="qr-preview-placeholder">
                    <i class="bi bi-exclamation-triangle text-danger"></i>
                    <p class="text-danger">${message || 'Error generating preview'}</p>
                </div>
            `;
        }
        hideProgress();
    }

    function showProgress() {
        let progressBar = document.getElementById('generationProgress');
        if (!progressBar) {
            progressBar = document.createElement('div');
            progressBar.id = 'generationProgress';
            progressBar.className = 'generation-progress';
            document.body.appendChild(progressBar);
        }
        progressBar.classList.add('active');
    }

    function hideProgress() {
        const progressBar = document.getElementById('generationProgress');
        if (progressBar) {
            progressBar.classList.remove('active');
        }
    }

    function showToast(message, type = 'info') {
        if (typeof window.showToast === 'function') {
            window.showToast(message, type);
        }
    }

    // Export functions for use in other scripts if needed
    window.qrGenerator = {
        generatePreview,
        showPlaceholder
    };

})();
