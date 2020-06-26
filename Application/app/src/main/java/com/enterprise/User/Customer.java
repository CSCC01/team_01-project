package com.enterprise.User;

public class Customer extends User{
  
  private float experience;

  public Customer() {
  }

  public float getExperience() {
    return this.experience;
  }

  public void setExperience(float exp) {
    this.experience = exp;
  }

  public void addExperience(float exp) {
    this.experience += exp;
  }
}