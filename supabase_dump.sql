-- ============================================
-- AssetTrack Pro - Supabase/PostgreSQL Comprehensive Dump
-- ============================================

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables (ordered by dependency)
DROP TABLE IF EXISTS asset_maintenance_logs;
DROP TABLE IF EXISTS asset_assignments;
DROP TABLE IF EXISTS assets;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS hr_admins;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

-- 1. Roles Table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    permissions JSONB DEFAULT '[]'::jsonb
);

-- 2. Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id)
);

-- 3. Departments Table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    department_code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Employees Table
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    department_id INTEGER REFERENCES departments(department_id),
    designation VARCHAR(100),
    employment_status VARCHAR(50) DEFAULT 'ACTIVE',
    date_of_joining DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. HR Admins Table
CREATE TABLE hr_admins (
    hr_admin_id SERIAL PRIMARY KEY,
    admin_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    role VARCHAR(50) DEFAULT 'HR_ADMIN',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Assets Table
CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    asset_code VARCHAR(100) UNIQUE NOT NULL,
    asset_name VARCHAR(150) NOT NULL,
    asset_category VARCHAR(100),
    purchase_date DATE,
    purchase_cost NUMERIC(12,2),
    asset_status VARCHAR(50) DEFAULT 'AVAILABLE', -- 'AVAILABLE', 'ASSIGNED', 'MAINTENANCE'
    asset_condition VARCHAR(50) DEFAULT 'GOOD',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Asset Assignments Table
CREATE TABLE asset_assignments (
    assignment_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    assigned_by_hr_id INTEGER REFERENCES hr_admins(hr_admin_id),
    assignment_date DATE NOT NULL,
    return_date DATE,
    assignment_status VARCHAR(50) DEFAULT 'ASSIGNED',
    remarks TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 8. Asset Maintenance Logs
CREATE TABLE asset_maintenance_logs (
    maintenance_id SERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL REFERENCES assets(asset_id),
    maintenance_type VARCHAR(100), -- E.g., 'ASSIGNED', 'RETURNED', 'MAINTENANCE'
    maintenance_description TEXT,
    maintenance_cost NUMERIC(12,2),
    maintenance_date DATE,
    performed_by VARCHAR(150),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_employee_code ON users(employee_code);
CREATE INDEX idx_employees_department_id ON employees(department_id);
CREATE INDEX idx_asset_assignments_employee_id ON asset_assignments(employee_id);
CREATE INDEX idx_asset_assignments_asset_id ON asset_assignments(asset_id);
CREATE INDEX idx_assets_asset_status ON assets(asset_status);

-- Seed Initial Data
INSERT INTO roles (name, permissions) VALUES
('Superadmin', '["manage:super", "delete:asset", "view:inventory", "manage:users"]'::jsonb),
('Admin', '["delete:asset", "view:inventory", "manage:users"]'::jsonb),
('Employee', '["view:my_gear"]'::jsonb);

-- Need careful password hashing for users - normally handled by setup endpoint.
-- Seeding default roles is easy; users require password hashing which is done via app code.

INSERT INTO departments (department_name, department_code) VALUES
('Human Resources', 'HR'),
('Engineering', 'ENG'),
('Finance', 'FIN'),
('Operations', 'OPS');

INSERT INTO hr_admins (admin_name, email, phone_number) VALUES
('System Master', 'admin@company.com', '9999999999');

INSERT INTO assets (asset_code, asset_name, asset_category, purchase_date, purchase_cost)
VALUES
('AST001', 'MacBook Pro 14"', 'Electronics', CURRENT_DATE, 150000.00),
('AST002', 'Dell UltraSharp 27"', 'Electronics', CURRENT_DATE, 35000.00),
('AST003', 'ErgoChair Pro', 'Furniture', CURRENT_DATE, 12000.00);
