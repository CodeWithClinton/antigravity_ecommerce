<!-- API_DOCS_START -->

### `POST` /api/auth/register/

**Register User**

Create a new user account.

- **View:** `register_user` | **Name:** `register`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | `string (email)` | **Yes** | - |
| `username` | `string` | **Yes** | - |
| `password` | `string` | **Yes** | - |

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `email` | `string (email)` | - |
| `username` | `string` | - |
| `is_active` | `boolean` | *(Read-only)* |
| `date_joined` | `datetime` | *(Read-only)* |

### `POST` /api/auth/login/

**User Login**

Authenticate a user and return JWT tokens along with user data.

- **View:** `login_user` | **Name:** `login`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `email` | `string (email)` | **Yes** | - |
| `password` | `string` | **Yes** | - |

### `GET` /api/categories/

**List Categories**

Get a list of all active categories.

- **View:** `category_list` | **Name:** `category-list`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `name` | `string` | - |
| `slug` | `string (slug)` | - |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `total_products` | `SerializerMethodField` | *(Read-only)* |

### `GET` /api/categories/<int:pk>/

**Category Detail**

Get details of a specific category.

- **View:** `category_detail` | **Name:** `category-detail`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `name` | `string` | - |
| `slug` | `string (slug)` | - |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `total_products` | `SerializerMethodField` | *(Read-only)* |

### `GET` /api/products/

**List Products**

Get a paginated list of active products with filtering and sorting.

- **View:** `product_list` | **Name:** `product-list`

**Query Parameters**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `search` | `string` | No | Search by title |
| `category` | `string` | No | Filter by category slug(s) |
| `min_price` | `string` | No | Minimum price |
| `max_price` | `string` | No | Maximum price |
| `sort` | `string` | No | Sort by price-asc, price-desc, or newest |

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `title` | `string` | - |
| `description` | `string` | - |
| `price` | `decimal` | - |
| `stock_quantity` | `integer` | - |
| `category` | `PrimaryKeyRelatedField` | - |
| `category_name` | `ReadOnlyField` | *(Read-only)* |
| `category_slug` | `ReadOnlyField` | *(Read-only)* |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `created_at` | `datetime` | *(Read-only)* |

### `GET` /api/products/featured/

**Featured Products**

Get a list of featured products.

- **View:** `featured_products` | **Name:** `featured-products`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `title` | `string` | - |
| `description` | `string` | - |
| `price` | `decimal` | - |
| `stock_quantity` | `integer` | - |
| `category` | `PrimaryKeyRelatedField` | - |
| `category_name` | `ReadOnlyField` | *(Read-only)* |
| `category_slug` | `ReadOnlyField` | *(Read-only)* |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `created_at` | `datetime` | *(Read-only)* |

### `GET` /api/products/latest/

**Latest Products**

Get the most recently added products.

- **View:** `latest_products` | **Name:** `latest-products`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `title` | `string` | - |
| `description` | `string` | - |
| `price` | `decimal` | - |
| `stock_quantity` | `integer` | - |
| `category` | `PrimaryKeyRelatedField` | - |
| `category_name` | `ReadOnlyField` | *(Read-only)* |
| `category_slug` | `ReadOnlyField` | *(Read-only)* |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `created_at` | `datetime` | *(Read-only)* |

### `GET` /api/products/search/

**Search Products**

Search products by title.

- **View:** `product_search` | **Name:** `product-search`

**Query Parameters**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `q` | `string` | No | Search query |

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `title` | `string` | - |
| `description` | `string` | - |
| `price` | `decimal` | - |
| `stock_quantity` | `integer` | - |
| `category` | `PrimaryKeyRelatedField` | - |
| `category_name` | `ReadOnlyField` | *(Read-only)* |
| `category_slug` | `ReadOnlyField` | *(Read-only)* |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `created_at` | `datetime` | *(Read-only)* |

### `GET` /api/products/<int:pk>/

**Product Detail**

Get full details of a specific product.

- **View:** `product_detail` | **Name:** `product-detail`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `title` | `string` | - |
| `description` | `string` | - |
| `price` | `decimal` | - |
| `stock_quantity` | `integer` | - |
| `category` | `PrimaryKeyRelatedField` | - |
| `category_name` | `ReadOnlyField` | *(Read-only)* |
| `category_slug` | `ReadOnlyField` | *(Read-only)* |
| `image` | `ImageField` | - |
| `is_active` | `boolean` | - |
| `created_at` | `datetime` | *(Read-only)* |

### `GET` /api/cart/

**Get Cart**

Retrieve the authenticated user's cart.

- **View:** `get_cart` | **Name:** `get-cart`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |
| `total_amount` | `SerializerMethodField` | *(Read-only)* |

### `POST` /api/cart/add/

**Add to Cart**

Add a product to the user's cart.

- **View:** `add_to_cart` | **Name:** `add-to-cart`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `product_id` | `integer` | **Yes** | - |
| `quantity` | `integer` | No | - |

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |
| `total_amount` | `SerializerMethodField` | *(Read-only)* |

### `POST` /api/cart/update/

**Update Cart Item**

Update the quantity of an item in the cart.

- **View:** `update_cart_item` | **Name:** `update-cart-item`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `item_id` | `integer` | **Yes** | - |
| `quantity` | `integer` | **Yes** | - |

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |
| `total_amount` | `SerializerMethodField` | *(Read-only)* |

### `POST` /api/cart/remove/

**Remove from Cart**

Remove an item from the cart.

- **View:** `remove_from_cart` | **Name:** `remove-from-cart`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `item_id` | `integer` | **Yes** | - |

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |
| `total_amount` | `SerializerMethodField` | *(Read-only)* |

### `GET` /api/orders/

**List Orders**

Get a list of all orders for the authenticated user.

- **View:** `order_list` | **Name:** `order-list`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `total_amount` | `decimal` | *(Read-only)* |
| `status` | `string/integer (choice)` | *(Read-only)* |
| `payment_status` | `string/integer (choice)` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |

### `POST` /api/orders/create/

**Create Order**

Create a new order from items in the authenticated user's cart.

- **View:** `create_order` | **Name:** `create-order`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `total_amount` | `decimal` | *(Read-only)* |
| `status` | `string/integer (choice)` | *(Read-only)* |
| `payment_status` | `string/integer (choice)` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |

### `GET` /api/orders/<int:pk>/

**Order Detail**

Get details of a specific order.

- **View:** `order_detail` | **Name:** `order-detail`

**Responses**

##### `200`

| Field | Type | Description |
| --- | --- | --- |
| `id` | `BigIntegerField` | *(Read-only)* |
| `user` | `PrimaryKeyRelatedField` | *(Read-only)* |
| `total_amount` | `decimal` | *(Read-only)* |
| `status` | `string/integer (choice)` | *(Read-only)* |
| `payment_status` | `string/integer (choice)` | *(Read-only)* |
| `created_at` | `datetime` | *(Read-only)* |
| `items` | `ListSerializer` | *(Read-only)* |

### `POST` /api/payments/initiate/

**Initiate Payment**

Initialize a Paystack transaction for an order.

- **View:** `initiate_payment` | **Name:** `initiate-payment`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `order_id` | `integer` | **Yes** | - |

### `POST` /api/payments/verify/

**Verify Payment**

Verify a Paystack transaction status and update order status.

- **View:** `verify_payment` | **Name:** `verify-payment`

**Request Body**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `reference` | `string` | **Yes** | - |

<!-- API_DOCS_END -->
