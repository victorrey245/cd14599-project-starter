# Udatracker Starter Code

## Reflection

### Design Trade-off

1. **Dictionary-Based Order Storage**: Orders are stored in-memory as dictionaries and returned by reference. We copy dictionaries in `InMemoryStorage` to prevent unintended mutations. This approach is simple and fast for small datasets but wouldn't scale for production. The alternative is using immutable data structures or ORM objects in a DB.

### Testing Insight

- **Test-Driven API Integration**: Writing API tests before implementing endpoints ensured the Flask routes handled all expected inputs and error cases (201 vs. 400 status codes, 404 for missing orders). This prevented common HTTP API mistakes like returning 500 when 404 is appropriate.

### Next-Step Improvement

- **DELETE Endpoint**: Add a `DELETE /api/orders/<order_id>` endpoint to remove orders. This would complete the full CRUD cycle and require implementing a `delete_order` method in both `OrderTracker` and storage layers.
