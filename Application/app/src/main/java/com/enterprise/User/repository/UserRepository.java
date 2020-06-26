package com.enterprise.User.repository;

import com.enterprise.User.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository <User, Integer>{
  
}