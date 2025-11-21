<?php
/**
 * Astra functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Astra
 * @since 1.0.0
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit; // Exit if accessed directly.
}

/**
 * Define Constants
 */
define( 'ASTRA_THEME_VERSION', '4.11.13' );
define( 'ASTRA_THEME_SETTINGS', 'astra-settings' );
define( 'ASTRA_THEME_DIR', trailingslashit( get_template_directory() ) );
define( 'ASTRA_THEME_URI', trailingslashit( esc_url( get_template_directory_uri() ) ) );
define( 'ASTRA_THEME_ORG_VERSION', file_exists( ASTRA_THEME_DIR . 'inc/w-org-version.php' ) );

/**
 * Minimum Version requirement of the Astra Pro addon.
 * This constant will be used to display the notice asking user to update the Astra addon to the version defined below.
 */
define( 'ASTRA_EXT_MIN_VER', '4.11.6' );

/**
 * Load in-house compatibility.
 */
if ( ASTRA_THEME_ORG_VERSION ) {
	require_once ASTRA_THEME_DIR . 'inc/w-org-version.php';
}

/**
 * Setup helper functions of Astra.
 */
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-theme-options.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-theme-strings.php';
require_once ASTRA_THEME_DIR . 'inc/core/common-functions.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-icons.php';

define( 'ASTRA_WEBSITE_BASE_URL', 'https://wpastra.com' );

/**
 * Deprecate constants in future versions as they are no longer used in the codebase.
 */
define( 'ASTRA_PRO_UPGRADE_URL', ASTRA_THEME_ORG_VERSION ? astra_get_pro_url( '/pricing/', 'free-theme', 'dashboard', 'upgrade' ) : 'https://woocommerce.com/products/astra-pro/' );
define( 'ASTRA_PRO_CUSTOMIZER_UPGRADE_URL', ASTRA_THEME_ORG_VERSION ? astra_get_pro_url( '/pricing/', 'free-theme', 'customizer', 'upgrade' ) : 'https://woocommerce.com/products/astra-pro/' );

/**
 * Update theme
 */
require_once ASTRA_THEME_DIR . 'inc/theme-update/astra-update-functions.php';
require_once ASTRA_THEME_DIR . 'inc/theme-update/class-astra-theme-background-updater.php';

/**
 * Fonts Files
 */
require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-font-families.php';
if ( is_admin() ) {
	require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-fonts-data.php';
}

require_once ASTRA_THEME_DIR . 'inc/lib/webfont/class-astra-webfont-loader.php';
require_once ASTRA_THEME_DIR . 'inc/lib/docs/class-astra-docs-loader.php';
require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-fonts.php';

require_once ASTRA_THEME_DIR . 'inc/dynamic-css/custom-menu-old-header.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/container-layouts.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/astra-icons.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-walker-page.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-enqueue-scripts.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-gutenberg-editor-css.php';
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-wp-editor-css.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/block-editor-compatibility.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/inline-on-mobile.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/content-background.php';
require_once ASTRA_THEME_DIR . 'inc/dynamic-css/dark-mode.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-dynamic-css.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-global-palette.php';

// Enable NPS Survey only if the starter templates version is < 4.3.7 or > 4.4.4 to prevent fatal error.
if ( ! defined( 'ASTRA_SITES_VER' ) || version_compare( ASTRA_SITES_VER, '4.3.7', '<' ) || version_compare( ASTRA_SITES_VER, '4.4.4', '>' ) ) {
	// NPS Survey Integration
	require_once ASTRA_THEME_DIR . 'inc/lib/class-astra-nps-notice.php';
	require_once ASTRA_THEME_DIR . 'inc/lib/class-astra-nps-survey.php';
}

/**
 * Custom template tags for this theme.
 */
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-attr.php';
require_once ASTRA_THEME_DIR . 'inc/template-tags.php';

require_once ASTRA_THEME_DIR . 'inc/widgets.php';
require_once ASTRA_THEME_DIR . 'inc/core/theme-hooks.php';
require_once ASTRA_THEME_DIR . 'inc/admin-functions.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-memory-limit-notice.php';
require_once ASTRA_THEME_DIR . 'inc/core/sidebar-manager.php';

/**
 * Markup Functions
 */
require_once ASTRA_THEME_DIR . 'inc/markup-extras.php';
require_once ASTRA_THEME_DIR . 'inc/extras.php';
require_once ASTRA_THEME_DIR . 'inc/blog/blog-config.php';
require_once ASTRA_THEME_DIR . 'inc/blog/blog.php';
require_once ASTRA_THEME_DIR . 'inc/blog/single-blog.php';

