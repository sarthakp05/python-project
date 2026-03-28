// Custom JavaScript for HMS

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Sidebar active link handling
    const currentUrl = window.location.href;
    $('.sidebar-link').each(function() {
        if(currentUrl.includes($(this).attr('href')) && $(this).attr('href') !== '/') {
            $(this).addClass('active');
        }
    });

    // Auto-dismiss toasts after 5 seconds
    setTimeout(function() {
        $('.toast').each(function() {
            var toast = new bootstrap.Toast($(this));
            toast.hide();
        });
    }, 5000);
});
