/**
 * InsureAI Core Interface Logic
 */
document.addEventListener('DOMContentLoaded', () => {
    // Bootstrap tooltip init
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(el => new bootstrap.Tooltip(el));

    // Entity pill filter for verification report page
    document.querySelectorAll('.entity-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            document.querySelectorAll('.entity-pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            const filterKey = pill.textContent.trim();
            const rows = document.querySelectorAll('.vr-field-row');
            rows.forEach(row => {
                const key = row.querySelector('.vr-field-key');
                if (!key) return;
                if (filterKey === 'All Fields') {
                    row.style.display = '';
                } else {
                    row.style.display = key.textContent.trim() === filterKey ? '' : 'none';
                }
            });
        });
    });
});

/**
 * markDocumentStatus — shows a premium confirmation modal then calls the API
 * @param {string} docId   - MongoDB document _id
 * @param {string} newStatus - 'VERIFIED' or 'FAKE'
 */
function markDocumentStatus(docId, newStatus) {
    const isVerified = newStatus === 'VERIFIED';

    // Create modal markup
    const overlay = document.createElement('div');
    overlay.id = 'statusConfirmOverlay';
    overlay.style.cssText = `
        position:fixed;inset:0;z-index:99999;
        display:flex;align-items:center;justify-content:center;
        background:rgba(15,23,42,0.65);backdrop-filter:blur(6px);
        animation:fadeIn 0.2s ease;
    `;

    overlay.innerHTML = `
        <div style="
            background:#fff;border-radius:24px;padding:2.5rem;
            max-width:420px;width:90%;box-shadow:0 32px 80px rgba(0,0,0,0.3);
            animation:slideUp 0.25s cubic-bezier(0.16,1,0.3,1);
            text-align:center;
        ">
            <div style="
                width:70px;height:70px;border-radius:50%;
                background:${isVerified ? '#dcfce7' : '#fee2e2'};
                display:flex;align-items:center;justify-content:center;
                margin:0 auto 1.25rem auto;font-size:2rem;
            ">
                <i class="fas ${isVerified ? 'fa-shield-check' : 'fa-times-circle'}"
                   style="color:${isVerified ? '#16a34a' : '#dc2626'};"></i>
            </div>
            <h5 style="font-weight:800;color:#1e293b;margin-bottom:0.5rem;">
                ${isVerified ? 'Confirm Document as Verified?' : 'Mark Document as Failed?'}
            </h5>
            <p style="color:#64748b;font-size:0.9rem;margin-bottom:1.75rem;">
                ${isVerified
                    ? 'This will set the document status to <strong>VERIFIED</strong> and update the confidence score. This action can be reversed.'
                    : 'This will flag the document as <strong>FAILED / REJECTED</strong> and reduce the confidence score. This action can be reversed.'
                }
            </p>
            <div style="display:flex;gap:0.75rem;justify-content:center;">
                <button id="cancelStatusBtn"
                    style="flex:1;padding:0.75rem 1rem;border-radius:12px;border:1.5px solid #e2e8f0;
                           background:#fff;color:#64748b;font-weight:600;font-size:0.9rem;cursor:pointer;">
                    Cancel
                </button>
                <button id="confirmStatusBtn"
                    style="flex:1;padding:0.75rem 1rem;border-radius:12px;border:none;
                           background:${isVerified ? 'linear-gradient(135deg,#16a34a,#22c55e)' : 'linear-gradient(135deg,#dc2626,#ef4444)'};
                           color:#fff;font-weight:700;font-size:0.9rem;cursor:pointer;
                           box-shadow:0 4px 16px ${isVerified ? 'rgba(34,197,94,0.35)' : 'rgba(239,68,68,0.35)'};">
                    <i class="fas ${isVerified ? 'fa-check' : 'fa-times'} me-2"></i>
                    ${isVerified ? 'Yes, Verify It' : 'Yes, Mark Failed'}
                </button>
            </div>
        </div>`;

    // Inject slide-up animation
    if (!document.getElementById('statusModalStyle')) {
        const style = document.createElement('style');
        style.id = 'statusModalStyle';
        style.textContent = '@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}';
        document.head.appendChild(style);
    }

    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';

    // Cancel
    document.getElementById('cancelStatusBtn').addEventListener('click', () => {
        overlay.remove();
        document.body.style.overflow = '';
    });

    // Click outside to cancel
    overlay.addEventListener('click', e => {
        if (e.target === overlay) { overlay.remove(); document.body.style.overflow = ''; }
    });

    // Confirm
    document.getElementById('confirmStatusBtn').addEventListener('click', () => {
        const confirmBtn = document.getElementById('confirmStatusBtn');
        confirmBtn.disabled = true;
        confirmBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Updating...';

        fetch('/api/verify/' + docId, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        })
        .then(res => res.json())
        .then(data => {
            overlay.remove();
            document.body.style.overflow = '';

            if (data.success) {
                updateVerificationUI(newStatus);
                showStatusToast(
                    isVerified ? 'Document confirmed as VERIFIED successfully.' : 'Document marked as FAILED.',
                    isVerified ? 'success' : 'danger'
                );
            } else {
                showStatusToast('Error: ' + (data.error || 'Could not update status.'), 'danger');
            }
        })
        .catch(err => {
            overlay.remove();
            document.body.style.overflow = '';
            showStatusToast('Network error — could not reach server. Please try again.', 'danger');
            console.error(err);
        });
    });
}