/**
 * Markup Files
 */
require_once ASTRA_THEME_DIR . 'inc/template-parts.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-loop.php';
require_once ASTRA_THEME_DIR . 'inc/class-astra-mobile-header.php';

/**
 * Functions and definitions.
 */
require_once ASTRA_THEME_DIR . 'inc/class-astra-after-setup-theme.php';

// Required files.
require_once ASTRA_THEME_DIR . 'inc/core/class-astra-admin-helper.php';

require_once ASTRA_THEME_DIR . 'inc/schema/class-astra-schema.php';

/* Setup API */
require_once ASTRA_THEME_DIR . 'admin/includes/class-astra-api-init.php';

if ( is_admin() ) {
	/**
	 * Admin Menu Settings
	 */
	require_once ASTRA_THEME_DIR . 'inc/core/class-astra-admin-settings.php';
	require_once ASTRA_THEME_DIR . 'admin/class-astra-admin-loader.php';
	require_once ASTRA_THEME_DIR . 'inc/lib/astra-notices/class-astra-notices.php';
}

/**
 * Metabox additions.
 */
require_once ASTRA_THEME_DIR . 'inc/metabox/class-astra-meta-boxes.php';
require_once ASTRA_THEME_DIR . 'inc/metabox/class-astra-meta-box-operations.php';
require_once ASTRA_THEME_DIR . 'inc/metabox/class-astra-elementor-editor-settings.php';

/**
 * Customizer additions.
 */
require_once ASTRA_THEME_DIR . 'inc/customizer/class-astra-customizer.php';

/**
 * Astra Modules.
 */
require_once ASTRA_THEME_DIR . 'inc/modules/posts-structures/class-astra-post-structures.php';
require_once ASTRA_THEME_DIR . 'inc/modules/related-posts/class-astra-related-posts.php';

/**
 * Compatibility
 */
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-gutenberg.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-jetpack.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/woocommerce/class-astra-woocommerce.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/edd/class-astra-edd.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/lifterlms/class-astra-lifterlms.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/learndash/class-astra-learndash.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-beaver-builder.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-bb-ultimate-addon.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-contact-form-7.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-visual-composer.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-site-origin.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-gravity-forms.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-bne-flyout.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-ubermeu.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-divi-builder.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-amp.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-yoast-seo.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/surecart/class-astra-surecart.php';
require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-starter-content.php';
require_once ASTRA_THEME_DIR . 'inc/addons/transparent-header/class-astra-ext-transparent-header.php';
require_once ASTRA_THEME_DIR . 'inc/addons/breadcrumbs/class-astra-breadcrumbs.php';
require_once ASTRA_THEME_DIR . 'inc/addons/scroll-to-top/class-astra-scroll-to-top.php';
require_once ASTRA_THEME_DIR . 'inc/addons/heading-colors/class-astra-heading-colors.php';
require_once ASTRA_THEME_DIR . 'inc/builder/class-astra-builder-loader.php';

// Elementor Compatibility requires PHP 5.4 for namespaces.
if ( version_compare( PHP_VERSION, '5.4', '>=' ) ) {
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-elementor.php';
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-elementor-pro.php';
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-web-stories.php';
}

// Beaver Themer compatibility requires PHP 5.3 for anonymous functions.
if ( version_compare( PHP_VERSION, '5.3', '>=' ) ) {
	require_once ASTRA_THEME_DIR . 'inc/compatibility/class-astra-beaver-themer.php';
}

require_once ASTRA_THEME_DIR . 'inc/core/markup/class-astra-markup.php';

/**
 * Load deprecated functions
 */
require_once ASTRA_THEME_DIR . 'inc/core/deprecated/deprecated-filters.php';
require_once ASTRA_THEME_DIR . 'inc/core/deprecated/deprecated-hooks.php';
require_once ASTRA_THEME_DIR . 'inc/core/deprecated/deprecated-functions.php';

/* ============================================================================
   CUSTOM FOOD DELIVERY API CONFIGURATION
   ============================================================================ */

// Increase WPGetAPI timeout to 30 seconds
function wpgetapi_set_request_args_parameters( $args ) {
    $args['timeout'] = 30;  // 30 seconds
    return $args;
}
add_filter( 'wpgetapi_default_request_args_parameters', 'wpgetapi_set_request_args_parameters' );

// Increase PHP execution time for API requests
function increase_php_timeout_for_api() {
    if (is_admin() || (defined('DOING_AJAX') && DOING_AJAX)) {
        set_time_limit(60);  // 60 seconds
    }
}
add_action('init', 'increase_php_timeout_for_api');

