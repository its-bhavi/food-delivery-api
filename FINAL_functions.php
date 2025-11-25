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

// API Base URL
define('API_BASE_URL', 'https://food-delivery-api-production-1d00.up.railway.app/api');

// Razorpay Configuration
define('RAZORPAY_KEY_ID', 'rzp_test_Rf8SX4fcBCXLU3');
define('RAZORPAY_KEY_SECRET', 'oAqctnCPvGY1S4u2Uxqo6FR7');

// Google Maps API Key
define('GOOGLE_MAPS_API_KEY', 'AIzaSyAMeehYlcfmKARKqpP--BVZj7C6GZCUqIQ');

/* ============================================================================
   CSP HEADERS - NO RESTRICTIONS FOR RAZORPAY AND MAPS
   ============================================================================ */

// COMPLETELY DISABLE CSP - NO RESTRICTIONS AT ALL
function remove_all_csp_headers() {
    if (is_admin()) {
        return;
    }
    
    // Remove ALL CSP headers
    header_remove('Content-Security-Policy');
    header_remove('Content-Security-Policy-Report-Only');
    header_remove('X-Content-Security-Policy');
    header_remove('X-WebKit-CSP');
    
    // DO NOT add any CSP - let everything load freely
}
add_action('send_headers', 'remove_all_csp_headers', 999);
add_action('wp_headers', 'remove_all_csp_headers', 999);
add_action('template_redirect', 'remove_all_csp_headers', 999);

/* ============================================================================
   DISABLE CONFLICTING SECURITY PLUGINS
   ============================================================================ */

// Disable other CSP headers
add_filter('wp_headers', function($headers) {
    unset($headers['Content-Security-Policy']);
    unset($headers['X-Content-Security-Policy']);
    unset($headers['X-WebKit-CSP']);
    return $headers;
}, 999);

/* ============================================================================
   EXPOSE CONFIGURATION TO FRONTEND
   ============================================================================ */

function expose_config_to_frontend() {
    ?>
    <script>
        window.FOOD_DELIVERY_CONFIG = {
            apiBaseUrl: '<?php echo esc_js(API_BASE_URL); ?>',
            googleMapsKey: '<?php echo esc_js(GOOGLE_MAPS_API_KEY); ?>',
            razorpayKeyId: '<?php echo esc_js(RAZORPAY_KEY_ID); ?>',
            siteUrl: '<?php echo esc_js(home_url()); ?>'
        };
        console.log('✅ Food Delivery Config Loaded:', window.FOOD_DELIVERY_CONFIG);
    </script>
    <?php
}
add_action('wp_head', 'expose_config_to_frontend', 1);

/* ============================================================================
   CORS HEADERS
   ============================================================================ */

function add_cors_headers() {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
    header('Access-Control-Allow-Credentials: true');
}
add_action('send_headers', 'add_cors_headers', 1);

/* ============================================================================
   CLEANUP
   ============================================================================ */

// Remove WordPress version and generator tags
remove_action('wp_head', 'wp_generator');

/* ============================================================================
   ROLE-BASED MENU FILTERING
   ============================================================================ */

// Register custom user roles
function register_food_delivery_roles() {
    // Customer role
    if (!get_role('customer')) {
        add_role('customer', 'Customer', array(
            'read' => true,
            'edit_posts' => false,
            'delete_posts' => false,
        ));
    }
    
    // Restaurant Owner role
    if (!get_role('restaurant_owner')) {
        add_role('restaurant_owner', 'Restaurant Owner', array(
            'read' => true,
            'edit_posts' => false,
            'delete_posts' => false,
        ));
    }
    
    // Delivery Partner role
    if (!get_role('delivery_partner')) {
        add_role('delivery_partner', 'Delivery Partner', array(
            'read' => true,
            'edit_posts' => false,
            'delete_posts' => false,
        ));
    }
}
add_action('init', 'register_food_delivery_roles');

