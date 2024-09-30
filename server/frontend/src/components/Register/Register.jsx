import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  // Function to redirect to the home page
  const goHome = () => {
    window.location.href = "/";
  };

  // Function to handle form submission
  const register = async (e) => {
    e.preventDefault();
    const registerUrl = `${window.location.origin}/djangoapp/register`;
    
    const response = await fetch(registerUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        userName,
        password,
        firstName,
        lastName,
        email,
      }),
    });

    const json = await response.json();
    
    if (json.status) {
      sessionStorage.setItem('username', json.userName);
      goHome();  // Redirect upon successful registration
    } else if (json.error === "Already Registered") {
      alert("The user with the same username is already registered.");
      goHome();  // Redirect back to home page
    }
  };

  return (
    <div className="register_container" style={{ width: "50%" }}>
      <div className="header" style={{ display: "flex", justifyContent: "space-between" }}>
        <span className="text">Sign Up</span>
        <a href="/" onClick={goHome} style={{ alignSelf: "start" }}>
          <img style={{ width: "1cm" }} src={close_icon} alt="Close" />
        </a>
      </div>
      <hr />
      
      <form onSubmit={register}>
        <div className="inputs">
          <div className="input">
            <img src={user_icon} className="img_icon" alt="Username" />
            <input 
              type="text" 
              name="username" 
              placeholder="Username" 
              className="input_field" 
              onChange={({ target }) => setUserName(target.value)} 
            />
          </div>
          <div className="input">
            <img src={user_icon} className="img_icon" alt="First Name" />
            <input 
              type="text" 
              name="first_name" 
              placeholder="First Name" 
              className="input_field" 
              onChange={({ target }) => setFirstName(target.value)} 
            />
          </div>
          <div className="input">
            <img src={user_icon} className="img_icon" alt="Last Name" />
            <input 
              type="text" 
              name="last_name" 
              placeholder="Last Name" 
              className="input_field" 
              onChange={({ target }) => setLastName(target.value)} 
            />
          </div>
          <div className="input">
            <img src={email_icon} className="img_icon" alt="Email" />
            <input 
              type="email" 
              name="email" 
              placeholder="Email" 
              className="input_field" 
              onChange={({ target }) => setEmail(target.value)} 
            />
          </div>
          <div className="input">
            <img src={password_icon} className="img_icon" alt="Password" />
            <input 
              type="password" 
              name="password" 
              placeholder="Password" 
              className="input_field" 
              onChange={({ target }) => setPassword(target.value)} 
            />
          </div>
        </div>

        <div className="submit_panel">
          <input className="submit" type="submit" value="Register" />
        </div>
      </form>
    </div>
  );
};

export default Register;
