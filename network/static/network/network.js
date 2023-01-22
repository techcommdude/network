document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  //FIXME:

  // debugger;
  document.querySelector("#allPosts").addEventListener("click", () => allPosts());

  document.querySelector(".navbar-brand").addEventListener("click", () => profile());


  document.querySelector("#profile").addEventListener("click", () => profile());

  // debugger;
  document
    .querySelector("#following")
    .addEventListener("click", () => following());

  // By default, load the profile
  profile()
});

function allPosts() {
  // debugger;

  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "none";

  // return false;
}

function following() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "block";
  document.querySelector("#profile-view").style.display = "none";

  // return false;
}

function profile() {
  // debugger;
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "block";

  // return false;
}
