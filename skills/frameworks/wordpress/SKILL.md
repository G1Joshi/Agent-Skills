---
name: wordpress
description: Expert WordPress assistance covering themes, plugins, REST API, Gutenberg blocks, and WP_Query. Use when developing custom WordPress plugins, themes, or headless CMS backends.
---

# WordPress

WordPress 6.6 (2025) continues the **Full Site Editing (FSE)** revolution. Everything is a block.

## When to Use

- **Modern Content Management Platforms**: Powering blogs, news publications, and enterprise corporate websites.
- **Gutenberg Custom Block Development**: Developing custom editorial blocks using `@wordpress/scripts` and React.
- **Headless WordPress**: Using WordPress as a content backend decoupled from Next.js, Nuxt, or Astro frontends.
- **Modern PHP 8.2+ Plugins & Themes**: Writing object-oriented, PSR-compliant WordPress code.

## Quick Start

```php
<?php
/**
 * Plugin Name: Custom API Endpoint
 * Description: Registers a custom WordPress REST API endpoint.
 * Version: 1.0.0
 */

add_action('rest_api_init', function () {
    register_rest_route('custom/v1', '/latest-posts', [
        'methods' => 'GET',
        'callback' => function () {
            $posts = get_posts(['numberposts' => 5]);
            return new WP_REST_Response($posts, 200);
        },
        'permission_callback' => '__return_true'
    ]);
});
```

## Core Concepts

#Gutenberg Custom Block with @wordpress/scripts

Building editorial blocks using React and block.json metadata:

```json
// block.json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "custom/hero-banner",
  "version": "1.0.0",
  "title": "Hero Banner",
  "category": "design",
  "icon": "superhero",
  "attributes": {
    "heading": { "type": "string", "default": "Default Hero" }
  },
  "editorScript": "file:./index.js",
  "render": "file:./render.php"
}
```

```javascript
// src/index.js
import { registerBlockType } from "@wordpress/blocks";
import { RichText, useBlockProps } from "@wordpress/block-editor";

registerBlockType("custom/hero-banner", {
  edit: ({ attributes, setAttributes }) => {
    const blockProps = useBlockProps({ className: "custom-hero-editor" });
    return (
      <div {...blockProps}>
        <RichText
          tagName="h1"
          value={attributes.heading}
          onChange={(val) => setAttributes({ heading: val })}
          placeholder="Enter hero title..."
        />
      </div>
    );
  },
  save: () => null, // Dynamic rendering handled by render.php
});
```

#Type-Safe WP REST API Endpoint Registration

Exposing custom REST endpoints with permission callbacks:

```php
namespace App\Rest;

add_action('rest_api_init', function () {
    register_rest_route('app/v1', '/metrics', [
        'methods' => 'GET',
        'callback' => function (\WP_REST_Request $request) {
            return new \WP_REST_Response([
                'posts_count' => wp_count_posts()->publish,
                'status' => 'healthy',
                'timestamp' => time(),
            ], 200);
        },
        'permission_callback' => function () {
            return current_user_can('edit_posts');
        },
    ]);
});
```

#Secure Database Queries with $wpdb

Preventing SQL injection using prepared statements:

```php
function get_verified_order(int $order_id): ?object {
    global $wpdb;

    $table_name = $wpdb->prefix . 'custom_orders';
    $query = $wpdb->prepare(
        "SELECT id, total_amount, customer_email FROM {$table_name} WHERE id = %d AND status = %s",
        $order_id,
        'completed'
    );

    return $wpdb->get_row($query);
}
```

## Common Patterns

### Efficient WP_Query with Custom Meta and Pagination

**Problem**: Complex meta queries cause high server load and unindexed table scans on `wp_postmeta`.

**Solution**:
Use indexed fields and limit fields returned:

```php
$args = [
    'post_type'      => 'product',
    'post_status'    => 'publish',
    'posts_per_page' => 12,
    'paged'          => get_query_var('paged') ? get_query_var('paged') : 1,
    'meta_query'     => [
        [
            'key'     => 'in_stock',
            'value'   => '1',
            'compare' => '='
        ]
    ],
    'no_found_rows'  => false, // Set true if pagination is not needed
];

$query = new WP_Query($args);
```

## Best Practices (2026)

- **Do** target WordPress 6.x+ with Block API v3 and Full Site Editing (FSE) block themes.
- **Do** always use `permission_callback` in `register_rest_route()` to prevent unauthorized API access.
- **Do** use `$wpdb->prepare()` for all custom SQL statements to eliminate SQL injection vulnerabilities.
- **Do** sanitize incoming inputs (`sanitize_text_field()`) and escape outgoing outputs (`esc_html()`, `esc_url()`).
- **Don't** write raw SQL queries when native `WP_Query` or `get_posts()` can fulfill the requirement.
- **Don't** build classic PHP widget-based themes for new projects; adopt Block Themes and Gutenberg.
- **Don't** commit secrets, database credentials, or security salts to version control.

## Troubleshooting

| Error                          | Cause                                                              | Solution                                                                      |
| :----------------------------- | :----------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `Headers already sent error`   | Whitespace or output before `<?php` tag or inside `functions.php`. | Check for empty lines before opening `<?php` or remove trailing `?>`.         |
| `REST API 403 Forbidden`       | Nonce verification failed or `permission_callback` missing.        | Provide valid `X-WP-Nonce` header or define appropriate permission callback.  |
| `White Screen of Death (WSOD)` | Fatal PHP error with `WP_DEBUG` disabled.                          | Enable `define('WP_DEBUG', true);` in `wp-config.php` to inspect stack trace. |

## References

- [WordPress Developer](https://developer.wordpress.org/)
