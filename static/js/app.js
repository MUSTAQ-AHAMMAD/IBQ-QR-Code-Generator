// QR Code Generator Frontend Application

let currentFilename = null;

// Form submission handler
document.getElementById('qrForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await generateQRCode();
});

// Generate QR Code
async function generateQRCode() {
    const statusMessage = document.getElementById('statusMessage');
    const previewContainer = document.getElementById('previewContainer');
    const downloadSection = document.getElementById('downloadSection');
    
    // Show loading
    statusMessage.className = 'status-message';
    statusMessage.style.display = 'block';
    statusMessage.textContent = 'Generating QR code...';
    previewContainer.innerHTML = '<div class="spinner"></div>';
    downloadSection.style.display = 'none';
    
    try {
        // Collect form data
        const formData = collectFormData();
        
        // Prepare request
        const request = {
            business_card: {
                name: formData.name,
                phone: formData.phone || null,
                email: formData.email || null,
                company: formData.company || null,
                job_title: formData.jobTitle || null,
                website: formData.website || null,
                address: formData.address || null,
                city: formData.city || null,
                state: formData.state || null,
                postal_code: formData.postalCode || null,
                country: formData.country || null,
                notes: formData.notes || null
            },
            size: parseInt(formData.size),
            border: parseInt(formData.border),
            error_correction: formData.errorCorrection,
            foreground_color: formData.foregroundColor,
            background_color: formData.backgroundColor,
            output_format: formData.outputFormat,
            include_logo: false
        };
        
        // Make API request
        const response = await fetch('/api/v1/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate QR code');
        }
        
        const result = await response.json();
        
        // Display success
        statusMessage.className = 'status-message success';
        statusMessage.textContent = result.message;
        
        // Show preview
        currentFilename = result.filename;
        displayPreview(result);
        
        // Show download button
        downloadSection.style.display = 'block';
        document.getElementById('fileInfo').textContent = 
            `File: ${result.filename} (${formatFileSize(result.file_size)})`;
        
    } catch (error) {
        statusMessage.className = 'status-message error';
        statusMessage.textContent = `Error: ${error.message}`;
        previewContainer.innerHTML = '<div class="preview-placeholder">Failed to generate QR code</div>';
    }
}

// Collect form data
function collectFormData() {
    const form = document.getElementById('qrForm');
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    return data;
}

// Display preview
function displayPreview(result) {
    const previewContainer = document.getElementById('previewContainer');
    const format = result.format.toLowerCase();
    
    if (format === 'png') {
        // Display PNG image
        previewContainer.innerHTML = `
            <img src="/api/v1/download/${result.filename}" alt="QR Code" />
        `;
    } else if (format === 'svg') {
        // Display SVG
        previewContainer.innerHTML = `
            <img src="/api/v1/download/${result.filename}" alt="QR Code" />
        `;
    } else if (format === 'pdf') {
        // Show PDF icon/info
        previewContainer.innerHTML = `
            <div class="preview-placeholder">
                <svg width="100" height="100" viewBox="0 0 100 100" fill="#667eea">
                    <path d="M30 10h30l10 10v60H30V10z"/>
                    <path d="M60 10v10h10" fill="none" stroke="white" stroke-width="2"/>
                    <text x="50" y="55" text-anchor="middle" fill="white" font-size="20" font-weight="bold">PDF</text>
                </svg>
                <p style="margin-top: 15px; color: #667eea; font-weight: 600;">
                    PDF generated successfully
                </p>
            </div>
        `;
    }
}

// Download QR Code
document.getElementById('downloadBtn').addEventListener('click', () => {
    if (currentFilename) {
        window.location.href = `/api/v1/download/${currentFilename}`;
    }
});

// Reset form
function resetForm() {
    document.getElementById('qrForm').reset();
    document.getElementById('previewContainer').innerHTML = `
        <div class="preview-placeholder">
            <svg width="200" height="200" viewBox="0 0 200 200">
                <rect width="200" height="200" fill="#f0f0f0"/>
                <text x="100" y="100" text-anchor="middle" fill="#999" font-size="16">
                    Generate a QR code
                </text>
            </svg>
        </div>
    `;
    document.getElementById('downloadSection').style.display = 'none';
    document.getElementById('statusMessage').style.display = 'none';
    currentFilename = null;
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB';
    else return (bytes / 1048576).toFixed(2) + ' MB';
}

// Real-time validation
document.getElementById('name').addEventListener('input', (e) => {
    if (e.target.value.trim() === '') {
        e.target.style.borderColor = '#ef4444';
    } else {
        e.target.style.borderColor = '#10b981';
    }
});

document.getElementById('email').addEventListener('input', (e) => {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (e.target.value && !emailPattern.test(e.target.value)) {
        e.target.style.borderColor = '#ef4444';
    } else if (e.target.value) {
        e.target.style.borderColor = '#10b981';
    } else {
        e.target.style.borderColor = '#e0e0e0';
    }
});
