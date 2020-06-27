package com.enterprise.restaurant.controller;

import com.enterprise.restaurant.dataobject.Restaurant;
import com.enterprise.restaurant.repository.RestaurantRepository;
import java.util.List;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/restaurant")
public class RestaurantController {
  @Autowired
  private RestaurantRepository repository;

  @PostMapping("/restaurants")
  public Restaurant createRestaurant(@RequestParam("resName") String resName,
                                     @RequestParam("ownerId") Integer ownerId) {
    Restaurant newRestaurant = new Restaurant();
    newRestaurant.setResName(resName);
    newRestaurant.setOwnerId(ownerId);
    return repository.save(newRestaurant);
  }

  @GetMapping("/restaurants")
  public List<Restaurant> listRestaurant() {
    return repository.findAll();
  }

  @GetMapping("/restaurant/{resId}")
  public Restaurant findRestaurantById(@PathVariable("resId") Integer resId) {
    return repository.findById(resId).orElse(null);
  }
  
}