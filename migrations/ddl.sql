-- Таблица для хранения информации о регионах
CREATE TABLE regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(100)
);

COMMENT ON TABLE regions IS 'Информация о регионах';

COMMENT ON COLUMN regions.region_id IS 'Уникальный идентификатор региона';
COMMENT ON COLUMN regions.region_name IS 'Название региона';

-- Таблица для хранения данных о спортивных школах
CREATE TABLE sport_schools (
    school_id SERIAL PRIMARY KEY,
    school_name VARCHAR(256),
    school_role VARCHAR(256),
    user_password VARCHAR(256),
    region_id INT,  -- Внешний ключ на таблицу regions
    FOREIGN KEY (region_id) REFERENCES regions(region_id) ON DELETE CASCADE
);

COMMENT ON TABLE sport_schools IS 'Данные о спортивных школах';

COMMENT ON COLUMN sport_schools.school_id IS 'Уникальный идентификатор школы';
COMMENT ON COLUMN sport_schools.school_name IS 'Название спортивной школы';
COMMENT ON COLUMN sport_schools.school_role IS 'Роль школы (например, Chad/no chad)';
COMMENT ON COLUMN sport_schools.user_password IS 'Роль школы (например, Chad/no chad)';
COMMENT ON COLUMN sport_schools.region_id IS 'Регион, в котором находится школа (внешний ключ на таблицу regions)';

-- Таблица для хранения информации о производителях лодок
CREATE TABLE boat_firms (
    firm_id SERIAL PRIMARY KEY,
    firm_name VARCHAR(256),
    country VARCHAR(100)
);

COMMENT ON TABLE boat_firms IS 'Информация о производителях лодок';

COMMENT ON COLUMN boat_firms.firm_id IS 'Уникальный идентификатор фирмы';
COMMENT ON COLUMN boat_firms.firm_name IS 'Название фирмы';
COMMENT ON COLUMN boat_firms.country IS 'Страна производителя';

-- Таблица для хранения состава каждой поставки
CREATE TABLE boat_specifications (
    spec_id SERIAL PRIMARY KEY,
    class VARCHAR(10),
    weight NUMERIC,
    user_weight VARCHAR(10)
);

COMMENT ON TABLE boat_specifications IS 'Состав поставки продуктов';

COMMENT ON COLUMN boat_specifications.spec_id IS 'Уникальный идентификатор строки поставки';
COMMENT ON COLUMN boat_specifications.class IS 'Класс лодки';
COMMENT ON COLUMN boat_specifications.weight IS 'Вес лодки';
COMMENT ON COLUMN boat_specifications.user_weight IS 'Вес пользователя';

-- Таблица для хранения основной информации о лодках
CREATE TABLE boats (
    boat_id SERIAL PRIMARY KEY,
    firm_id INT,
    spec_id INT,
    price INT,
    purchased BOOLEAN DEFAULT FALSE,  -- Флаг для отслеживания, была ли лодка куплена
    FOREIGN KEY (firm_id) REFERENCES boat_firms(firm_id) ON DELETE CASCADE,
    FOREIGN KEY (spec_id) REFERENCES boat_specifications(spec_id) ON DELETE CASCADE
);

COMMENT ON TABLE boats IS 'Основная информация о лодках и их стоимости';

COMMENT ON COLUMN boats.boat_id IS 'Уникальный идентификатор лодки';
COMMENT ON COLUMN boats.firm_id IS 'Идентификатор фирмы, производящей лодку';
COMMENT ON COLUMN boats.spec_id IS 'Идентификатор спецификации лодки';
COMMENT ON COLUMN boats.price IS 'Цена лодки';
COMMENT ON COLUMN boats.purchased IS 'Флаг, указывающий, была ли лодка куплена';

-- Таблица для хранения информации о сделках
CREATE TABLE deals (
    deal_id SERIAL PRIMARY KEY,
    school_id INT REFERENCES sport_schools(school_id) ON DELETE CASCADE,
    boat_id INT REFERENCES boats(boat_id) ON DELETE CASCADE,
    deal_time DATE NOT NULL
);

COMMENT ON TABLE deals IS 'Информация о сделках, включающих покупку лодок спортивными школами';

COMMENT ON COLUMN deals.deal_id IS 'Уникальный идентификатор сделки';
COMMENT ON COLUMN deals.school_id IS 'Идентификатор спортивной школы, совершившей покупку';
COMMENT ON COLUMN deals.boat_id IS 'Идентификатор лодки, которая была куплена';
COMMENT ON COLUMN deals.deal_time IS 'Дата, когда была совершена сделка';

-- Таблица для хранения информации о эксплуатации лодок
CREATE TABLE boat_explotation (
    exp_id SERIAL PRIMARY KEY,
    school_id INT REFERENCES sport_schools(school_id) ON DELETE CASCADE,
    boat_id INT REFERENCES boats(boat_id) ON DELETE CASCADE,  -- Ссылка на лодку из таблицы boats
    begin_date DATE,  -- Дата начала эксплуатации лодки
    end_date DATE,    -- Дата окончания эксплуатации лодки (NULL, если лодка всё ещё используется)
    repaired BOOLEAN  -- Флаг, был ли проведён ремонт
);

COMMENT ON TABLE boat_explotation IS 'Информация о эксплуатации лодок в спортивных школах, включая даты использования и ремонт';
COMMENT ON COLUMN boat_explotation.exp_id IS 'Уникальный идентификатор записи эксплуатации';
COMMENT ON COLUMN boat_explotation.school_id IS 'Идентификатор спортивной школы, использующей лодку';
COMMENT ON COLUMN boat_explotation.boat_id IS 'Идентификатор лодки, которая находится в эксплуатации';
COMMENT ON COLUMN boat_explotation.begin_date IS 'Дата начала эксплуатации лодки';
COMMENT ON COLUMN boat_explotation.end_date IS 'Дата окончания эксплуатации лодки (NULL, если лодка всё ещё используется)';
COMMENT ON COLUMN boat_explotation.repaired IS 'Флаг, указывающий, была ли лодка отремонтирована в процессе эксплуатации';

-- Обновление с проверкой, что только лодки с purchased = FALSE могут быть использованы для эксплуатации
-- Это можно выполнить с помощью триггера.
CREATE OR REPLACE FUNCTION check_boat_exploitation()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка, что лодка с purchased = FALSE
    IF (SELECT purchased FROM boats WHERE boat_id = NEW.boat_id) = TRUE THEN
        RAISE EXCEPTION 'Лодка с boat_id % уже куплена, её нельзя использовать для эксплуатации', NEW.boat_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера для проверки перед вставкой
CREATE TRIGGER before_insert_boat_exploitation
BEFORE INSERT ON boat_explotation
FOR EACH ROW
EXECUTE FUNCTION check_boat_exploitation();