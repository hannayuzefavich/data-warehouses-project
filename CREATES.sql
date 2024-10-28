CREATE TABLE Addresses (
	Address_id INT PRIMARY KEY IDENTITY(1,1),
	City VARCHAR(50),
	District VARCHAR(50),
	Street VARCHAR(50),
	House_number VARCHAR(10),
	Apartment_number VARCHAR(10),
	Postal_code VARCHAR(6)
);

CREATE TABLE Agencies (
	Agency_id INT PRIMARY KEY IDENTITY(1,1),
	Address_id INT FOREIGN KEY (Address_id) REFERENCES Addresses(Address_id)
);

CREATE TABLE Employees (
	Employee_id INT,
	Agency_id INT FOREIGN KEY (Agency_id) REFERENCES Agencies(Agency_id),
	Employee_name VARCHAR(15),
	Employee_surname VARCHAR(30),
	Position VARCHAR(30),
	Effective_date DATE,
	End_date DATE,
	Is_current BIT,
	Employee_pesel_number VARCHAR(11),
	PRIMARY KEY (Employee_id, Effective_date)
);

CREATE TABLE Properties (
	Property_id INT PRIMARY KEY IDENTITY(1,1),
	Address_id INT FOREIGN KEY (Address_id) REFERENCES Addresses(Address_id),
	Property_type VARCHAR(30),
	Rooms_number INT,
	Usable_area DECIMAL(10, 2),
	Rental_price DECIMAL(10,2),
	Property_owner VARCHAR(30)
);

CREATE TABLE Rental_Orders(
	Rental_order_id INT PRIMARY KEY IDENTITY(1,1),
	Employee_id INT,
	Effective_date DATE,
	Property_id INT,
	Creation_date DATE,
	Margin DECIMAL(5,2),
	Order_status VARCHAR(30),
	Rental_period INT,
	Rental_start_date DATE,
	Rental_end_date DATE,
	FOREIGN KEY (Employee_id, Effective_date) REFERENCES Employees(Employee_id, Effective_date),
    FOREIGN KEY (Property_id) REFERENCES Properties(Property_id)
);

CREATE TABLE Invoices (
	Invoice_id INT PRIMARY KEY IDENTITY(1,1),
	Rental_order_id INT FOREIGN KEY (Rental_order_id) REFERENCES Rental_orders(Rental_order_id),
	Issue_date DATE,
	Amount DECIMAL(10,2),
	Payment_date DATETIME,
	Payment_method VARCHAR(30)
);