/***********************************************
** File: Module2-NorthwindInSights.sql
** Desc: Insights based on Northwind dataset
** Auth: Shreenidhi Bharadwaj
** Date: 9/21/2019
** Ref : https://www.geeksengine.com/database/problem-solving/northwind-queries-part-1.php
** ALL RIGHTS RESERVED | DO NOT DISTRIBUTE
************************************************/
select * from categories;
select * from customer_customer_demo;
select * from customer_demographics;
select * from customers;
select * from employees;
select * from employee_territories;
select * from order_details;
select * from orders;
select * from products;
select * from region;
select * from shippers;
select * from suppliers;
select * from territories;
select * from us_states;

-- 1. Order Subtotals
-- For each order, calculate a subtotal for each Order (identified by order_id). This is a simple query using GROUP BY to aggregate data for each order.
-- Get subtotal for each order.

select order_id,
	   round(cast(sum(unit_price * quantity * (1 - discount)) as numeric), 2) as subtotal
from order_details
group by order_id
order by order_id;


-- 2. Sales by Year

-- This query shows how to get the year part from Shipped_Date column. A subtotal is calculated by a sub-query for each order. The sub-query forms a table and then joined with the Orders table.

select distinct date(a.shipped_date) as shipped_date, 
       a.order_id, 
       b.subtotal, 
       cast(date_part('year', a.shipped_date) as text) as year
from orders a 
inner join
(
    -- Get subtotal for each order
    select order_id,
	       round(cast(sum(unit_price * quantity * (1 - discount)) as numeric), 2) as subtotal
    from order_details
    group by order_id

) b on a.order_id = b.order_id

where a.shipped_date is not null
    and a.shipped_date between date('1996-12-24') and date('1997-09-30')
order by a.shipped_date;


-- 3. Employee Sales by Country
-- For each employee, get their sales amount, broken down by country name.

select e.first_name,
       e.last_name, 
       a.ship_country,
       sum(b.subtotal) as sales_amount
from employees e left outer join orders a on (e.employee_id = a.employee_id) 
inner join
(
    -- Get subtotal for each order
    select order_id,
	       round(cast(sum(unit_price * quantity * (1 - discount)) as numeric), 2) as subtotal
    from order_details
    group by order_id

) b on a.order_id = b.order_id

where a.shipped_date is not null
group by e.first_name, e.last_name, a.ship_country
order by e.first_name, e.last_name, a.ship_country

select a.ship_country,
	   e.last_name, 
       e.first_name,
       a.shipped_date,
       a.order_id,
       sum(b.subtotal) as sales_amount
from employees e left outer join orders a on (e.employee_id = a.employee_id) 
inner join
(
    -- Get subtotal for each order
    select order_id,
	       round(cast(sum(unit_price * quantity * (1 - discount)) as numeric), 2) as subtotal
    from order_details
    group by order_id

) b on a.order_id = b.order_id
where a.shipped_date is not null
group by a.ship_country, e.last_name, e.first_name, a.shipped_date, a.order_id
order by a.ship_country, e.last_name, e.first_name, a.shipped_date, a.order_id


-- 4. Current Product List
-- This is another simple query. No aggregation is used for summarizing data.

select product_id, product_name
from products
where discontinued = 0
order by product_name;

-- 5. Alphabetical List of Products with their category
-- This is a rather simple query to get an alphabetical list of products with associated category_names.

select b.*, a.category_name
from categories a 
inner join products b on a.category_id = b.category_id
where b.discontinued = 0
order by b.product_name;


-- 6. Order Details Extended
-- This query calculates sales price for each order after discount is applied.

select y.order_id, 
    y.product_id,
    x.product_name, 
    y.unit_price, 
    y.quantity, 
    y.discount, 
    round(cast(y.unit_price * y.quantity * (1 - y.discount) as numeric), 2) as extended_price
from products x
inner join order_details y on x.product_id = y.product_id
order by y.order_id;


-- 7. Sales by Category
-- For each category, we get the list of products sold and the total sales amount. 
-- Note that, in the second query, the inner query for table c is to get sales for each product on each order. 
-- It then joins with outer query on Product_ID. In the outer query, products are grouped for each category.

-- Query 1: normal joins

