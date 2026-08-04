-- =============================
-- DATABASE: AI Data Analyst Demo
-- =============================

-- Drop tables if they exist
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS employees;

-- =============================
-- TABLE: customers
-- =============================
CREATE TABLE customers (
id SERIAL PRIMARY KEY,
name VARCHAR(100),
email VARCHAR(100),
city VARCHAR(50),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================
-- TABLE: employees
-- =============================
CREATE TABLE employees (
id SERIAL PRIMARY KEY,
name VARCHAR(100),
role VARCHAR(50),
salary INT,
city VARCHAR(50)
);

-- =============================
-- TABLE: products
-- =============================
CREATE TABLE products (
id SERIAL PRIMARY KEY,
name VARCHAR(100),
category VARCHAR(50),
price DECIMAL(10,2),
stock INT
);

-- =============================
-- TABLE: orders
-- =============================
CREATE TABLE orders (
id SERIAL PRIMARY KEY,
customer_id INT REFERENCES customers(id),
product_id INT REFERENCES products(id),
quantity INT,
total_price DECIMAL(10,2),
order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================
-- INSERT DATA: customers
-- =============================
INSERT INTO customers (name, email, city) VALUES
('Ali Khan', '[ali@gmail.com](mailto:ali@gmail.com)', 'Karachi'),
('Sara Ahmed', '[sara@gmail.com](mailto:sara@gmail.com)', 'Lahore'),
('Usman Tariq', '[usman@gmail.com](mailto:usman@gmail.com)', 'Islamabad'),
('Ayesha Noor', '[ayesha@gmail.com](mailto:ayesha@gmail.com)', 'Karachi'),
('Bilal Hassan', '[bilal@gmail.com](mailto:bilal@gmail.com)', 'Lahore');

-- =============================
-- INSERT DATA: employees
-- =============================
INSERT INTO employees (name, role, salary, city) VALUES
('Hamza Ali', 'Manager', 120000, 'Karachi'),
('Zain Malik', 'Developer', 90000, 'Lahore'),
('Hira Khan', 'Analyst', 80000, 'Islamabad'),
('Ahmed Raza', 'Developer', 95000, 'Karachi'),
('Fatima Noor', 'HR', 70000, 'Lahore');

-- =============================
-- INSERT DATA: products
-- =============================
INSERT INTO products (name, category, price, stock) VALUES
('Laptop', 'Electronics', 150000, 10),
('Phone', 'Electronics', 80000, 25),
('Headphones', 'Accessories', 5000, 50),
('Keyboard', 'Accessories', 3000, 40),
('Mouse', 'Accessories', 1500, 60);

-- =============================
-- INSERT DATA: orders
-- =============================
INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES
(1, 1, 1, 150000),
(2, 2, 2, 160000),
(3, 3, 3, 15000),
(1, 4, 2, 6000),
(4, 5, 5, 7500),
(5, 1, 1, 150000),
(2, 3, 2, 10000);

-- =============================
-- SAMPLE QUERIES (FOR TESTING)
-- =============================

-- 1. Get all customers
-- SELECT * FROM customers;

-- 2. Total sales
-- SELECT SUM(total_price) FROM orders;

-- 3. Top selling products
-- SELECT p.name, SUM(o.quantity) as total_sold
-- FROM orders o
-- JOIN products p ON o.product_id = p.id
-- GROUP BY p.name
-- ORDER BY total_sold DESC;

-- 4. Customers from Karachi
-- SELECT * FROM customers WHERE city = 'Karachi';

-- 5. Employee salary ranking
-- SELECT name, salary FROM employees ORDER BY salary DESC;
