package com.enterprise.User.repository;

import com.enterprise.User.Customer;
import com.enterprise.User.Employee;
import com.enterprise.User.Owner;
import com.enterprise.User.User;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest
public class UserRepositoryTest {
  @Autowired
  private UserRepository user_repo;

  @Test
  public void checkCreateOwner() {
    Owner newOwner  = new Owner();
    newOwner.setEmail("owner.email@mail.ca");
    newOwner.setName("ABCD");
    newOwner.setAddress("abc abc abc abc");
    newOwner.setUserType(0);
    user_repo.save(newOwner);
  }

  @Test
  public void checkCreateCustomer() {
    Customer newCustomer = new Customer();
    newCustomer.setEmail("Customer123.email@mail.ca");
    newCustomer.setName("cus1");
    newCustomer.setAddress("123 456 adada");
    newCustomer.setUserType(1);
    user_repo.save(newCustomer);
  }
  
  @Test
  public void checkCreateEmployee() {
    Employee newEmployee = new Employee();
    newEmployee.setEmail("empleemail@gmail.ca");
    newEmployee.setName(" asd");
    newEmployee.setAddress("abc abc abc abc");
    newEmployee.setUserType(2);
    user_repo.save(newEmployee);
  }


  @Test
  public void findOneUser() {
    User owner = user_repo.findById(1).orElse(null);
    System.out.println(owner.toString());
    User customer = user_repo.findById(2).orElse(null);
    System.out.println(customer.toString());
    User employee = user_repo.findById(3).orElse(null);
    System.out.println(employee.toString());
  }
}