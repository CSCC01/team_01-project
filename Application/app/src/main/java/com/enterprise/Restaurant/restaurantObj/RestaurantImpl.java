package com.enterprise.Restaurant.restaurantObj;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class RestaurantImpl implements Restaurant {
  @Id
  @GeneratedValue(strategy=GenerationType.AUTO)
  private Integer resId;
  private String resName;
  private Integer ownerId;

  public RestaurantImpl() {
  }

  @Override
  public Integer getResId() {
    return this.resId;
  }

  @Override
  public void setResId(Integer resId) {
    this.resId = resId;
  }

  @Override
  public String getResName() {
    return this.resName;
  }

  @Override
  public void setResName(String resName) {
    this.resName = resName;
  }

  @Override
  public Integer getOwnerId() {
    return this.ownerId;
  }

  @Override
  public void setOwnerId(Integer ownerId) {
    this.ownerId = ownerId;
  }
  
}