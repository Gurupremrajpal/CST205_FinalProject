var stateData;
getStates();
document.querySelector("#zip").addEventListener("change", displayCity);
document.querySelector("#password").addEventListener("click", displaySuggestedPassword);
document.querySelector("#userName").addEventListener("change", validateUserName);
document.querySelector("#state").addEventListener("change", addCounties);
document.querySelector("#button").addEventListener("click", validate);

async function displayCity() {
  let zipCode = document.querySelector("#zip").value;
  let url = `https://cst336.herokuapp.com/projects/api/cityInfoAPI.php?zip=${zipCode}`;
  let data = await fetchData(url);

  if (data == false) {
    document.querySelector("#vzip").innerHTML = " Zip  not found";
    document.querySelector("#city").innerHTML = "";
    document.querySelector("#lati").innerHTML= "";
    document.querySelector("#longi").innerHTML = "";
  } 
  else {
    document.querySelector("#vzip").innerHTML = "";
    document.querySelector("#city").innerHTML = data.city;
    document.querySelector("#lati").innerHTML= data.latitude;
    document.querySelector("#longi").innerHTML = data.longitude;
  }
}

async function displaySuggestedPassword() {
  let url = "https://itcdland.csumb.edu/~milara/api/suggestedPwd.php?length=8";
  let data  = await fetchData(url);
  document.querySelector("#suggest").innerHTML = ` Suggested Password: ${data.password}`;
}
async function validateUserName(){
  let userName = document.querySelector("#userName").value;
  let validation = `https://cst336.herokuapp.com/projects/api/usernamesAPI.php?username=${userName}`;
  let data = await fetchData(validation);
  if (data.available == true ){
    document.querySelector("#avail").innerHTML = " Username available";
    document.querySelector("#avail").style.color = "green";
  }
  else{
    document.querySelector("#avail").innerHTML = " Username unavailable";
    document.querySelector("#avail").style.color = "red";
  }
  return data.available;
}
async function getStates() {
  let url = "https://cst336.herokuapp.com/projects/api/state_abbrAPI.php";
  stateData = await fetchData(url);
  for (i = 0; i < stateData.length; i++) {
    document.querySelector("#state").innerHTML += `<option>${stateData[i].state}</option>`;
  }
  
}
async function addCounties() {
  let state = document.querySelector("#state").value;
  let usps = "";
  for (i = 0; i < stateData.length; i++) {
    if (stateData[i].state == state) {
      usps = stateData[i].usps;
    }
  }
  let url = `https://cst336.herokuapp.com/projects/api/countyListAPI.php?state=${usps}`;
  let data = await fetchData(url);
  document.querySelector("#county").innerHTML = "<option>Select:</option>"
  for (i = 0; i < data.length; i++) {
    document.querySelector("#county").innerHTML += `<option>${data[i].county}</option>`;
  }
}
async function validate() {
  let userName = document.querySelector("#userName").value;
  let password = document.querySelector("#password").value;
  let passwordRetype = document.querySelector("#passwordRetype").value;
  document.querySelector("#sValid").innerHTML = "";
  if (await validateUserName() == false) {
    document.querySelector("#sValid").innerHTML += " Invalid Username! ";
  }
  if (userName.length == 0) {
    document.querySelector("#sValid").innerHTML += " No Username! ";
  }
  if (password.length < 6) {
    document.querySelector("#sValid").innerHTML += " Password must be at least 6 characters! "; 
  } 
  if (password != passwordRetype) {
    document.querySelector("#sValid").innerHTML += " Passwords do not match! "; 
  }
}

async function fetchData(url) {
  let response = await fetch(url);
  let data = await response.json();
  return data;
} 