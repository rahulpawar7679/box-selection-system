# AI_USAGE.md

### 1. AI Tool(s) Used
- Google Gemini

### 2. Prompts Given
- "Given an ecommerce box selection system where items have length, width, height, and weight, and boxes have internal dimensions, weight capacity, and cost, provide a Django service and model architecture to find the optimal box."
- "Write automated Django unit test cases covering 3D rotation checks, weight capacity thresholds, empty items, and API payload edge cases."

### 3. Output Accepted
- Sorting dimensions on both the item and box (`sorted(item_dims) <= sorted(box_dims)`) to handle 3D spatial orientations without third-party packing dependencies.
- Model architecture with explicit `DecimalField` for currency and weights.
- Separation of business logic into a standalone service (`BoxSelectionService`) rather than embedding logic directly in views.

### 4. Output Rejected or Modified
- **Rejected Complex External 3D Packing Libraries**: The initial AI suggestion proposed external C-based bin packing packages (`py3dbp`). Modified this to use clean, pure Python dimension-boundary checks to keep setup lightweight.
- **Refined Weight Aggregation**: AI initially evaluated item weights individually against `max_weight`. Updated this logic to calculate total order weight (accounting for individual item quantities).
- **Added Input Validation**: Enforced strict boundary conditions to reject non-positive values, zeros, and malformed JSON payloads.

### 5. Mistakes Identified
- Initial AI snippet used `FloatField` for box costs and weights, which introduces precision issues. This was corrected to use `DecimalField`.
- The first AI iteration checked single item bounds but failed to unpack multiplied item quantities when summing total weight and volume.

### 6. Verification Steps
- Ran schema migrations with SQLite backend.
- Executed `python manage.py test packaging -v 2` validating 100% test pass rate across unit logic and API endpoints.
- Performed endpoint testing using POST requests with valid and invalid payloads.