select distinct a.category_id, 
    a.category_name,  
    b.product_name, 
    sum(round(cast(y.unit_price * y.quantity * (1 - y.discount) as numeric), 2)) as product_sales
from order_details y
inner join orders d on d.order_id = y.order_id
inner join products b on b.product_id = y.product_id
inner join categories a on a.category_id = b.category_id
where d.order_date between date('1997/1/1') and date('1997/12/31')
group by a.category_id, a.category_name, b.product_name
order by a.category_name, b.product_name, product_sales;
 

-- Query 2: join with a sub query
 
-- This query returns identical result as above, but here sub query is used to calculate extended price 
-- which then used in the main query to get ProductSales

select distinct a.category_id, 
    a.category_name, 
    b.product_name, 
    sum(c.extended_price) as product_sales
from categories a 
inner join products b on a.category_id = b.category_id
inner join 
(
    select distinct y.order_id, 
        y.product_id, 
        x.product_name, 
        y.unit_price, 
        y.quantity, 
        y.discount, 
        round(cast(y.unit_price * y.quantity * (1 - y.discount) as numeric), 2) as extended_price
    from products x
    inner join order_details y on x.product_id = y.product_id
    order by y.order_id
) c on c.product_id = b.product_id
inner join orders d on d.order_id = c.order_id
where d.order_date between date('1997/1/1') and date('1997/12/31')
group by a.category_id, a.category_name, b.product_name
order by a.category_name, b.product_name, product_sales;


-- 8. Ten Most Expensive Products
-- The two queries below return the same result. It demonstrates how MySQL limits the number of records returned.
-- The first query uses correlated sub-query to get the top 10 most expensive products.
-- The second query retrieves data from an ordered sub-query table and then the keyword LIMIT is used outside the sub-query to restrict the number of rows returned.

-- Query 1

select a.product_name as ten_most_expensive_products, 
       a.unit_price
from products as a
where 10 >= (select count(distinct unit_price)
                    from products as b
                    where b.unit_price >= a.unit_price)
order by a.unit_price desc;
 
-- Query 2

select * from
(
    select product_name as ten_most_expensive_products, 
           unit_price
    from products
    order by unit_price desc
) as a
limit 10;


-- 9. Products by Category
-- This is a simple query just because it's in Access Northwind so we converted it here in MySQL.

select distinct a.category_name, 
    b.product_name, 
    b.quantity_per_unit, 
    b.units_in_stock, 
    b.discontinued
from categories a
inner join products b on a.category_id = b.category_id
where b.discontinued = 0
order by a.category_name, b.product_name;


-- 10. Customers and Suppliers by City
-- This query shows how to use UNION to merge Customers and Suppliers into one result set by
-- identifying them as having different relationships to Northwind Traders - Customers and Suppliers.

select city, company_name, contact_name, 'customers' as relationship 
from customers
union
select city, company_name, contact_name, 'suppliers'
from suppliers
order by city, company_name;


-- 11. Products Above Average Price
-- This query shows how to use sub-query to get a single value (average unit price) that can be used in the outer-query.

select product_name, unit_price
from products
where unit_price > (select avg(unit_price) from products)
order by unit_price;


-- 12. Product Sales for 1997
-- This query shows how to group categories and products by quarters and shows sales amount for each quarter.

select distinct a.category_name, 
    b.product_name, 
    round(cast(sum(c.unit_price * c.Quantity * (1 - c.Discount)) as numeric), 2) as product_sales,
    concat('Qtr ', extract(quarter from d.shipped_date)) as shipped_quarter
from categories a
inner join products b on a.category_id = b.category_id
inner join order_details c on b.product_id = c.product_id
inner join orders d on d.order_id = c.order_id
where d.shipped_date between date('1997/01/01') and date('1997/12/31')
group by a.category_name, 
    b.product_name, 
    concat('Qtr ', extract(quarter from d.shipped_date))
order by a.category_name, 
    b.product_name, 
    shipped_quarter;
    

-- 13. Category Sales for 1997
-- This query shows how to group categories by quarters and shows sales amount for each quarter.

