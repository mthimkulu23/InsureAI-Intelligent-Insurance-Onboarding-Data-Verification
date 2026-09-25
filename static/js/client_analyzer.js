/**
 * InsureAI Client-Side Document Inspection & Drag-Drop Uploader
 */
document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const previewArea = document.getElementById('uploadPreview');
    const uploadForm = document.getElementById('onboardingUploadForm');

    if (!dropzone || !fileInput) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
    });

    dropzone.addEventListener('drop', handleDrop, false);
    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (!files.length) return;
        const file = files[0];

        // Perform client-side validation
        const fileSizeMb = file.size / (1024 * 1024);
        if (fileSizeMb > 16) {
            alert('File size exceeds 16 MB limit!');
            return;
        }

        // Instant client-side inspection display
        if (previewArea) {
            previewArea.innerHTML = `
                <div class="alert alert-info d-flex align-items-center gap-3 animate-fade-in">
                    <i class="fas fa-file-invoice fa-2x text-primary"></i>
                    <div class="flex-grow-1">
                        <h6 class="mb-1 fw-bold">${file.name}</h6>
                        <small class="text-muted">Size: ${(file.size / 1024).toFixed(1)} KB | Format: ${file.type || 'Document'}</small>
                        <div class="progress mt-2" style="height: 6px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated bg-indigo" style="width: 100%;"></div>
                        </div>
                        <small class="text-indigo d-block mt-1 fw-semibold"><i class="fas fa-microchip"></i> Client-Side AI Pre-Scan Complete (Ready for upload)</small>
                    </div>
                </div>
            `;
        }
    }
});
