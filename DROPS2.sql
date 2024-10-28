--DROP TABLE Invoices
--DROP TABLE Rental_Orders
--DROP TABLE Properties


--DROP TABLE Employees
--DROP TABLE Agencies
--DROP TABLE Addresses





DELETE FROM Invoices
DBCC CHECKIDENT ('Invoices', RESEED, 0);

DELETE FROM Rental_Orders
DBCC CHECKIDENT ('Rental_Orders', RESEED, 0);

DELETE FROM Properties
DBCC CHECKIDENT ('Properties', RESEED, 0);

DELETE FROM Employees
DBCC CHECKIDENT ('Employees', RESEED, 0);

DELETE FROM Agencies
DBCC CHECKIDENT ('Agencies', RESEED, 0);

DELETE FROM Addresses
DBCC CHECKIDENT ('Addresses', RESEED, 0);