/**
 * Update the verification page UI in-place after a status change (no page reload needed)
 */
function updateVerificationUI(newStatus) {
    const isVerified = newStatus === 'VERIFIED';
    const isFailed = newStatus === 'FAKE' || newStatus === 'REJECTED';

    // Update top status badge
    const topBadge = document.querySelector('.vr-topbar .badge');
    if (topBadge) {
        if (isVerified) {
            topBadge.className = 'badge bg-success px-3 py-2 rounded-pill fs-6';
            topBadge.innerHTML = '<i class="fas fa-shield-check me-1"></i> VERIFIED';
        } else {
            topBadge.className = 'badge bg-danger px-3 py-2 rounded-pill fs-6';
            topBadge.innerHTML = '<i class="fas fa-times-circle me-1"></i> FAILED';
        }
    }

    // Update the status footer in the right panel
    const statusFooter = document.querySelector('.vr-right-panel .p-4.border-top .d-flex.align-items-center');
    if (statusFooter) {
        statusFooter.innerHTML = isVerified
            ? `<div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
                    style="width:44px;height:44px;background:#dcfce7;color:#16a34a;font-size:1.3rem;">
                    <i class="fas fa-shield-check"></i></div>
               <div><div class="fw-bold text-success">Document Verified</div>
               <div class="text-muted small">Status updated successfully</div></div>`
            : `<div class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
                    style="width:44px;height:44px;background:#fee2e2;color:#dc2626;font-size:1.3rem;">
                    <i class="fas fa-times-circle"></i></div>
               <div><div class="fw-bold text-danger">Verification Failed</div>
               <div class="text-muted small">Document flagged as anomalous</div></div>`;
    }

    // Highlight action buttons to show which was just applied
    const markFailedBtn = document.querySelector('button[onclick*="FAKE"]');
    const confirmVerBtn = document.querySelector('button[onclick*="VERIFIED"]');
    if (isVerified && confirmVerBtn) {
        confirmVerBtn.style.background = 'linear-gradient(135deg,#16a34a,#22c55e)';
        confirmVerBtn.innerHTML = '<i class="fas fa-check-circle me-1"></i> Verified ✓';
    }
    if (isFailed && markFailedBtn) {
        markFailedBtn.style.borderColor = '#dc2626';
        markFailedBtn.style.background = '#fee2e2';
        markFailedBtn.innerHTML = '<i class="fas fa-times-circle me-1"></i> Failed ✓';
    }
}

/**
 * Show a floating toast notification
 */
function showStatusToast(message, type) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        container.style.cssText = 'position:fixed;top:1.25rem;right:1.25rem;z-index:99999;display:flex;flex-direction:column;align-items:flex-end;gap:0.5rem;';
        document.body.appendChild(container);
    }
    const colors = { success: '#10b981', danger: '#ef4444', warning: '#f59e0b', info: '#0ea5e9' };
    const bg = colors[type] || colors.info;
    const toast = document.createElement('div');
    toast.style.cssText = `background:${bg};color:#fff;padding:0.85rem 1.25rem;border-radius:14px;
        font-size:0.9rem;font-weight:600;box-shadow:0 8px 24px rgba(0,0,0,0.18);
        animation:fadeIn 0.3s ease;max-width:400px;display:flex;align-items:center;gap:0.75rem;`;
    toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'danger' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>${message}`;
    container.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.4s'; setTimeout(() => toast.remove(), 400); }, 4000);
}

