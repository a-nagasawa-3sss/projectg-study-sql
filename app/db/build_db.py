"""study-sql用のサンプルSQLiteデータベースを生成するスクリプト。

実行すると study-sql/app/db/sample.db が作成される。
既存のファイルがあれば削除して作り直す。
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sample.db"

SCHEMA = """
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    salary INTEGER NOT NULL,
    hire_date TEXT NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
);

CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    budget INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE employee_projects (
    employee_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    hours_worked INTEGER NOT NULL,
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    signup_date TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit_price INTEGER NOT NULL,
    stock_quantity INTEGER NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
"""

DEPARTMENTS = [
    (1, "営業部", "東京"),
    (2, "開発部", "大阪"),
    (3, "人事部", "東京"),
    (4, "マーケティング部", "福岡"),
    (5, "経理部", "東京"),
]

EMPLOYEES = [
    # id, name, department_id, job_title, salary, hire_date, manager_id
    (1, "山田一郎", 1, "部長", 680000, "2012-04-01", None),
    (2, "伊藤さくら", 1, "営業", 420000, "2017-04-01", 1),
    (3, "渡辺健太", 1, "営業", 390000, "2019-10-01", 1),
    (4, "佐藤太郎", 2, "部長", 720000, "2011-04-01", None),
    (5, "鈴木花子", 2, "エンジニア", 480000, "2016-04-01", 4),
    (6, "高橋翼", 2, "エンジニア", 450000, "2018-04-01", 4),
    (7, "田中美咲", 2, "エンジニア", 410000, "2020-04-01", 4),
    (8, "伊藤大輔", 2, "エンジニア", 470000, "2017-10-01", 4),
    (9, "中村洋子", 3, "部長", 650000, "2013-04-01", None),
    (10, "小林健", 3, "人事担当", 400000, "2019-04-01", 9),
    (11, "加藤愛", 3, "人事担当", 380000, "2021-04-01", 9),
    (12, "吉田真一", 4, "部長", 660000, "2014-04-01", None),
    (13, "山本桃子", 4, "マーケター", 430000, "2018-10-01", 12),
    (14, "佐々木大地", 4, "マーケター", 400000, "2020-10-01", 12),
    (15, "松本恵子", 5, "部長", 670000, "2012-10-01", None),
    (16, "井上翔", 5, "経理担当", 410000, "2017-04-01", 15),
    (17, "木村優", 5, "経理担当", 390000, "2019-04-01", 15),
    (18, "林明美", 5, "経理担当", 370000, "2021-10-01", 15),
    (19, "斎藤健二", 5, "経理担当", 360000, "2022-04-01", 15),
    (20, "清水さやか", 1, "営業", 400000, "2021-04-01", 1),
]

PROJECTS = [
    (1, "ECサイト構築", 2, 5000000, "2023-01-01", "2023-12-31"),
    (2, "社内ツール開発", 2, 2000000, "2023-03-01", "2023-09-30"),
    (3, "新規顧客開拓キャンペーン", 1, 1500000, "2023-04-01", "2023-08-31"),
    (4, "採用プロセス改善", 3, 800000, "2023-02-01", "2023-07-31"),
    (5, "ブランドリニューアル", 4, 3000000, "2023-01-15", "2023-10-31"),
    (6, "経費精算システム導入", 5, 1200000, "2023-05-01", "2023-11-30"),
    (7, "モバイルアプリ開発", 2, 4000000, "2023-06-01", "2024-03-31"),
    (8, "海外展開調査", 1, 2500000, "2023-07-01", "2024-01-31"),
]

EMPLOYEE_PROJECTS = [
    # employee_id, project_id, role, hours_worked
    (4, 1, "プロジェクトリーダー", 180),
    (5, 1, "開発", 320),
    (6, 1, "開発", 300),
    (7, 1, "開発", 280),
    (4, 2, "プロジェクトリーダー", 80),
    (6, 2, "開発", 150),
    (8, 2, "開発", 160),
    (1, 3, "プロジェクトリーダー", 60),
    (2, 3, "営業", 120),
    (3, 3, "営業", 110),
    (20, 3, "営業", 90),
    (9, 4, "プロジェクトリーダー", 50),
    (10, 4, "推進", 140),
    (11, 4, "推進", 130),
    (12, 5, "プロジェクトリーダー", 100),
    (13, 5, "企画", 220),
    (14, 5, "企画", 200),
    (15, 6, "プロジェクトリーダー", 40),
    (16, 6, "推進", 120),
    (17, 6, "推進", 110),
    (4, 7, "プロジェクトリーダー", 90),
    (5, 7, "開発", 260),
    (7, 7, "開発", 240),
    (8, 7, "開発", 250),
    (1, 8, "プロジェクトリーダー", 70),
    (2, 8, "調査", 100),
    (20, 8, "調査", 95),
]

CUSTOMERS = [
    (1, "株式会社アルファ", "東京", "日本", "2021-01-10"),
    (2, "ベータ商事", "大阪", "日本", "2021-03-15"),
    (3, "Gamma Corp", "New York", "USA", "2021-05-20"),
    (4, "デルタ製作所", "名古屋", "日本", "2021-07-01"),
    (5, "Epsilon Ltd", "London", "UK", "2021-09-12"),
    (6, "ゼータ株式会社", "福岡", "日本", "2022-01-05"),
    (7, "Eta Trading", "Sydney", "Australia", "2022-02-18"),
    (8, "シータ工業", "札幌", "日本", "2022-04-22"),
    (9, "Iota Inc", "Toronto", "Canada", "2022-06-30"),
    (10, "カッパ商店", "広島", "日本", "2022-08-14"),
    (11, "Lambda GmbH", "Berlin", "Germany", "2022-10-01"),
    (12, "ミュー株式会社", "仙台", "日本", "2023-01-09"),
    (13, "Nu Enterprises", "Singapore", "Singapore", "2023-03-25"),
    (14, "クシー商会", "神戸", "日本", "2023-05-17"),
    (15, "Omicron LLC", "Chicago", "USA", "2023-07-08"),
    (16, "Pi Solutions", "Tokyo", "USA", "2023-08-01"),
]

PRODUCTS = [
    (1, "ノートPC A", "PC", 120000, 15),
    (2, "ノートPC B", "PC", 95000, 25),
    (3, "デスクトップPC X", "PC", 150000, 10),
    (4, "ワイヤレスマウス", "アクセサリ", 3000, 200),
    (5, "メカニカルキーボード", "アクセサリ", 8000, 80),
    (6, "USB-Cハブ", "アクセサリ", 4500, 150),
    (7, "モニター24インチ", "モニター", 25000, 40),
    (8, "モニター27インチ", "モニター", 35000, 30),
    (9, "ウェブカメラ", "アクセサリ", 6000, 60),
    (10, "ヘッドセット", "アクセサリ", 7000, 90),
    (11, "外付けSSD 1TB", "ストレージ", 12000, 70),
    (12, "外付けHDD 2TB", "ストレージ", 9000, 50),
    (13, "プリンター", "プリンター", 28000, 12),
    (14, "インクカートリッジ", "消耗品", 3500, 300),
    (15, "ノートPCスタンド", "アクセサリ", 4000, 100),
    (16, "タブレット", "タブレット", 60000, 20),
    (17, "スマートフォン", "スマートフォン", 90000, 18),
    (18, "スマートウォッチ", "ウェアラブル", 35000, 25),
    (19, "Bluetoothスピーカー", "オーディオ", 9000, 45),
    (20, "ルーター", "ネットワーク機器", 15000, 35),
]

ORDERS = [
    # order_id, customer_id, order_date, status
    (1, 1, "2023-01-15", "completed"),
    (2, 2, "2023-01-20", "completed"),
    (3, 3, "2023-02-02", "completed"),
    (4, 1, "2023-02-10", "completed"),
    (5, 4, "2023-02-18", "cancelled"),
    (6, 5, "2023-03-01", "completed"),
    (7, 6, "2023-03-05", "completed"),
    (8, 2, "2023-03-12", "completed"),
    (9, 7, "2023-03-20", "shipped"),
    (10, 8, "2023-04-02", "completed"),
    (11, 3, "2023-04-10", "completed"),
    (12, 9, "2023-04-15", "completed"),
    (13, 1, "2023-04-22", "shipped"),
    (14, 10, "2023-05-01", "completed"),
    (15, 11, "2023-05-08", "completed"),
    (16, 2, "2023-05-15", "cancelled"),
    (17, 12, "2023-05-20", "completed"),
    (18, 4, "2023-06-01", "completed"),
    (19, 13, "2023-06-10", "shipped"),
    (20, 5, "2023-06-18", "completed"),
    (21, 14, "2023-07-02", "completed"),
    (22, 6, "2023-07-09", "completed"),
    (23, 15, "2023-07-15", "completed"),
    (24, 7, "2023-07-22", "shipped"),
    (25, 1, "2023-08-01", "completed"),
    (26, 8, "2023-08-09", "completed"),
    (27, 9, "2023-08-15", "cancelled"),
    (28, 3, "2023-08-22", "completed"),
    (29, 10, "2023-09-01", "completed"),
    (30, 2, "2023-09-10", "completed"),
]

ORDER_ITEMS = [
    # order_item_id, order_id, product_id, quantity
    (1, 1, 1, 2), (2, 1, 4, 5),
    (3, 2, 2, 1), (4, 2, 5, 2),
    (5, 3, 3, 1), (6, 3, 7, 1), (7, 3, 4, 3),
    (8, 4, 11, 2), (9, 4, 6, 1),
    (10, 5, 1, 1),
    (11, 6, 8, 1), (12, 6, 9, 2),
    (13, 7, 16, 1), (14, 7, 19, 1),
    (15, 8, 2, 2), (16, 8, 10, 1),
    (17, 9, 17, 1), (18, 9, 18, 1),
    (19, 10, 1, 1), (20, 10, 4, 2), (21, 10, 5, 1),
    (22, 11, 7, 2), (23, 11, 8, 1),
    (24, 12, 3, 1), (25, 12, 12, 2),
    (26, 13, 20, 1), (27, 13, 6, 3),
    (28, 14, 2, 1), (29, 14, 9, 1),
    (30, 15, 16, 2), (31, 15, 15, 4),
    (32, 16, 1, 1),
    (33, 17, 19, 2), (34, 17, 10, 1),
    (35, 18, 11, 1), (36, 18, 12, 1),
    (37, 19, 17, 1), (38, 19, 18, 2),
    (39, 20, 8, 1), (40, 20, 7, 1),
    (41, 21, 3, 1), (42, 21, 5, 2),
    (43, 22, 16, 1), (44, 22, 4, 4),
    (45, 23, 1, 2), (46, 23, 6, 2),
    (47, 24, 20, 1), (48, 24, 19, 1),
    (49, 25, 2, 3), (50, 25, 10, 2),
    (51, 26, 7, 1), (52, 26, 9, 1),
    (53, 27, 3, 1),
    (54, 28, 11, 2), (55, 28, 12, 1),
    (56, 29, 17, 1), (57, 29, 18, 1),
    (58, 30, 1, 1), (59, 30, 4, 2), (60, 30, 5, 1),
]


def build() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.executescript(SCHEMA)

        cur.executemany("INSERT INTO departments VALUES (?, ?, ?)", DEPARTMENTS)
        cur.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)", EMPLOYEES)
        cur.executemany("INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)", PROJECTS)
        cur.executemany("INSERT INTO employee_projects VALUES (?, ?, ?, ?)", EMPLOYEE_PROJECTS)
        cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", CUSTOMERS)
        cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", PRODUCTS)
        cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", ORDERS)
        cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?)", ORDER_ITEMS)

        conn.commit()
    finally:
        conn.close()

    print(f"created: {DB_PATH}")


if __name__ == "__main__":
    build()
