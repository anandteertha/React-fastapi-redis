-- NutriBite Database Schema
-- BCNF Normalized Schema
-- MySQL 8.0+

CREATE DATABASE IF NOT EXISTS nutribite CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nutribite;

-- Users table (BCNF normalized)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    age INT,
    gender VARCHAR(20),
    height_cm INT,
    weight_kg INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Foods catalog table (BCNF normalized)
CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    calories_per_100g DECIMAL(10, 2) NOT NULL,
    protein_per_100g DECIMAL(10, 2) NOT NULL,
    carbs_per_100g DECIMAL(10, 2) NOT NULL,
    fats_per_100g DECIMAL(10, 2) NOT NULL,
    fiber_per_100g DECIMAL(10, 2) DEFAULT 0.00,
    sugar_per_100g DECIMAL(10, 2) DEFAULT 0.00,
    sodium_per_100g DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Food items table (user's customized food entries)
CREATE TABLE IF NOT EXISTS food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity_g DECIMAL(10, 2) NOT NULL,
    custom_name VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_food_id (food_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Meals table (BCNF normalized)
CREATE TABLE IF NOT EXISTS meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
    meal_date DATETIME NOT NULL,
    notes VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_meal_date (meal_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Meal-Food junction table (BCNF normalized)
CREATE TABLE IF NOT EXISTS meal_foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    meal_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity_g DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_meal_id (meal_id),
    INDEX idx_food_id (food_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- User preferences table (BCNF normalized)
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    target_calories DECIMAL(10, 2),
    target_protein DECIMAL(10, 2),
    target_carbs DECIMAL(10, 2),
    target_fats DECIMAL(10, 2),
    preferred_meal_times VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dietary restrictions table (BCNF normalized)
CREATE TABLE IF NOT EXISTS dietary_restrictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    preference_id INT NOT NULL,
    restriction_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) DEFAULT 'moderate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (preference_id) REFERENCES user_preferences(id) ON DELETE CASCADE,
    INDEX idx_preference_id (preference_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Goals table (BCNF normalized)
CREATE TABLE IF NOT EXISTS goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    goal_type ENUM('weight_loss', 'weight_gain', 'maintenance', 'muscle_gain', 'general_health') NOT NULL,
    target_weight_kg DECIMAL(10, 2),
    current_weight_kg DECIMAL(10, 2),
    target_date DATETIME,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Daily reports table (BCNF normalized)
CREATE TABLE IF NOT EXISTS daily_reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    report_date DATETIME NOT NULL,
    total_calories DECIMAL(10, 2) NOT NULL,
    total_protein DECIMAL(10, 2) NOT NULL,
    total_carbs DECIMAL(10, 2) NOT NULL,
    total_fats DECIMAL(10, 2) NOT NULL,
    total_fiber DECIMAL(10, 2) DEFAULT 0.00,
    total_sugar DECIMAL(10, 2) DEFAULT 0.00,
    total_sodium DECIMAL(10, 2) DEFAULT 0.00,
    analysis TEXT,
    recommendations TEXT,
    motivation_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_report_date (report_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Sample data for testing
INSERT INTO foods (name, description, calories_per_100g, protein_per_100g, carbs_per_100g, fats_per_100g, fiber_per_100g, sugar_per_100g, sodium_per_100g) VALUES
('Chicken Breast', 'Lean chicken breast', 165.0, 31.0, 0.0, 3.6, 0.0, 0.0, 74.0),
('Brown Rice', 'Cooked brown rice', 111.0, 2.6, 23.0, 0.9, 1.8, 0.4, 5.0),
('Broccoli', 'Steamed broccoli', 35.0, 2.8, 7.0, 0.4, 2.6, 1.5, 33.0),
('Salmon', 'Atlantic salmon', 208.0, 20.0, 0.0, 12.0, 0.0, 0.0, 44.0),
('Sweet Potato', 'Baked sweet potato', 90.0, 2.0, 21.0, 0.2, 3.3, 4.2, 54.0),
('Greek Yogurt', 'Plain Greek yogurt', 59.0, 10.0, 3.6, 0.4, 0.0, 3.6, 36.0),
('Oatmeal', 'Cooked oatmeal', 68.0, 2.4, 12.0, 1.4, 1.7, 0.5, 5.0),
('Eggs', 'Large whole eggs', 155.0, 13.0, 1.1, 11.0, 0.0, 1.1, 124.0);

