---
name: jquery
description: Expert jQuery assistance covering DOM manipulation, AJAX, event delegation, and legacy web migration. Use when maintaining or refactoring classic JavaScript web applications.
---

# jQuery

jQuery v4.0 (2025) is a cleanup release, removing IE support and shrinking the file size. While not for new apps, it remains vital for legacy maintenance and WordPress.

## When to Use

- **Legacy Web Application Maintenance**: Maintaining and extending established web applications, themes, and portals.
- **WordPress & CMS Plugin Development**: Supporting traditional WordPress, Drupal, or Magento themes requiring jQuery.
- **Quick DOM Manipulation Scripts**: Adding simple animations, modal toggles, and AJAX calls to server-rendered pages.
- **Third-Party jQuery Plugin Integrations**: Utilizing established plugins (DataTables, Select2, Slick Carousel).

## Quick Start

```html
<!doctype html>
<html>
  <head>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  </head>
  <body>
    <button id="btn">Click Me</button>
    <div id="output"></div>

    <script>
      $(document).ready(function () {
        $("#btn").on("click", function () {
          $("#output").text("Button clicked!").fadeIn();
        });
      });
    </script>
  </body>
</html>
```

## Core Concepts

#DOM Traversal & Event Delegation

Handling events dynamically for current and future DOM nodes:

```javascript
$(document).ready(function () {
  // Event delegation on dynamic table rows
  $("#product-table").on("click", ".delete-btn", function (event) {
    event.preventDefault();
    const row = $(this).closest("tr");
    const productId = row.data("product-id");

    if (confirm("Delete this product?")) {
      $.ajax({
        url: `/api/products/${productId}`,
        method: "DELETE",
        success: function () {
          row.fadeOut(300, function () {
            $(this).remove();
          });
        },
        error: function (xhr, status, error) {
          alert("Failed to delete: " + error);
        },
      });
    }
  });
});
```

#AJAX Requests with Promises

Modern asynchronous requests using jQuery Deferred:

```javascript
function fetchUserData(userId) {
  return $.getJSON(`/api/v1/users/${userId}`)
    .then(function (user) {
      $("#profile-name").text(user.name);
      $("#profile-email").text(user.email);
      return user;
    })
    .catch(function (error) {
      console.error("Error fetching user data:", error);
      $("#profile-error").show().text("User could not be loaded.");
    });
}
```

#Writing a Custom jQuery Plugin

Encapsulating reusable UI behavior following standard plugin conventions:

```javascript
(function ($) {
  $.fn.characterCounter = function (options) {
    const settings = $.extend({ maxChars: 140, warningThreshold: 10 }, options);

    return this.each(function () {
      const $textarea = $(this);
      const $badge = $('<span class="char-counter badge"></span>').insertAfter(
        $textarea,
      );

      function update() {
        const remaining = settings.maxChars - $textarea.val().length;
        $badge.text(remaining + " remaining");
        $badge.toggleClass(
          "badge-warning",
          remaining <= settings.warningThreshold,
        );
      }

      $textarea.on("input keyup", update);
      update();
    });
  };
})(jQuery);
```

## Common Patterns

### Event Delegation for Dynamically Injected Elements

**Problem**: Click handlers do not fire on elements injected after initial `$(document).ready()`.

**Solution**:
Delegate events from a static parent container:

```javascript
// Delegate click event from persistent parent to dynamic child items
$("#items-container").on("click", ".delete-btn", function (e) {
  e.preventDefault();
  const itemId = $(this).data("id");
  $(this)
    .closest(".item-row")
    .fadeOut(300, function () {
      $(this).remove();
    });
});
```

## Best Practices (2026)

- **Do** always use event delegation (`$(parent).on('event', '.child', fn)`) for dynamically added DOM elements.
- **Do** cache jQuery selector lookups (`const $list = $('#list');`) rather than re-querying the DOM in loops.
- **Do** target jQuery 3.7+ or higher to ensure security patches and modern browser compatibility.
- **Do** migrate simple DOM tasks to native Vanilla JavaScript (`querySelector`, `fetch`, `classList`) where practical.
- **Don't** load full jQuery in greenfield projects if native browser APIs or modern micro-libraries suffice.
- **Don't** use synchronous AJAX (`async: false`); it freezes the browser UI thread.
- **Don't** inject untrusted user strings with `.html()`; use `.text()` to prevent XSS attacks.

## Troubleshooting

| Error                                           | Cause                                                                | Solution                                                                       |
| :---------------------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `Uncaught TypeError: $ is not a function`       | jQuery loaded after script, or running in `noConflict()` mode.       | Wrap script in `jQuery(function($) { ... })` or ensure jQuery CDN loads first. |
| `Event handler firing multiple times`           | Event listener bound repeatedly inside loop or multiple ready calls. | Call `$("#btn").off("click").on("click", ...)` to unbind duplicates.           |
| `Cross-Origin Request Blocked (CORS) in $.ajax` | Target API lacks CORS headers for cross-domain requests.             | Configure CORS headers on server or proxy requests via same origin.            |

## References

- [jQuery Documentation](https://jquery.com/)
