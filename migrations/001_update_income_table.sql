-- Crea la tabla incomes si todavía no existe. Mantén este archivo sincronizado con app/models/income_model.py
CREATE TABLE IF NOT EXISTS incomes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    salary DECIMAL(12,2) NOT NULL,
    bonus DECIMAL(12,2) NULL DEFAULT 0,
    other_income DECIMAL(12,2) NULL DEFAULT 0,
    total_income DECIMAL(12,2) NOT NULL,
    status ENUM('planned','posted') NOT NULL DEFAULT 'posted',
    income_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_incomes_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
