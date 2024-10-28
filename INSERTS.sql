BULK INSERT [RealEstateAgency].[dbo].[Addresses]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\addresses.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');


BULK INSERT [RealEstateAgency].[dbo].[Agencies]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\offices.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');



BULK INSERT [RealEstateAgency].[dbo].[Properties]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\real_estates.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');

BULK INSERT [RealEstateAgency].[dbo].[Employees]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\employess.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');

BULK INSERT [RealEstateAgency].[dbo].[Rental_Orders]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\orders.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');

BULK INSERT [RealEstateAgency].[dbo].[Invoices]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\invoices.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');

BULK INSERT [RealEstateAgency].[dbo].[Employees]
FROM 'C:\Users\juzef\PycharmProjects\data-generator\employess_t2.csv'
WITH (FIRSTROW =1,
	FIELDTERMINATOR = ',',
	CODEPAGE = '65001',
	ROWTERMINATOR = '\n');