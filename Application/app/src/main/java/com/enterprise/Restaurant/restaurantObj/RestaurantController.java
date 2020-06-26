package com.enterprise.Restaurant.restaurantObj;

import java.util.List;

import com.enterprise.Restaurant.restrepository.RestaurantRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RestaurantController {
  @Autowired
  private RestaurantRepository repository;

  @PostMapping("/Restaurant")
  public Restaurant createRestaurant(@RequestParam("resName") String resName,
                                     @RequestParam("ownerId") Integer ownerId) {
    Restaurant newRestaurant = new RestaurantImpl();
    newRestaurant.setResName(resName);
    newRestaurant.setOwnerId(ownerId);
    return repository.save(newRestaurant);
  }

  @GetMapping("/Restaurant")
  public List<Restaurant> listRestaurant() {
    return repository.findAll();
  }

  @GetMapping("/Restaurant/{resId}")
  public Restaurant findRestaurantById(@PathVariable("resId") Integer resId) {
    return repository.findById(resId).orElse(null);
  }
  
}