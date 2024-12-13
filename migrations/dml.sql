
-- Вставка данных в таблицу regions
INSERT INTO
    regions (region_name)
VALUES
    ('Москва'),
    ('Санкт-Петербург'),
    ('Калужская область'),
    ('Липецкая область'),
    ('Ростовская область'),
    ('Нижегородская область'),
    ('Саратовская область'),
    ('Челябинская область'),
    ('Краснодарский край'),
    ('Томская область'),
    ('Республика Крым'),
    ('Республика Карелия'),
    ('Республика Татарстан');

INSERT INTO
    sport_schools (school_name, school_role, user_password, region_id)
VALUES
    ('admin', 'admin', '$2b$12$iD5un9xBRjxTC6Dn4DAJD.ws5Y1GbFjD9i2n35M7c1cao0HUKPWMe', 1);

INSERT INTO
    boat_firms (firm_name, country)
VALUES
    (
        'Filippi',
        'Italy'
    ),
    (
        'Empacher',
        'Germany'
    ),
    (
        'Swift Racing',
        'China'
    ),
    (
        'Wintech racing',
        'China'
    ),
    (
        'TMK',
        'Russia'
    ),
    (
        'Nowing',
        'Russia'
    );

INSERT INTO
    boat_specifications (class, weight, user_weight)
VALUES
    ('1x', 14.0, '55-65'),
    ('1x', 14.0, '65-75'),
    ('1x', 14.0, '75-85'),
    ('1x', 14.0, '85-100'),
    ('1x', 14.0, '100+'),
    ('2x', 28.0, '55-65'),
    ('2x', 28.0, '65-75'),
    ('2x', 28.0, '75-85'),
    ('2x', 28.0, '85-100'),
    ('2x', 28.0, '100+'),
    ('2-', 27.0, '55-65'),
    ('2-', 27.0, '65-75'),
    ('2-', 27.0, '75-85'),
    ('2-', 27.0, '85-100'),
    ('2-', 27.0, '100+'),
    ('2x/2-', 28.0, '55-65'),
    ('2x/2-', 28.0, '65-75'),
    ('2x/2-', 28.0, '75-85'),
    ('2x/2-', 28.0, '85-100'),
    ('2x/2-', 28.0, '100+'),
    ('4x', 52.0, '55-65'),
    ('4x', 52.0, '65-75'),
    ('4x', 52.0, '75-85'),
    ('4x', 52.0, '85-100'),
    ('4x', 52.0, '100+'),
    ('4-', 50.0, '55-65'),
    ('4-', 50.0, '65-75'),
    ('4-', 50.0, '75-85'),
    ('4-', 50.0, '85-100'),
    ('4-', 50.0, '100+'),
    ('4x/4-', 52.0, '55-65'),
    ('4x/4-', 52.0, '65-75'),
    ('4x/4-', 52.0, '75-85'),
    ('4x/4-', 52.0, '85-100'),
    ('4x/4-', 52.0, '100+'),
    ('4+', 56.0, '65-75'),
    ('4+', 56.0, '75-85'),
    ('4+', 56.0, '85-100'),
    ('8+', 96.0, '65-75'),
    ('8+', 96.0, '75-85'),
    ('8+', 96.0, '85-100'),
    ('8+', 96.0, '100+');

INSERT INTO
    boats (firm_id, spec_id, price)
VALUES
    (5, 28, 6424),
    (6, 26, 12199),
    (3, 40, 20356),
    (5, 5, 22845),
    (5, 22, 23954),
    (4, 8, 14612),
    (2, 38, 18536),
    (6, 4, 8610),
    (2, 14, 47732),
    (2, 7, 35646),
    (6, 25, 6102),
    (1, 8, 16304),
    (6, 33, 7244),
    (2, 40, 39434),
    (1, 9, 32126),
    (2, 31, 48397),
    (3, 13, 21355),
    (1, 2, 34284),
    (3, 8, 15509),
    (4, 14, 32485),
    (5, 1, 13893),
    (2, 23, 49006),
    (1, 5, 45660),
    (1, 33, 49754),
    (2, 27, 19970),
    (2, 33, 40261),
    (5, 27, 13725),
    (5, 24, 24140),
    (2, 3, 36535),
    (6, 24, 17422),
    (3, 31, 20406),
    (6, 23, 20389),
    (6, 14, 17213),
    (4, 25, 15963),
    (6, 4, 9861),
    (6, 19, 24122),
    (5, 9, 5049),
    (1, 31, 35636),
    (6, 8, 18769),
    (6, 32, 24135),
    (5, 37, 12708),
    (1, 9, 27703),
    (2, 16, 40190),
    (4, 3, 9694),
    (3, 42, 18272),
    (6, 30, 18104),
    (6, 26, 13760),
    (1, 41, 19668),
    (5, 5, 6608),
    (3, 34, 18540),
    (1, 38, 38953),
    (1, 28, 24079),
    (6, 16, 8018),
    (1, 18, 18117),
    (3, 2, 15893),
    (4, 40, 14566),
    (2, 31, 39014),
    (6, 18, 21600),
    (1, 29, 22472),
    (2, 28, 31384),
    (5, 42, 23812),
    (5, 28, 21762),
    (6, 4, 12154),
    (6, 10, 16138),
    (5, 28, 10038),
    (3, 32, 23595),
    (2, 18, 54427),
    (2, 41, 42292),
    (4, 34, 17565),
    (4, 22, 13248),
    (6, 41, 14870),
    (6, 27, 24457),
    (5, 6, 11699),
    (5, 8, 19167),
    (5, 9, 15572),
    (3, 11, 10224),
    (6, 9, 8519),
    (3, 41, 15554),
    (6, 19, 24904),
    (6, 13, 23180),
    (4, 32, 26765),
    (4, 20, 26864),
    (5, 18, 18591),
    (2, 39, 49256),
    (4, 40, 33741),
    (6, 11, 7849),
    (6, 18, 12174),
    (1, 5, 20276),
    (6, 20, 11427),
    (5, 12, 6541),
    (6, 27, 21652),
    (1, 32, 18761),
    (2, 15, 45304),
    (5, 21, 18375),
    (5, 38, 23687),
    (5, 41, 24767),
    (4, 22, 17827),
    (2, 34, 37438),
    (5, 31, 21010),
    (3, 18, 16337);