SELECT * FROM Employees
WHERE Employee_id IN (
	SELECT Employee_id FROM Employees 
	GROUP BY Employee_id
HAVING COUNT(Employee_id) >= 2
);



