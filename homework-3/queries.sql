-- Напишите запросы, которые выводят следующую информацию:
-- 1. Название компании заказчика (company_name из табл. customers) и ФИО сотрудника, работающего над заказом этой компании (см таблицу employees),
-- когда и заказчик и сотрудник зарегистрированы в городе London, а доставку заказа ведет компания United Package (company_name в табл shippers)
SELECT a.order_id, b.company_name, CONCAT(c.first_name, ' ', c.last_name) as name
FROM orders a
JOIN customers b USING (customer_id)
JOIN employees c USING (employee_id)
JOIN shippers d ON a.ship_via = d.shipper_id
WHERE b.city = 'London' AND c.city = 'London' and d.company_name = 'United Package'

-- 2. Наименование продукта, количество товара (product_name и units_in_stock в табл products),
-- имя поставщика и его телефон (contact_name и phone в табл suppliers) для таких продуктов,
-- которые не сняты с продажи (поле discontinued) и которых меньше 25 и которые в категориях Dairy Products и Condiments.
-- Отсортировать результат по возрастанию количества оставшегося товара.
SELECT a.product_name, a.units_in_stock, b.contact_name, b.phone
FROM products a
JOIN suppliers b USING (supplier_id)
JOIN categories c USING (category_id)
WHERE a.discontinued = 0 AND a.units_in_stock < 25 and c.category_name in ('Dairy Products', 'Condiments')
ORDER BY a.units_in_stock

-- 3. Список компаний заказчиков (company_name из табл customers), не сделавших ни одного заказа
SELECT a.company_name
FROM customers a
LEFT JOIN orders b USING (customer_id)
WHERE b.customer_id IS NULL

-- 4. уникальные названия продуктов, которых заказано ровно 10 единиц (количество заказанных единиц см в колонке quantity табл order_details)
-- Этот запрос написать именно с использованием подзапроса.
SELECT DISTINCT product_name
FROM products a
WHERE EXISTS(SELECT 1 FROM order_details b WHERE b.product_id = a.product_id AND quantity = 10)