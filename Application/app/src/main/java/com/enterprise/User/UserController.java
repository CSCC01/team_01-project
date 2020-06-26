package com.enterprise.User;

import java.util.List;

import com.enterprise.User.repository.UserRepository;
import com.enterprise.Restaurant.restaurantObj.Restaurant;
import com.enterprise.Restaurant.restaurantObj.RestaurantController;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
  @Autowired
  private UserRepository user_repo;

  @PostMapping("/Owner")
  public User createOwner(@RequestParam("email") String email,
                          @RequestParam("name") String name,
                          @RequestParam("address") String address
                          ) {
    Owner newOwner = new Owner();
    newOwner.setEmail(email);
    newOwner.setName(name);
    newOwner.setAddress(address);
    newOwner.setUserType(0);
    return user_repo.save(newOwner);
  }

  @PostMapping("/Customer")
  public User createCustomer(@RequestParam("email") String email,
                             @RequestParam("name") String name,
                             @RequestParam("address") String address
                             ) {
    Customer newCustomer = new Customer();
    newCustomer.setEmail(email);
    newCustomer.setName(name);
    newCustomer.setAddress(address);
    newCustomer.setUserType(1);
    return user_repo.save(newCustomer);
  }

  /* reserved */
  @PostMapping("/Employee")
  public User createEmployee(@RequestParam("email") String email,
                             @RequestParam("name") String name,
                             @RequestParam("address") String address
                             ) {
    Employee newEmployee = new Employee();
    newEmployee.setEmail(email);
    newEmployee.setName(name);
    newEmployee.setAddress(address);
    newEmployee.setUserType(2);
    return user_repo.save(newEmployee);
  }

  

  @GetMapping("/User")
  public List<User> listUser() {
    return user_repo.findAll();
  }
  @GetMapping("/User/{userId}")
  public User findUserById(@PathVariable("userId") Integer userId) {
    return user_repo.findById(userId).orElse(null);
  }
  
}