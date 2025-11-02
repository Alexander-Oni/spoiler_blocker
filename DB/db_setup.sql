CREATE TABLE Users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  subscription_type VARCHAR(20) DEFAULT 'free'
);

CREATE TABLE Categories (
  category_id SERIAL PRIMARY KEY,
  category_name VARCHAR(100) NOT NULL,
  description TEXT,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE Keywords (
  keyword_id SERIAL PRIMARY KEY,
  keyword_text VARCHAR(200) NOT NULL,
  category_id INTEGER REFERENCES Categories(category_id),
  severity_level VARCHAR(20) DEFAULT 'medium',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE User_Filters (
  filter_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES Users(user_id),
  keyword_id INTEGER REFERENCES Keywords(keyword_id),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Blocked_Content_Log (
  log_id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES Users(user_id),
  keyword_id INTEGER REFERENCES Keywords(keyword_id),
  url VARCHAR(500),
  blocked_content TEXT,
  blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Начальные данные для тестирования
INSERT INTO Categories (category_name, description) VALUES
('Фильмы', 'Спойлеры к фильмам'),
('Сериалы', 'Спойлеры к сериалам'), 
('Книги', 'Спойлеры к книгам'),
('Игры', 'Спойлеры к видеоиграм');

INSERT INTO Keywords (keyword_text, category_id, severity_level) VALUES
('Игра престолов финал', 2, 'high'),
('Смерть Тони Старка', 1, 'high'),
('Сюжет Дюны', 3, 'medium');

INSERT INTO Users (username, email, subscription_type) VALUES
('test_user', 'test@example.com', 'free'),
('admin', 'admin@example.com', 'premium');

SELECT 'База данных SpoilerBlocker создана успешно!' as status;
        