// Filter menu items based on user role
function filter_menu_by_role($items, $args) {
    if (!is_user_logged_in()) {
        // Remove logged-in only pages for guests
        $guest_hidden_slugs = array(
            'my-orders', 'cart', 'checkout', 'track-order', 'order-status', 'order-confirmation',
            'restaurant-dashboard', 'restaurant-profile', 'restaurant-detail',
            'delivery-partner-dashboard', 'delivery-partner-profile'
        );
        
        foreach ($items as $key => $item) {
            if ($item->object == 'page') {
                $page_slug = get_post_field('post_name', $item->object_id);
                if (in_array($page_slug, $guest_hidden_slugs)) {
                    unset($items[$key]);
                }
            }
        }
        return $items;
    }
    
    $user = wp_get_current_user();
    $user_roles = $user->roles;
    $user_role = !empty($user_roles) ? $user_roles[0] : 'subscriber';
    
    // Pages to hide based on role
    $hide_slugs = array();
    
    if ($user_role === 'customer' || $user_role === 'subscriber') {
        // Hide vendor and delivery pages from customers
        $hide_slugs = array(
            'restaurant-dashboard', 'restaurant-profile', 'restaurant-detail',
            'delivery-partner-dashboard', 'delivery-partner-profile'
        );
    } 
    elseif ($user_role === 'restaurant_owner') {
        // Hide customer and delivery pages from restaurant owners
        $hide_slugs = array(
            'my-orders', 'cart', 'checkout', 'track-order', 'order-confirmation',
            'delivery-partner-dashboard', 'delivery-partner-profile'
        );
    } 
    elseif ($user_role === 'delivery_partner') {
        // Hide customer and vendor pages from delivery partners
        $hide_slugs = array(
            'my-orders', 'cart', 'checkout', 'track-order', 'order-status', 'order-confirmation',
            'restaurant-dashboard', 'restaurant-profile', 'restaurant-detail'
        );
    }
    
    // Remove hidden pages from menu
    foreach ($items as $key => $item) {
        if ($item->object == 'page') {
            $page_slug = get_post_field('post_name', $item->object_id);
            if (in_array($page_slug, $hide_slugs)) {
                unset($items[$key]);
            }
        }
    }
    
    return $items;
}
add_filter('wp_nav_menu_objects', 'filter_menu_by_role', 10, 2);

// Add role class to body tag for CSS targeting
function add_role_class_to_body($classes) {
    if (is_user_logged_in()) {
        $user = wp_get_current_user();
        $user_roles = $user->roles;
        $user_role = !empty($user_roles) ? $user_roles[0] : 'subscriber';
        $classes[] = 'role-' . $user_role;
        $classes[] = 'logged-in';
    } else {
        $classes[] = 'not-logged-in';
    }
    return $classes;
}
add_filter('body_class', 'add_role_class_to_body');

/* ============================================================================
   API-BASED USER LOGIN & ROLE MANAGEMENT
   ============================================================================ */

// Handle API login and create WordPress session
function handle_api_login() {
    // Check if user logged in via API
    if (!is_user_logged_in() && isset($_COOKIE['authToken'])) {
        $token = sanitize_text_field($_COOKIE['authToken']);
        
        // Verify token with backend API
        $response = wp_remote_get(API_BASE_URL . '/users/profile/', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $token
            )
        ));
        
        if (!is_wp_error($response) && wp_remote_retrieve_response_code($response) === 200) {
            $user_data = json_decode(wp_remote_retrieve_body($response), true);
            
            if ($user_data && isset($user_data['email'])) {
                // Create or get WordPress user
                $wp_user = get_user_by('email', $user_data['email']);
                
                if (!$wp_user) {
                    // Create new WordPress user
                    $username = sanitize_user($user_data['email']);
                    $user_id = wp_create_user($username, wp_generate_password(), $user_data['email']);
                    
                    if (!is_wp_error($user_id)) {
                        $wp_user = get_user_by('id', $user_id);
                        
                        // Set first and last name
                        if (isset($user_data['first_name'])) {
                            wp_update_user(array(
                                'ID' => $user_id,
                                'first_name' => $user_data['first_name'],
                                'last_name' => $user_data['last_name'] ?? ''
                            ));
                        }
                    }
                }
                
                if ($wp_user) {
                    // Determine role based on API response
                    $role = 'customer'; // default
                    
                    if (isset($user_data['restaurant'])) {
                        $role = 'restaurant_owner';
                    } elseif (isset($user_data['delivery_partner'])) {
                        $role = 'delivery_partner';
                    }
                    
                    // Update user role if different
                    $user_obj = new WP_User($wp_user->ID);
                    if (!in_array($role, $user_obj->roles)) {
                        $user_obj->set_role($role);
                    }
                    
                    // Log user in to WordPress
                    wp_set_current_user($wp_user->ID);
                    wp_set_auth_cookie($wp_user->ID, true);
                    do_action('wp_login', $wp_user->user_login, $wp_user);
                }
            }
        }
    }
}
add_action('init', 'handle_api_login', 1);

// Sync logout - clear both WordPress and API cookies
function handle_api_logout() {
    if (isset($_GET['action']) && $_GET['action'] === 'logout') {
        // Clear API token cookie
        setcookie('authToken', '', time() - 3600, '/');
        setcookie('access_token', '', time() - 3600, '/');
        
        // WordPress logout will happen automatically
    }
}
add_action('init', 'handle_api_logout', 0);

// Add user info to frontend for debugging
function expose_user_info() {
    if (is_user_logged_in()) {
        $user = wp_get_current_user();
        ?>
        <script>
            window.WP_USER = {
                id: <?php echo $user->ID; ?>,
                email: '<?php echo esc_js($user->user_email); ?>',
                role: '<?php echo esc_js($user->roles[0] ?? 'subscriber'); ?>',
                firstName: '<?php echo esc_js($user->first_name); ?>',
                lastName: '<?php echo esc_js($user->last_name); ?>'
            };
            console.log('✅ WordPress User:', window.WP_USER);
        </script>
        <?php
    }
}
add_action('wp_head', 'expose_user_info', 2);

?>
