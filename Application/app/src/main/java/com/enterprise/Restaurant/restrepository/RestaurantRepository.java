package com.enterprise.Restaurant.restrepository;

import com.enterprise.Restaurant.restaurantObj.Restaurant;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RestaurantRepository extends JpaRepository <Restaurant,Integer>{
  
}