package com.enterprise.User;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public abstract class User {
  @Id
  @GeneratedValue(strategy=GenerationType.AUTO)
  private Integer userId;
  
  private String email;
  private String name;
  private Integer userType;
  private String address;

  public Integer getUserId() {
    return this.userId;
  }

  public void setUserId(Integer userId) {
    this.userId = userId;
  }

  public String getEmail() {
    return this.email;
  }

  public void setEmail(String email) {
    this.email = email;
  }

  public String getName() {
    return this.name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getAddress() {
    return this.address;
  }

  public void setAddress(String address) {
    this.address = address;
  }

  public Integer getUserType() {
    return this.userType;
  }

  public void setUserType(Integer userType) {
    this.userType = userType;
  }

  @Override
  public String toString() {
    return "User: \n"  + 
           "  UserId      = " + this.userId + ",\n" + 
           "  UserName    = " + this.name + ",\n" + 
           "  UserEmail   = " + this.email + ",\n" +
           "  UserAddress = " + this.address + ",\n" +
           "  UserType    = " + this.userType + ".\n\n";
  }         
}