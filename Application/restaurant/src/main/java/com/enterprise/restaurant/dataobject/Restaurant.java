package com.enterprise.restaurant.dataobject;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Restaurant {
  @Id
  @GeneratedValue
  private Integer resId;

  private String resName;
  private Integer ownerId;

  public Restaurant() {
  }

  public Integer getResId() {
    return resId;
  }

  public void setResId(Integer resId) {
    this.resId = resId;
  }

  public String getResName() {
    return resName;
  }

  public void setResName(String resName) {
    this.resName = resName;
  }

  public Integer getOwnerId() {
    return ownerId;
  }

  public void setOwnerId(Integer ownerId) {
    this.ownerId = ownerId;
  }
}