# Data Models

### Group 50 - Sprint 1

_Monetary values are stored as int for binary precision._

##### Product

| name               | type                        |
| ------------------ | --------------------------- |
| id                 | int                         |
| title              | string                      |
| description        | string                      |
| price              | int                         |
| last_modified_date | DateTime                    |
| owner_email        | string                      |
| quantity           | int                         |
| review             | int list (**Review** _ids_) |

##### Review

| name   | type                 |
| ------ | -------------------- |
| id     | int                  |
| score  | int                  |
| review | string               |
| buyer  | int (**Buyer** _id_) |

##### User

| name             | type                             |
| ---------------- | -------------------------------- |
| id               | int                              |
| user_name        | string                           |
| password         | string                           |
| email            | string                           |
| balance          | int                              |
| shipping_address | string                           |
| postal_code      | string                           |
| order_history    | int list (**Transaction** _ids_) |

##### Buyer _extends_ User

| name | type                             |
| ---- | -------------------------------- |
| cart | int list (**Transaction** _ids_) |

##### Seller _extends_ User

| name     | type                         |
| -------- | ---------------------------- |
| products | int list (**Product** _ids_) |

##### Transaction

| name        | type                   |
| ----------- | ---------------------- |
| id          | int                    |
| total_price | int                    |
| date        | DateTime               |
| buyer       | int (**Buyer** _id_)   |
| seller      | int (**Seller** _id_)  |
| product_id  | int (**Product** _id_) |
| quantity    | int                    |
| purchased   | boolean                |
| delivered   | boolean                |
