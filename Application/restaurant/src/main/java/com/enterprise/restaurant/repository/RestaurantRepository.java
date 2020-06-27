package com.enterprise.restaurant.repository;

import com.enterprise.restaurant.dataobject.Restaurant;
import org.springframework.data.jpa.repository.JpaRepository;

public interface RestaurantRepository extends JpaRepository <Restaurant,Integer>{
  
}