/**
 * JavaScript for the Job Application Tracker
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const applicationForm = document.getElementById('application-form');
    const cardView = document.getElementById('card-view');
    const tableView = document.getElementById('table-view');
    const cardViewBtn = document.getElementById('card-view-btn');
    const tableViewBtn = document.getElementById('table-view-btn');
    const filterStatus = document.getElementById('filter-status');
    const editModal = new bootstrap.Modal(document.getElementById('edit-modal'));
    const editForm = document.getElementById('edit-form');
    const saveBtn = document.getElementById('save-btn');
    const deleteBtn = document.getElementById('delete-btn');
    
    // State
    let applications = [];
    let currentFilter = 'All';
    let currentView = 'card';
    let currentEditId = null;
    
    // Initialize
    fetchApplications();
    
    // Event Listeners
    if (applicationForm) {
        applicationForm.addEventListener('submit', handleAddApplication);
    }
    
    if (saveBtn) {
        saveBtn.addEventListener('click', handleUpdateApplication);
    }
    
    if (cardViewBtn) {
        cardViewBtn.addEventListener('click', () => switchView('card'));
    }
    
    if (tableViewBtn) {
        tableViewBtn.addEventListener('click', () => switchView('table'));
    }
    
    if (filterStatus) {
        filterStatus.addEventListener('change', handleFilterChange);
    }
    
    if (deleteBtn) {
        deleteBtn.addEventListener('click', handleDeleteApplication);
    }
    
    /**
     * Fetch all job applications from the API
     */
    function fetchApplications() {
        fetch('/job-tracker/api/applications')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                applications = data;
                renderApplications();
            })
            .catch(error => {
                console.error('Error fetching applications:', error);
                showEmptyState('Error loading applications. Please try again.');
            });
    }
    
    /**
     * Render applications based on current view and filter
     */
    function renderApplications() {
        // Filter applications if needed
        const filteredApps = currentFilter === 'All' 
            ? applications 
            : applications.filter(app => app.status === currentFilter);
        
        if (filteredApps.length === 0) {
            showEmptyState('No applications found. Add your first job application!');
            return;
        }
        
        // Render based on current view
        if (currentView === 'card') {
            renderCardView(filteredApps);
        } else {
            renderTableView(filteredApps);
        }
    }
    
    /**
     * Render applications in card view
     */
    function renderCardView(apps) {
        cardView.innerHTML = '';
        
        apps.forEach(app => {
            const statusClass = app.status.toLowerCase();
            const col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4 mb-3';
            
            col.innerHTML = `
                <div class="card application-card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="company-name mb-0">${app.company}</h5>
                        <span class="status-badge ${statusClass}">${app.status}</span>
                    </div>
                    <div class="card-body">
                        <p class="role">${app.role}</p>
                        <p class="date">Applied: ${formatDate(app.date_applied)}</p>
                        ${app.notes ? `<p class="notes">${app.notes}</p>` : ''}
                    </div>
                    <div class="card-footer text-end">
                        <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${app.id}">Edit</button>
                    </div>
                </div>
            `;
            
            cardView.appendChild(col);
            
            // Add edit button event listener
            col.querySelector('.edit-btn').addEventListener('click', () => openEditModal(app));
        });
    }
    
    /**
     * Render applications in table view
     */
    function renderTableView(apps) {
        const tbody = tableView.querySelector('tbody');
        tbody.innerHTML = '';
        
        apps.forEach(app => {
            const statusClass = app.status.toLowerCase();
            const row = document.createElement('tr');
            
            row.innerHTML = `
                <td>${app.company}</td>
                <td>${app.role}</td>
                <td>${formatDate(app.date_applied)}</td>
                <td class="status-cell"><span class="status-badge ${statusClass}">${app.status}</span></td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${app.id}">Edit</button>
                </td>
            `;
            
            tbody.appendChild(row);
            
            // Add edit button event listener
            row.querySelector('.edit-btn').addEventListener('click', () => openEditModal(app));
        });
    }
    
    /**
     * Show empty state message
     */
    function showEmptyState(message) {
        if (currentView === 'card') {
            cardView.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <div class="icon">📋</div>
                        <p class="message">${message}</p>
                        <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#add-modal">Add Your First Application</button>
                    </div>
                </div>
            `;
        } else {
            const tbody = tableView.querySelector('tbody');
            tbody.innerHTML = `
                <tr>
                    <td colspan="5">
                        <div class="empty-state">
                            <div class="icon">📋</div>
                            <p class="message">${message}</p>
                        </div>
                    </td>
                </tr>
            `;
        }
    }
    
    /**
     * Handle adding a new application
     */
    function handleAddApplication(e) {
        e.preventDefault();
        
        const formData = new FormData(applicationForm);
        const application = {
            company: formData.get('company'),
            role: formData.get('role'),
            date_applied: formData.get('date-applied'),
            status: formData.get('status'),
            notes: formData.get('notes')
        };
        
        fetch('/job-tracker/api/applications', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(application)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Add to applications array and re-render
            applications.unshift(data);
            renderApplications();
            
            // Reset form
            applicationForm.reset();
            
            // Show success message
            showToast('Application added successfully!', 'success');
        })
        .catch(error => {
            console.error('Error adding application:', error);
            showToast('Error adding application. Please try again.', 'danger');
        });
    }
    
    /**
     * Open edit modal with application data
     */
    function openEditModal(application) {
        currentEditId = application.id;
        
        // Fill form with application data
        document.getElementById('edit-id').value = application.id;
        document.getElementById('edit-company').value = application.company;
        document.getElementById('edit-role').value = application.role;
        document.getElementById('edit-date-applied').value = application.date_applied;
        document.getElementById('edit-status').value = application.status;
        document.getElementById('edit-notes').value = application.notes || '';
        
        // Show modal
        editModal.show();
    }
    
    /**
     * Handle updating an application
     */
    function handleUpdateApplication() {
        if (!currentEditId) return;
        
        const formData = new FormData(editForm);
        const application = {
            company: formData.get('edit-company'),
            role: formData.get('edit-role'),
            date_applied: formData.get('edit-date-applied'),
            status: formData.get('edit-status'),
            notes: formData.get('edit-notes')
        };
        
        fetch(`/job-tracker/api/applications/${currentEditId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(application)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Update in applications array
            const index = applications.findIndex(app => app.id === currentEditId);
            if (index !== -1) {
                applications[index] = data;
            }
            
            // Re-render and close modal
            renderApplications();
            editModal.hide();
            
            // Show success message
            showToast('Application updated successfully!', 'success');
        })
        .catch(error => {
            console.error('Error updating application:', error);
            showToast('Error updating application. Please try again.', 'danger');
        });
    }
    
    /**
     * Handle deleting an application
     */
    function handleDeleteApplication() {
        if (!currentEditId) return;
        
        if (confirm('Are you sure you want to delete this application?')) {
            fetch(`/job-tracker/api/applications/${currentEditId}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Remove from applications array
                applications = applications.filter(app => app.id !== currentEditId);
                
                // Re-render and close modal
                renderApplications();
                editModal.hide();
                
                // Show success message
                showToast('Application deleted successfully!', 'success');
            })
            .catch(error => {
                console.error('Error deleting application:', error);
                showToast('Error deleting application. Please try again.', 'danger');
            });
        }
    }
    
    /**
     * Switch between card and table views
     */
    function switchView(view) {
        if (view === currentView) return;
        
        currentView = view;
        
        if (view === 'card') {
            cardView.style.display = 'flex';
            tableView.style.display = 'none';
            cardViewBtn.classList.add('active');
            tableViewBtn.classList.remove('active');
        } else {
            cardView.style.display = 'none';
            tableView.style.display = 'block';
            cardViewBtn.classList.remove('active');
            tableViewBtn.classList.add('active');
        }
        
        renderApplications();
    }
    
    /**
     * Handle filter change
     */
    function handleFilterChange(e) {
        currentFilter = e.target.value;
        renderApplications();
    }
    
    /**
     * Format date for display
     */
    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    }
    
    /**
     * Show toast notification
     */
    function showToast(message, type = 'info') {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.setAttribute('aria-live', 'assertive');
        toastEl.setAttribute('aria-atomic', 'true');
        
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;
        
        toastContainer.appendChild(toastEl);
        
        // Initialize and show toast
        const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 5000 });
        toast.show();
        
        // Remove toast after it's hidden
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });
    }
});
