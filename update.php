<?php
$eid=$_POST["emp_id"];
$ename=$_POST["emp_name"];
$dname=$_POST["dept_name"];
$esalary=$_POST["emp_salary"];
$eaddress=$_POST["emp_address"];

$servername="localhost";
$username="admin";
$password="admin";
$db="employee";
$conn=mysqli_connect($servername,$username,$password,$db) or die("connection failed");
$sql="update employee set emp_name='{$ename}',dept_id='{$dname}',emp_salary='{$esalary}',emp_address='{$eaddress}' where emp_id='{$eid}'";
$result=mysqli_query($conn,$sql) or die("Query unsuccessful".mysqli_error($conn));
header("location: http://localhost:8000/display.php");
mysqli_close($conn);
?>