select distinct a.category_name,
    round(cast(sum(c.unit_price * c.Quantity * (1 - c.Discount)) as numeric), 2) as product_sales,
    concat('Qtr ', extract(quarter from d.shipped_date)) as shipped_quarter
from categories a
inner join products b on a.category_id = b.category_id
inner join order_details c on b.product_id = c.product_id
inner join orders d on d.order_id = c.order_id
where d.shipped_date between date('1997/01/01') and date('1997/12/31')
group by a.category_name,
    concat('Qtr ', extract(quarter from d.shipped_date))
order by a.category_name,
    shipped_quarter;


-- 14. Quarterly Orders by Product
-- This query shows how to convert order dates to the corresponding quarters. It also demonstrates how SUM function is used together with CASE statement to get sales for each quarter, where quarters are converted from OrderDate column.

select a.product_name, 
    d.company_name, 
    extract(year from c.order_date) as order_year,    
    sum(round(cast(case extract(quarter from c.order_date) when '1'
    	 then b.unit_price * b.quantity * (1-b.discount) 
    	 else 0 end as numeric),2)) as "Qtr 1",
	sum(round(cast(case extract(quarter from c.order_date) when '2'
    	 then b.unit_price * b.quantity * (1-b.discount) 
    	 else 0 end as numeric),2)) as "Qtr 2",
    sum(round(cast(case extract(quarter from c.order_date) when '3'
    	 then b.unit_price * b.quantity * (1-b.discount) 
    	 else 0 end as numeric),2)) as "Qtr 3",
    sum(round(cast(case extract(quarter from c.order_date) when '4'
    	 then b.unit_price * b.quantity * (1-b.discount) 
    	 else 0 end as numeric),2)) as "Qtr 4"
from products a 
inner join order_details b on a.product_id = b.product_id
inner join orders c on c.order_id = b.order_id
inner join customers d on d.customer_id = c.customer_id 
where c.order_date between date('1997/01/01') and date('1997/12/31')
group by a.product_name, 
    d.company_name, 
    extract(year from c.order_date)
order by a.product_name, d.company_name;


-- 15. Invoice
-- A simple query to get detailed information for each sale so that invoice can be issued.

select b.ship_name, 
    b.ship_address, 
    b.ship_city, 
    b.ship_region, 
    b.ship_postal_code, 
    b.ship_country, 
    b.customer_id, 
    c.company_name, 
    c.address, 
    c.city, 
    c.region, 
    c.postal_code, 
    c.country, 
    concat(d.first_name, ' ', d.last_name) as sales_person, 
    b.order_id, 
    b.order_date, 
    b.required_date, 
    b.shipped_date, 
    a.company_name, 
    e.product_id, 
    f.product_name, 
    e.unit_price, 
    e.quantity, 
    e.discount,
    e.unit_price * e.quantity * (1 - e.discount) as extended_price,
    b.freight
from shippers a 
inner join orders b on a.shipper_id = b.ship_via 
inner join customers c on c.customer_id = b.customer_id
inner join employees d on d.employee_id = b.employee_id
inner join order_details e on b.order_id = e.order_id
inner join products f on f.product_id = e.product_id
order by b.ship_name;


-- 16. Number of units in stock by category and supplier continent
-- This query shows that case statement is used in GROUP BY clause to list the number of units in stock for each product category and supplier's continent. Note that, if only s.Country (not the case statement) is used in the GROUP BY, duplicated rows will exist for each product category and supplier continent.

select c.category_name as "product_category", 
       case when s.country in 
                 ('UK','Spain','Sweden','Germany','Norway',
                  'Denmark','Netherlands','Finland','Italy','France')
            then 'Europe'
            when s.country in ('USA','Canada','Brazil') 
            then 'America'
            else 'Asia-Pacific'
        end as "supplier_continent", 
        sum(p.units_in_stock) as units_in_stock
from suppliers s 
inner join products p on p.supplier_id=s.supplier_id
inner join categories c on c.category_id=p.category_id 
group by c.category_name, 
         case when s.country in 
                 ('UK','Spain','Sweden','Germany','Norway',
                  'Denmark','Netherlands','Finland','Italy','France')
              then 'Europe'
              when s.country in ('USA','Canada','Brazil') 
              then 'America'
              else 'Asia-Pacific'
         end
order by 1, 2;