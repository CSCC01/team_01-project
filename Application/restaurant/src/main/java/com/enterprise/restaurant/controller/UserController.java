package com.enterprise.restaurant.controller;

import com.enterprise.restaurant.dataobject.User;
import com.enterprise.restaurant.repository.UserRepository;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.ui.Model;

@RestController
@RequestMapping("/user/*")
public class UserController {
  @Autowired
  UserRepository repository;

  @GetMapping("/users")
  public List<User> list_user(){
    return repository.findAll();
  }

  // create owner
  // user_type 1 for owner -1 for customer
  // res_id -1 for customer default 0 for owner
  // exp -1 for owner default 1 for customer(can vary)
  // benefits of this is can use a if<0 to judge type
  @PostMapping("/owner")
  public User create_owner(@RequestParam("email") String email,
      @RequestParam("name") String name,
      @RequestParam("password") String password,
      @RequestParam("address") String address){
    User user = new User();
    user.setEmail(email);
    user.setName(name);
    user.setAddress(address);
    user.setPassword(password);
    user.setUser_type(1);
    user.setRes_id(0);
    user.setExperience(-1);
    return repository.save(user);
  }

  //create customer
  @PostMapping("/customer")
  public User create_customer(@RequestParam("email") String email,
      @RequestParam("name") String name,
      @RequestParam("password") String password,
      @RequestParam("address") String address){
    User user = new User();
    user.setEmail(email);
    user.setName(name);
    user.setAddress(address);
    user.setPassword(password);
    user.setUser_type(-1);
    user.setRes_id(-1);
    user.setExperience(1);
    return repository.save(user);
  }

  //login
//  @GetMapping("/login")
//  public String login(@RequestParam("email") String email,
//    @RequestParam("password") String password){
//
//    List <User> users = repository.findByEmail(email);
//    if(users==null){
//      return "no such user";
//    }else{
//      User user = users.get(0);
//      if(user.getPassword().equals(password)){
//      }
//    }
//    return "index";
//  }



}
