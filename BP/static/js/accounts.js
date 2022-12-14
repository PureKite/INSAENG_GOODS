const container = document.querySelector(".container"),
signUp = document.querySelector(".signup-link"),
login = document.querySelector(".login-link");

// js code to appear signup and login form
signUp.addEventListener("click", ( )=>{
  container.classList.add("active");
});
login.addEventListener("click", ( )=>{
  container.classList.remove("active");
});