// API Base URL - YOUR BACKEND API
define('API_BASE_URL', 'https://food-delivery-api-fr4f.onrender.com/api');

// API Request Helper Function
function make_api_request($endpoint, $method = 'GET', $data = null, $token = null) {
    $url = API_BASE_URL . $endpoint;
    
    $headers = array(
        'Content-Type' => 'application/json',
    );
    
    // Add JWT token if provided
    if ($token) {
        $headers['Authorization'] = 'Bearer ' . $token;
    }
    
    $args = array(
        'method' => $method,
        'headers' => $headers,
        'timeout' => 30,
        'sslverify' => true, // Enable SSL verification for security
    );
    
    if ($data) {
        $args['body'] = json_encode($data);
    }
    
    $response = wp_remote_request($url, $args);
    
    if (is_wp_error($response)) {
        return array('error' => $response->get_error_message());
    }
    
    $body = wp_remote_retrieve_body($response);
    $status_code = wp_remote_retrieve_response_code($response);
    
    return array(
        'status' => $status_code,
        'data' => json_decode($body, true)
    );
}

/* ============================================================================
   COMPLETE CSP (Content Security Policy) HEADERS - SIMPLE VERSION
   ============================================================================ */

// Complete CSP headers for all resources - SIMPLE AND WORKING
function add_full_csp_headers() {
    // Don't add in admin
    if (is_admin()) {
        return;
    }
    
    header("Content-Security-Policy: 
    default-src 'self'; 
    connect-src 'self' https://food-delivery-api-fr4f.onrender.com https://*.onrender.com https://*.hostingersite.com https://checkout.razorpay.com https://api.razorpay.com https://lumberjack.razorpay.com https://maps.googleapis.com https://*.googleapis.com; 
    script-src 'self' 'unsafe-inline' 'unsafe-eval' https://checkout.razorpay.com https://api.razorpay.com https://maps.googleapis.com https://*.googleapis.com; 
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; 
    font-src 'self' data: https://fonts.gstatic.com https://fonts.googleapis.com; 
    img-src 'self' data: https: http:; 
    frame-src 'self' https://api.razorpay.com https://checkout.razorpay.com https://maps.google.com https://www.google.com;");
}
add_action('send_headers', 'add_full_csp_headers');

// Remove conflicting CSP headers
function remove_default_csp_headers() {
    header_remove('Content-Security-Policy');
    header_remove('X-Content-Security-Policy');
}
add_action('init', 'remove_default_csp_headers');

/* ============================================================================
   ADDITIONAL SECURITY HEADERS
   ============================================================================ */

// Add security headers
function add_security_headers() {
    if (is_admin()) {
        return;
    }
    
    // Prevent MIME type sniffing
    header('X-Content-Type-Options: nosniff');
    
    // Enable XSS protection
    header('X-XSS-Protection: 1; mode=block');
    
    // Control referrer information
    header('Referrer-Policy: strict-origin-when-cross-origin');
    
    // Permissions Policy (formerly Feature Policy)
    header('Permissions-Policy: geolocation=(self), microphone=(), camera=()');
}
add_action('send_headers', 'add_security_headers', 10);

/* ============================================================================
   CORS HEADERS FOR API REQUESTS
   ============================================================================ */

// Enable CORS for your backend API
function add_cors_headers() {
    // Allow requests from your WordPress domain to backend API
    header('Access-Control-Allow-Origin: https://lightskyblue-ostrich-354680.hostingersite.com');
    header('Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
    header('Access-Control-Allow-Credentials: true');
    header('Access-Control-Max-Age: 86400'); // Cache preflight for 24 hours
}
add_action('send_headers', 'add_cors_headers', 10);

/* ============================================================================
   RAZORPAY PAYMENT GATEWAY SUPPORT
   ============================================================================ */

// Add specific CSP for Razorpay on checkout pages
function add_razorpay_csp_meta() {
    // Check if it's checkout page or payment page
    if (is_page(array('checkout', 'payment', 'my-account', 'cart'))) {
        echo '<meta http-equiv="Content-Security-Policy" content="script-src \'self\' \'unsafe-inline\' \'unsafe-eval\' https://checkout.razorpay.com https://api.razorpay.com; frame-src \'self\' https://api.razorpay.com; connect-src \'self\' https://api.razorpay.com https://lumberjack.razorpay.com https://food-delivery-api-fr4f.onrender.com;">' . "\n";
    }
}
add_action('wp_head', 'add_razorpay_csp_meta', 1);

/* ============================================================================
   UTILITY FUNCTIONS FOR FRONTEND
   ============================================================================ */

// Load Razorpay SDK
function load_razorpay_sdk() {
    // Load Razorpay checkout script on payment/checkout pages
    $is_checkout_page = (function_exists('is_checkout') && is_checkout()) || is_page(array('checkout', 'payment', 'my-account', 'cart'));
    
    if ($is_checkout_page) {
        wp_enqueue_script('razorpay-checkout', 'https://checkout.razorpay.com/v1/checkout.js', array(), null, true);
    }
}
add_action('wp_enqueue_scripts', 'load_razorpay_sdk');

// Add inline script to expose API base URL to JavaScript
function expose_api_config_to_js() {
    ?>
    <script>
        window.FOOD_DELIVERY_CONFIG = {
            apiBaseUrl: '<?php echo esc_js(API_BASE_URL); ?>',
            googleMapsKey: 'AIzaSyD1v0RxpSZc4HvO5GO4dTyGfUqi89oiHI0',
            razorpayKeyId: 'rzp_test_Rf8SX4fcBCXLU3', // Test mode key
            siteUrl: '<?php echo esc_js(home_url()); ?>'
        };
        
        // Load Razorpay dynamically if not loaded
        if (typeof Razorpay === 'undefined' && !document.querySelector('script[src*="razorpay"]')) {
            const rzpScript = document.createElement('script');
            rzpScript.src = 'https://checkout.razorpay.com/v1/checkout.js';
            rzpScript.async = true;
            document.head.appendChild(rzpScript);
        }
    </script>
    <?php
}
add_action('wp_head', 'expose_api_config_to_js', 5);

/* ============================================================================
   ELEMENTOR COMPATIBILITY
   ============================================================================ */

// Ensure Elementor HTML widget can execute inline scripts
function allow_elementor_inline_scripts($policy) {
    $policy->add_rule('script-src', "'unsafe-inline'");
    $policy->add_rule('script-src', "'unsafe-eval'");
    return $policy;
}
// Note: This may not work with all CSP implementations, 
// dynamic script loading in FIXED files is the proper solution

/* ============================================================================
   AJAX ENDPOINTS FOR CUSTOM FUNCTIONALITY
   ============================================================================ */

// Example: Proxy API requests through WordPress (optional, for additional security)
function proxy_api_request() {
    check_ajax_referer('food_delivery_nonce', 'nonce');
    
    $endpoint = isset($_POST['endpoint']) ? sanitize_text_field($_POST['endpoint']) : '';
    $method = isset($_POST['method']) ? sanitize_text_field($_POST['method']) : 'GET';
    $data = isset($_POST['data']) ? json_decode(stripslashes($_POST['data']), true) : null;
    $token = isset($_POST['token']) ? sanitize_text_field($_POST['token']) : null;
    
    if (empty($endpoint)) {
        wp_send_json_error(array('message' => 'Endpoint is required'));
        return;
    }
    
    $response = make_api_request($endpoint, $method, $data, $token);
    wp_send_json_success($response);
}
add_action('wp_ajax_proxy_api_request', 'proxy_api_request');
add_action('wp_ajax_nopriv_proxy_api_request', 'proxy_api_request');

// Add nonce for AJAX requests
function add_ajax_nonce() {
    ?>
    <script>
        window.foodDeliveryNonce = '<?php echo wp_create_nonce('food_delivery_nonce'); ?>';
    </script>
    <?php
}
add_action('wp_head', 'add_ajax_nonce', 5);

/* ============================================================================
   PERFORMANCE OPTIMIZATIONS
   ============================================================================ */

// Defer JavaScript loading for better performance
function defer_javascript_loading($tag, $handle) {
    // Don't defer admin scripts or jQuery
    if (is_admin() || $handle === 'jquery') {
        return $tag;
    }
    
    // Add defer attribute to all scripts
    return str_replace(' src', ' defer src', $tag);
}
// Uncomment to enable: add_filter('script_loader_tag', 'defer_javascript_loading', 10, 2);

/* ============================================================================
   CLEANUP AND MAINTENANCE
   ============================================================================ */

// Clear transients and cache when needed
function clear_food_delivery_cache() {
    // Clear WordPress transients
    delete_transient('food_delivery_menu_cache');
    delete_transient('food_delivery_restaurants_cache');
    
    // Clear object cache if available
    if (function_exists('wp_cache_flush')) {
        wp_cache_flush();
    }
}
// Call this function when you update menu items or restaurants

?>
