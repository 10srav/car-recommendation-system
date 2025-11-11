// Main JavaScript for Indian Automotive Marketplace

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Smooth scroll for anchor links
    $('a[href^="#"]').on('click', function(event) {
        var target = $(this.getAttribute('href'));
        if(target.length) {
            event.preventDefault();
            $('html, body').stop().animate({
                scrollTop: target.offset().top - 70
            }, 1000);
        }
    });

    // Format currency inputs
    $('.currency-input').on('blur', function() {
        var value = parseInt($(this).val());
        if (!isNaN(value)) {
            $(this).val(value.toLocaleString('en-IN'));
        }
    });

    // Form validation feedback
    $('form').on('submit', function() {
        var form = $(this);
        if (!form[0].checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.addClass('was-validated');
    });

    // Image lazy loading
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }

    // Add loading spinner to buttons on click
    $('.btn-loading').on('click', function() {
        var btn = $(this);
        btn.prop('disabled', true);
        btn.html('<span class="spinner-border spinner-border-sm me-2"></span>Loading...');
    });

    // Number formatting helper
    window.formatCurrency = function(value) {
        return '₹' + value.toLocaleString('en-IN');
    };

    // Success message display
    window.showSuccess = function(message) {
        var alertHtml = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="bi bi-check-circle-fill"></i> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        $('.container').first().prepend(alertHtml);

        setTimeout(function() {
            $('.alert').fadeOut('slow');
        }, 5000);
    };

    // Error message display
    window.showError = function(message) {
        var alertHtml = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="bi bi-exclamation-triangle-fill"></i> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        $('.container').first().prepend(alertHtml);

        setTimeout(function() {
            $('.alert').fadeOut('slow');
        }, 5000);
    };

    // EMI Calculator
    window.calculateEMI = function(principal, rate, tenure) {
        var monthlyRate = rate / (12 * 100);
        var emi = principal * monthlyRate * Math.pow(1 + monthlyRate, tenure) /
                  (Math.pow(1 + monthlyRate, tenure) - 1);
        return Math.round(emi);
    };

    // Back to top button
    var backToTop = $('<button class="btn btn-primary btn-floating" id="backToTop" style="position: fixed; bottom: 20px; right: 20px; display: none; z-index: 999;"><i class="bi bi-arrow-up"></i></button>');
    $('body').append(backToTop);

    $(window).scroll(function() {
        if ($(this).scrollTop() > 300) {
            $('#backToTop').fadeIn();
        } else {
            $('#backToTop').fadeOut();
        }
    });

    $('#backToTop').click(function() {
        $('html, body').animate({scrollTop: 0}, 600);
        return false;
    });

    // Console log to show app is loaded
    console.log('%cIndian Automotive Marketplace', 'color: #0d6efd; font-size: 20px; font-weight: bold;');
    console.log('%cApplication loaded successfully', 'color: #198754; font-size: 14px;');
});

// Price range formatter
function formatPriceRange(min, max) {
    return `₹${(min/100000).toFixed(1)}L - ₹${(max/100000).toFixed(1)}L`;
}

// Phone number formatter for India
function formatPhoneNumber(phone) {
    // Remove all non-digits
    var cleaned = ('' + phone).replace(/\D/g, '');

    // Format as +91-XXXXX-XXXXX
    if (cleaned.length === 10) {
        return '+91-' + cleaned.substring(0, 5) + '-' + cleaned.substring(5);
    }

    return phone;
}

// Validate email
function isValidEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Validate Indian phone number
function isValidIndianPhone(phone) {
    var cleaned = ('' + phone).replace(/\D/g, '');
    return cleaned.length === 10;
}
