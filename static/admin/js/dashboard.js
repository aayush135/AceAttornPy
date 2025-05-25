(function($) {
    $(document).ready(function() {
        // Add dashboard stats to the top of the page
        if ($('.model-contactmessage.change-list').length) {
            var stats = {
                total: window.dashboard_stats.total_messages || 0,
                unread: window.dashboard_stats.unread_messages || 0,
                recent: window.dashboard_stats.recent_messages || 0,
                services: window.dashboard_stats.total_services || 0,
                active_services: window.dashboard_stats.active_services || 0
            };

            var statsHtml = `
                <div class="dashboard-stats">
                    <div class="stat-card">
                        <h3>Messages Overview</h3>
                        <div class="stat-item">
                            <span class="stat-value">${stats.total}</span>
                            <span class="stat-label">Total Messages</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value unread-count">${stats.unread}</span>
                            <span class="stat-label">Unread Messages</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value">${stats.recent}</span>
                            <span class="stat-label">Recent Messages (7 days)</span>
                        </div>
                    </div>
                    <div class="stat-card">
                        <h3>Services Overview</h3>
                        <div class="stat-item">
                            <span class="stat-value">${stats.services}</span>
                            <span class="stat-label">Total Services</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-value active-count">${stats.active_services}</span>
                            <span class="stat-label">Active Services</span>
                        </div>
                    </div>
                </div>
            `;

            $('.module.filtered').before(statsHtml);
        }
    });
})(django.jQuery);
