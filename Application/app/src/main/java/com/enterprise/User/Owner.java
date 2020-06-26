package com.enterprise.User;

import com.enterprise.Restaurant.restaurantObj.Restaurant;

public class Owner extends User {

  private Restaurant restaurant;

  public Owner() {
  }

  public Restaurant getRestaurant() {
    return this.restaurant;
  }

  public void setRestaurant(Restaurant restaurant) {
    this.restaurant = restaurant;
  }
}