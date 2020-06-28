package com.enterprise.restaurant.controller;

import com.enterprise.restaurant.dataobject.User;
import com.enterprise.restaurant.repository.UserRepository;
import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/u/*")
public class LoginController {
  @Autowired
  UserRepository repository;

  @RequestMapping("/")
  public String index() {
    return "index";
  }


  @RequestMapping("/register")
  public String register() {
    return "register";
  }

  @RequestMapping("/doregister")
  public String register(HttpServletRequest servletRequest){
    String email = servletRequest.getParameter("email");
    String password = servletRequest.getParameter("password");
    User user1 = new User();
    user1.setEmail(email);
    user1.setPassword(password);
    repository.save(user1);
    return "login";
  }

  @RequestMapping("/login")
  public String login() {
    return "login";
  }

  @RequestMapping("/dologin")
  public String login(HttpServletRequest servletRequest){
    String email = servletRequest.getParameter("email");
    String password = servletRequest.getParameter("password");
    User user = repository.findByEmailAndPassword(email, password);
    if(user!=null){
      return "success";
      // target
    }
    else{
      return "login";
    }
  }

}
